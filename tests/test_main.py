# tests/test_main.py
import importlib
import runpy
import sys
import types
from typing import Any, cast


def _install_dummy_rembot(monkeypatch, calls):
    bot_pkg = types.ModuleType("bot")
    bot_pkg.__path__ = []  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "bot", bot_pkg)

    rem_bot_mod = types.ModuleType("bot.rem_bot")

    class DummyRemBot:
        def __init__(self):
            calls.append("init")

        def run(self):
            calls.append("run")

    cast(Any, rem_bot_mod).RemBot = DummyRemBot  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "bot.rem_bot", rem_bot_mod)


def test_main_function_calls_rembot_run(monkeypatch):
    calls = []
    _install_dummy_rembot(monkeypatch, calls)
    mod = importlib.import_module("main")
    importlib.reload(mod)
    mod.main()
    assert calls == ["init", "run"]


def test_module_runs_when_invoked_as_script(monkeypatch):
    calls = []
    _install_dummy_rembot(monkeypatch, calls)
    runpy.run_module("main", run_name="__main__")
    assert calls == ["init", "run"]
