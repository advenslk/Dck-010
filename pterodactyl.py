"""Pterodactyl integration and game-server plan management for Dck-010.

This module keeps Pterodactyl concerns separate from the existing LXC/VPS engine.
The bot owns economy, plans and lifecycle policy; Pterodactyl owns game-server runtime.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


@dataclass(frozen=True)
class GameServerPlan:
    id: int
    name: str
    category: str
    description: str
    ram_mb: int
    cpu_percent: int
    disk_mb: int
    duration_days: int
    cost_coins: int
    node_id: int
    nest_id: int
    egg_id: int
    allocation_id: int
    docker_image: str
    startup: str
    environment: Dict[str, Any]
    active: bool
    icon: str = "🎮"


def normalize_plan(row: Dict[str, Any]) -> GameServerPlan:
    environment = row.get("environment", {})
    if isinstance(environment, str):
        try:
            environment = json.loads(environment or "{}")
        except json.JSONDecodeError:
            environment = {}
    return GameServerPlan(
        id=int(row.get("id", 0)),
        name=str(row.get("name", "Unnamed")),
        category=str(row.get("category", "Game Servers")),
        description=str(row.get("description", "")),
        ram_mb=int(row.get("ram_mb", 0)),
        cpu_percent=int(row.get("cpu_percent", 0)),
        disk_mb=int(row.get("disk_mb", 0)),
        duration_days=int(row.get("duration_days", 30)),
        cost_coins=int(row.get("cost_coins", 0)),
        node_id=int(row.get("node_id", 0)),
        nest_id=int(row.get("nest_id", 0)),
        egg_id=int(row.get("egg_id", 0)),
        allocation_id=int(row.get("allocation_id", 0)),
        docker_image=str(row.get("docker_image", "")),
        startup=str(row.get("startup", "")),
        environment=environment,
        active=bool(int(row.get("active", 1))) if isinstance(row.get("active", 1), (int, str)) else bool(row.get("active", True)),
        icon=str(row.get("icon", "🎮")),
    )


def build_server_payload(plan: GameServerPlan, name: str, panel_user_id: int, external_identifier: str) -> Dict[str, Any]:
    """Build the Pterodactyl Application API server-create payload."""
    return {
        "name": name,
        "user": panel_user_id,
        "nest": plan.nest_id,
        "egg": plan.egg_id,
        "docker_image": plan.docker_image,
        "startup": plan.startup,
        "environment": dict(plan.environment),
        "limits": {
            "memory": plan.ram_mb,
            "swap": 0,
            "disk": plan.disk_mb,
            "io": 500,
            "cpu": plan.cpu_percent,
        },
        "feature_limits": {"databases": 0, "allocations": 1, "backups": 0},
        "deploy": {
            "locations": [],
            "dedicated_ip": False,
            "port_range": [],
            "nodes": [plan.node_id] if plan.node_id else [],
            "allocation": {"default": plan.allocation_id} if plan.allocation_id else None,
        },
        "external_id": external_identifier,
        "start_on_completion": False,
    }


class PterodactylError(RuntimeError):
    pass


class PterodactylClient:
    """Small synchronous Application API client used behind bot executor calls."""

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None, timeout: int = 15):
        self.base_url = (base_url or os.getenv("PTERODACTYL_URL", "")).rstrip("/")
        self.api_key = api_key or os.getenv("PTERODACTYL_API_KEY", "")
        self.timeout = timeout
        if not self.base_url or not self.api_key:
            raise PterodactylError("PTERODACTYL_URL and PTERODACTYL_API_KEY are required")

    def _request(self, method: str, path: str, **kwargs) -> Any:
        headers = kwargs.pop("headers", {})
        headers.update({"Authorization": f"Bearer {self.api_key}", "Accept": "Application/vnd.pterodactyl.v1+json", "Content-Type": "application/json"})
        try:
            response = requests.request(method, f"{self.base_url}{path}", headers=headers, timeout=self.timeout, **kwargs)
        except requests.RequestException as exc:
            raise PterodactylError(f"Panel connection failed: {exc}") from exc
        if not response.ok:
            try:
                detail = response.json()
            except ValueError:
                detail = response.text[:500]
            raise PterodactylError(f"Pterodactyl API {response.status_code}: {detail}")
        if not response.content:
            return {}
        return response.json()

    def get_user(self, email: str) -> Optional[Dict[str, Any]]:
        page = 1
        while page <= 10:
            data = self._request("GET", "/api/application/users", params={"filter[email]": email, "page": page})
            for item in data.get("data", []):
                attrs = item.get("attributes", item)
                if attrs.get("email", "").lower() == email.lower():
                    return attrs
            if not data.get("meta", {}).get("pagination", {}).get("current_page"):
                break
            if page >= data["meta"]["pagination"].get("total_pages", page):
                break
            page += 1
        return None

    def create_user(self, username: str, email: str, password: Optional[str] = None) -> Dict[str, Any]:
        body = {"username": username, "email": email, "first_name": username, "last_name": "HelzerX", "root_admin": False, "language": "en"}
        if password:
            body["password"] = password
        return self._request("POST", "/api/application/users", json=body).get("attributes", {})

    def ensure_user(self, username: str, email: str) -> Dict[str, Any]:
        existing = self.get_user(email)
        return existing or self.create_user(username, email)

    def create_server(self, plan: GameServerPlan, name: str, panel_user_id: int, external_identifier: str) -> Dict[str, Any]:
        payload = build_server_payload(plan, name, panel_user_id, external_identifier)
        payload["deploy"] = {k: v for k, v in payload["deploy"].items() if v is not None}
        return self._request("POST", "/api/application/servers", json=payload).get("attributes", {})

    def get_server(self, server_id: int) -> Dict[str, Any]:
        return self._request("GET", f"/api/application/servers/{server_id}").get("attributes", {})

    def delete_server(self, server_id: int, force: bool = False) -> None:
        self._request("DELETE", f"/api/application/servers/{server_id}", params={"force": str(force).lower()})

    def suspend_server(self, server_id: int) -> None:
        self._request("POST", f"/api/application/servers/{server_id}/suspend")

    def unsuspend_server(self, server_id: int) -> None:
        self._request("POST", f"/api/application/servers/{server_id}/unsuspend")

    def reinstall_server(self, server_id: int) -> None:
        self._request("POST", f"/api/application/servers/{server_id}/reinstall")

    def list_nodes(self) -> List[Dict[str, Any]]:
        data = self._request("GET", "/api/application/nodes", params={"per_page": 100})
        return [x.get("attributes", x) for x in data.get("data", [])]

    def list_allocations(self, node_id: int) -> List[Dict[str, Any]]:
        data = self._request("GET", f"/api/application/nodes/{node_id}/allocations", params={"per_page": 100})
        return [x.get("attributes", x) for x in data.get("data", [])]


def init_pterodactyl_db(get_db) -> None:
    """Create game-server categories, plans, panel accounts and server tables."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS game_categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT DEFAULT '',
        icon TEXT DEFAULT '🎮',
        active INTEGER DEFAULT 1,
        created_at TEXT NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS game_server_plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        category TEXT NOT NULL,
        description TEXT DEFAULT '',
        ram_mb INTEGER NOT NULL,
        cpu_percent INTEGER NOT NULL,
        disk_mb INTEGER NOT NULL,
        duration_days INTEGER NOT NULL,
        cost_coins INTEGER NOT NULL,
        node_id INTEGER NOT NULL,
        nest_id INTEGER NOT NULL,
        egg_id INTEGER NOT NULL,
        allocation_id INTEGER DEFAULT 0,
        docker_image TEXT DEFAULT '',
        startup TEXT DEFAULT '',
        environment TEXT DEFAULT '{}',
        active INTEGER DEFAULT 1,
        icon TEXT DEFAULT '🎮',
        created_at TEXT NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS panel_accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        discord_user_id TEXT UNIQUE NOT NULL,
        panel_user_id INTEGER UNIQUE NOT NULL,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        created_at TEXT NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS game_servers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        public_id TEXT UNIQUE NOT NULL,
        discord_user_id TEXT NOT NULL,
        panel_user_id INTEGER NOT NULL,
        panel_server_id INTEGER UNIQUE NOT NULL,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        plan_id INTEGER NOT NULL,
        status TEXT DEFAULT 'unknown',
        expires_at TEXT NOT NULL,
        suspended INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS game_server_transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_server_id INTEGER,
        discord_user_id TEXT NOT NULL,
        type TEXT NOT NULL,
        amount INTEGER NOT NULL,
        description TEXT,
        created_at TEXT NOT NULL
    )""")
    defaults = [
        ("Minecraft Java", "Java Edition servers", "⛏️"),
        ("Minecraft Bedrock", "Bedrock Edition servers", "🧱"),
        ("Other Games", "Other Pterodactyl-supported games", "🎮"),
    ]
    for name, description, icon in defaults:
        cur.execute("INSERT OR IGNORE INTO game_categories (name, description, icon, created_at) VALUES (?, ?, ?, datetime('now'))", (name, description, icon))
    conn.commit()
    conn.close()


def get_game_categories(get_db, active_only: bool = True) -> List[Dict[str, Any]]:
    conn = get_db()
    q = "SELECT * FROM game_categories" + (" WHERE active = 1" if active_only else "") + " ORDER BY name"
    rows = [dict(x) for x in conn.execute(q).fetchall()]
    conn.close()
    return rows


def get_game_plans(get_db, category: Optional[str] = None, active_only: bool = True) -> List[GameServerPlan]:
    conn = get_db()
    q = "SELECT * FROM game_server_plans WHERE 1=1"
    args: List[Any] = []
    if active_only:
        q += " AND active = 1"
    if category:
        q += " AND category = ?"
        args.append(category)
    q += " ORDER BY cost_coins, ram_mb"
    rows = [normalize_plan(dict(x)) for x in conn.execute(q, args).fetchall()]
    conn.close()
    return rows


def get_game_plan(get_db, plan_id: int) -> Optional[GameServerPlan]:
    conn = get_db()
    row = conn.execute("SELECT * FROM game_server_plans WHERE id = ?", (plan_id,)).fetchone()
    conn.close()
    return normalize_plan(dict(row)) if row else None
