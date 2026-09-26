import ast
from pathlib import Path

BOT_SOURCE = Path(__file__).with_name("bot.py").read_text(encoding="utf-8")
EMOJI_SOURCE = Path(__file__).with_name("emoji.py").read_text(encoding="utf-8")


def _command_decorators(function_name):
    tree = ast.parse(BOT_SOURCE)
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_name:
            return [
                ast.unparse(dec)
                for dec in node.decorator_list
                if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute)
            ]
    raise AssertionError(f"Function {function_name!r} not found")


def _function(function_name):
    tree = ast.parse(BOT_SOURCE)
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_name:
            return node
    raise AssertionError(f"Function {function_name!r} not found")


def test_game_plan_admin_commands_have_vps_style_aliases():
    create = _command_decorators("game_plan_create")
    edit = _command_decorators("game_plan_edit")
    delete = _command_decorators("game_plan_delete")
    listing = _command_decorators("game_plan_list")

    assert any("create-game-plan" in d and "aliases" in d for d in create)
    assert any("edit-game-plan" in d and "aliases" in d for d in edit)
    assert any("delete-game-plan" in d and "aliases" in d for d in delete)
    assert any("list-game-plans" in d and "aliases" in d for d in listing)


def test_game_plan_create_uses_gb_for_ram_and_disk():
    fn = _function("game_plan_create")
    arg_names = [arg.arg for arg in fn.args.args]
    assert arg_names[2:6] == ["ram_gb", "cpu_percent", "disk_gb", "days"]
    assert "ram_mb" not in arg_names
    assert "disk_mb" not in arg_names

    source = ast.unparse(fn)
    assert "ram_gb * 1024" in source
    assert "disk_gb * 1024" in source


def test_game_plan_edit_accepts_gb_resource_fields():
    fn = _function("game_plan_edit")
    source = ast.unparse(fn)
    assert '"ram_gb"' in source
    assert '"disk_gb"' in source


def test_help_menu_contains_game_server_category():
    assert '"games":' in BOT_SOURCE
    assert 'game-plan-create' in BOT_SOURCE
    assert 'game-plan-edit' in BOT_SOURCE
    assert 'game-plan-delete' in BOT_SOURCE
    assert 'game-category-create' in BOT_SOURCE
    assert 'game-category-edit' in BOT_SOURCE
    assert 'game-category-delete' in BOT_SOURCE
    assert '<ram_gb>' in BOT_SOURCE
    assert '<disk_gb>' in BOT_SOURCE


def test_help_category_emojis_use_centralized_game_constants():
    assert 'EMOJI_GAME' in EMOJI_SOURCE
    assert 'EMOJI_GAME_SERVER' in EMOJI_SOURCE
    assert 'EMOJI_NETWORK' in EMOJI_SOURCE
    assert 'EMOJI_GAME_NODE' in EMOJI_SOURCE
    assert 'EMOJI_GAME_SECURITY' in EMOJI_SOURCE
    start = BOT_SOURCE.index('def get_category_emoji')
    end = BOT_SOURCE.index('def update_embed', start)
    helper = BOT_SOURCE[start:end]
    assert '"games": EMOJI_GAME' in helper
    assert '"vps": EMOJI_GAME_SERVER' in helper
    assert '"ports": EMOJI_NETWORK' in helper
    assert '"nodes": EMOJI_GAME_NODE' in helper
    assert '"admin": EMOJI_GAME_SECURITY' in helper


import re
import sys

sys.path.insert(0, str(Path(__file__).parent))
import emoji as emoji_registry


_EMOJI_PATTERN = re.compile(
    r"[\U0001F000-\U0001FAFF\u2300-\u23FF\u2600-\u27BF\u2B00-\u2BFF]"
    r"(?:[\uFE0F\u20E3\U0001F3FB-\U0001F3FF]*)?"
    r"(?:\u200D[\U0001F000-\U0001FAFF\u2300-\u23FF\u2600-\u27BF\u2B00-\u2BFF]"
    r"(?:[\uFE0F\u20E3\U0001F3FB-\U0001F3FF]*)?)*"
)


def test_every_bot_emoji_is_registered_in_emoji_module():
    source_emojis = set(_EMOJI_PATTERN.findall(BOT_SOURCE))
    assert len(source_emojis) >= 90
    missing = source_emojis.difference(emoji_registry.EMOJI_REPLACEMENTS)
    assert not missing, f"Unregistered bot emojis: {sorted(missing)}"


def test_emoji_registry_exposes_replacement_function_and_custom_mappings():
    assert callable(emoji_registry.replace_emojis)
    assert emoji_registry.replace_emojis("🎮") == emoji_registry.EMOJI_GAME
    assert emoji_registry.replace_emojis("🔄") == emoji_registry.EMOJI_REINSTALL
    assert emoji_registry.replace_emojis("📊") == emoji_registry.EMOJI_STATS
    assert emoji_registry.replace_emojis("❌") == emoji_registry.EMOJI_CANCEL
    assert emoji_registry.replace_emojis("✅") == emoji_registry.EMOJI_SUCCESS


def test_discord_send_paths_apply_centralized_emoji_replacement():
    assert "replace_emojis(" in BOT_SOURCE
    assert "replace_emojis(content)" in BOT_SOURCE
    assert "replace_emojis" in BOT_SOURCE[BOT_SOURCE.index("def _install_components_v2_compat"):]


def test_emoji_registry_has_all_existing_custom_constants():
    required = [
        "EMOJI_REINSTALL", "EMOJI_START", "EMOJI_STOP", "EMOJI_SSH",
        "EMOJI_STATS", "EMOJI_RESOURCES", "EMOJI_EXPIRATION",
        "EMOJI_USAGE", "EMOJI_CONTROLS", "EMOJI_WARNING", "EMOJI_SUCCESS",
        "EMOJI_CONFIRM", "EMOJI_CANCEL", "EMOJI_GAME", "EMOJI_MINECRAFT",
        "EMOJI_BEDROCK", "EMOJI_GAME_SERVER", "EMOJI_PANEL", "EMOJI_CONSOLE",
        "EMOJI_BACKUP", "EMOJI_NETWORK", "EMOJI_FILES", "EMOJI_RENEW",
        "EMOJI_UPGRADE", "EMOJI_DELETE", "EMOJI_DEPLOY", "EMOJI_GAME_JAVA",
        "EMOJI_GAME_BEDROCK", "EMOJI_GAME_OTHER", "EMOJI_GAME_CATEGORY",
        "EMOJI_GAME_NODE", "EMOJI_GAME_ALLOCATION", "EMOJI_GAME_SECURITY",
    ]
    for name in required:
        assert hasattr(emoji_registry, name), name
