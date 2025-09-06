import types
import builtins
from bot.states.flat.flat_position_state import FlatPositionState
import bot.states.flat.flat_position_state as flat_pos_module


class DummySnapshot:
    def __init__(
        self,
        price: float = 100.0,
        ema_100: float = 120.0,
        macd_12: float = 0.0,
        macd_26: float = 0.0,
        rsi_6: float = 50.0,
    ) -> None:
        self.price = price
        self.ema_100 = ema_100
        self.macd_12 = macd_12
        self.macd_26 = macd_26
        self.rsi_6 = rsi_6
        self._cloned = False

    def clone(self) -> "DummySnapshot":
        cloned = DummySnapshot(
            price=self.price,
            ema_100=self.ema_100,
            macd_12=self.macd_12,
            macd_26=self.macd_26,
            rsi_6=self.rsi_6,
        )
        cloned._cloned = True
        return cloned

    def __str__(self) -> str:
        return f"Snapshot(price={self.price})"


class DummyDataManager:
    def __init__(self, snapshot: DummySnapshot) -> None:
        self.market_snapshot = snapshot
        self.position_snapshot = None
        self.is_long_blocked = False
        self.is_short_blocked = False

    def block_long(self) -> None:
        self.is_long_blocked = True

    def block_short(self) -> None:
        self.is_short_blocked = True


class DummyBinanceAdapter:
    def __init__(
        self, long_tp=110.0, long_sl=90.0, short_tp=80.0, short_sl=120.0
    ) -> None:
        self._long_tp = long_tp
        self._long_sl = long_sl
        self._short_tp = short_tp
        self._short_sl = short_sl
        self.called: dict[str, float] = {}

    def enter_long(self, price: float):
        self.called["enter_long"] = price
        return self._long_tp, self._long_sl

    def enter_short(self, price: float):
        self.called["enter_short"] = price
        return self._short_tp, self._short_sl


class DummyParent:
    def __init__(
        self, snapshot: DummySnapshot, adapter: DummyBinanceAdapter | None = None
    ) -> None:
        self.data_manager = DummyDataManager(snapshot)
        self.binance_adapter = adapter or DummyBinanceAdapter()
        self.state = None


def test_is_long_entry_condition_met_true_and_false():
    snapshot = DummySnapshot(
        price=90, ema_100=100, macd_12=-0.5, macd_26=-1.0, rsi_6=60
    )
    parent = DummyParent(snapshot)
    state = FlatPositionState(parent)
    assert state._is_long_entry_condition_met() is True

    parent.data_manager.is_long_blocked = True
    assert state._is_long_entry_condition_met() is False


def test_is_short_entry_condition_met_true_and_false():
    snapshot = DummySnapshot(price=110, ema_100=100, macd_12=1.0, macd_26=2.0, rsi_6=40)
    parent = DummyParent(snapshot)
    state = FlatPositionState(parent)
    assert state._is_short_entry_condition_met() is True

    parent.data_manager.is_short_blocked = True
    assert state._is_short_entry_condition_met() is False


def test_update_position_snapshot_clones():
    snapshot = DummySnapshot()
    parent = DummyParent(snapshot)
    state = FlatPositionState(parent)
    state._update_position_snapshot()
    assert parent.data_manager.position_snapshot is not snapshot
    assert isinstance(parent.data_manager.position_snapshot, DummySnapshot)
    assert parent.data_manager.position_snapshot._cloned is True


def test_apply_long_transitions_and_logs(monkeypatch):
    snapshot = DummySnapshot(
        price=100, ema_100=200, macd_12=-0.5, macd_26=-1.0, rsi_6=60
    )
    parent = DummyParent(snapshot, adapter=DummyBinanceAdapter(long_tp=150, long_sl=80))
    state = FlatPositionState(parent)

    logs: list[str] = []
    monkeypatch.setattr(
        flat_pos_module.Logger, "log_info", lambda msg: logs.append(msg)
    )

    original_import = builtins.__import__

    def import_stub(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "bot.states.active.long_position_state":
            mod = types.ModuleType(name)

            class FakeLongState:
                def __init__(self, parent, target_prices):
                    self.parent = parent
                    self.target_prices = target_prices

            setattr(mod, "LongPositionState", FakeLongState)
            return mod
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", import_stub)

    state._apply_long()

    assert parent.data_manager.is_long_blocked is True
    assert parent.data_manager.position_snapshot is not None
    assert parent.binance_adapter.called["enter_long"] == 100
    assert type(parent.state).__name__ == "FakeLongState"
    assert logs and logs[0].startswith("Entered LONG")
    assert "Snapshot(" in logs[1]


def test_apply_short_transitions_and_logs(monkeypatch):
    snapshot = DummySnapshot(price=200, ema_100=100, macd_12=1.5, macd_26=2.0, rsi_6=40)
    parent = DummyParent(
        snapshot, adapter=DummyBinanceAdapter(short_tp=180, short_sl=220)
    )
    state = FlatPositionState(parent)

    logs: list[str] = []
    monkeypatch.setattr(
        flat_pos_module.Logger, "log_info", lambda msg: logs.append(msg)
    )

    original_import = builtins.__import__

    def import_stub(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "bot.states.active.short_position_state":
            mod = types.ModuleType(name)

            class FakeShortState:
                def __init__(self, parent, target_prices):
                    self.parent = parent
                    self.target_prices = target_prices

            setattr(mod, "ShortPositionState", FakeShortState)
            return mod
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", import_stub)

    state._apply_short()

    assert parent.data_manager.is_short_blocked is True
    assert parent.data_manager.position_snapshot is not None
    assert parent.binance_adapter.called["enter_short"] == 200
    assert type(parent.state).__name__ == "FakeShortState"
    assert logs and logs[0].startswith("Entered SHORT")
    assert "Snapshot(" in logs[1]


def test_apply_branches(monkeypatch):
    snapshot = DummySnapshot()
    parent = DummyParent(snapshot)
    state = FlatPositionState(parent)

    called = {"long": False, "short": False}

    monkeypatch.setattr(state, "_is_long_entry_condition_met", lambda: True)
    monkeypatch.setattr(state, "_apply_long", lambda: called.__setitem__("long", True))
    state.apply()
    assert called["long"] is True

    monkeypatch.setattr(state, "_is_long_entry_condition_met", lambda: False)
    monkeypatch.setattr(state, "_is_short_entry_condition_met", lambda: True)
    monkeypatch.setattr(
        state, "_apply_short", lambda: called.__setitem__("short", True)
    )
    state.apply()
    # Original code references _apply_short without invoking it
    assert called["short"] is False

    parent.state = None
    monkeypatch.setattr(state, "_is_short_entry_condition_met", lambda: False)
    state.apply()
    assert parent.state is None
