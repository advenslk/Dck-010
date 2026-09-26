import json
import unittest

from pterodactyl import GameServerPlan, normalize_plan, build_server_payload


class PterodactylPlanTests(unittest.TestCase):
    def test_normalize_plan_keeps_category_and_resources(self):
        plan = normalize_plan({
            "name": "Survival",
            "category": "Minecraft Java",
            "ram_mb": 4096,
            "cpu_percent": 200,
            "disk_mb": 40960,
            "duration_days": 30,
            "cost_coins": 1500,
            "node_id": 1,
            "nest_id": 1,
            "egg_id": 3,
            "allocation_id": 7,
        })
        self.assertIsInstance(plan, GameServerPlan)
        self.assertEqual(plan.category, "Minecraft Java")
        self.assertEqual(plan.ram_mb, 4096)
        self.assertEqual(plan.cost_coins, 1500)

    def test_server_payload_uses_plan_resources(self):
        plan = GameServerPlan(
            id=1, name="Survival", category="Minecraft Java", description="",
            ram_mb=4096, cpu_percent=200, disk_mb=40960, duration_days=30,
            cost_coins=1500, node_id=1, nest_id=1, egg_id=3, allocation_id=7,
            docker_image="ghcr.io/pterodactyl/yolks:java_21", startup="java -Xms128M -Xmx{{SERVER_MEMORY}}M -jar {{SERVER_JARFILE}}",
            environment={"SERVER_JARFILE": "server.jar"}, active=True, icon="🎮"
        )
        payload = build_server_payload(plan, "Test Server", 12345, "player")
        self.assertEqual(payload["user"], 12345)
        self.assertEqual(payload["deploy"]["allocation"]["default"] if "deploy" in payload else None, 7)
        self.assertEqual(payload["limits"]["memory"], 4096)
        self.assertEqual(payload["limits"]["cpu"], 200)
        self.assertEqual(payload["limits"]["disk"], 40960)


if __name__ == "__main__":
    unittest.main()
