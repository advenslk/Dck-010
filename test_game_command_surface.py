import ast
from pathlib import Path

BOT_SOURCE = Path(__file__).with_name("bot.py").read_text(encoding="utf-8")


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


def test_game_plan_admin_commands_have_vps_style_aliases():
    create = _command_decorators("game_plan_create")
    edit = _command_decorators("game_plan_edit")
    delete = _command_decorators("game_plan_delete")
    listing = _command_decorators("game_plan_list")

    assert any('"create-game-plan"' in d and "aliases" in d for d in create)
    assert any('"edit-game-plan"' in d and "aliases" in d for d in edit)
    assert any('"delete-game-plan"' in d and "aliases" in d for d in delete)
    assert any('"list-game-plans"' in d and "aliases" in d for d in listing)


def test_help_menu_contains_game_server_category():
    assert '"games":' in BOT_SOURCE
    assert 'game-plan-create' in BOT_SOURCE
    assert 'game-plan-edit' in BOT_SOURCE
    assert 'game-plan-delete' in BOT_SOURCE
    assert 'game-category-create' in BOT_SOURCE
    assert 'game-category-edit' in BOT_SOURCE
    assert 'game-category-delete' in BOT_SOURCE
