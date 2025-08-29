from dataclasses import dataclass
from utils.file_utils import FileUtils
from base_dir import BASE_DIR


@dataclass(frozen=True)
class BotSettings:
    API_PUBLIC_KEY: str
    API_SECRET_KEY: str
    SYMBOL: str
    COIN_PRECISION: int
    TP_RATIO: float
    SL_RATIO: float
    LEVERAGE: int
    TEST_MODE: bool
    DEBUG_MODE: bool
    INTERVAL: str
    SLEEP_DURATION: float
    OUTPUT_CSV_PATH: str


SETTINGS_PATH = BASE_DIR / "settings.toml"
_settings = FileUtils.read_toml_file(SETTINGS_PATH)
SETTINGS = BotSettings(
    _settings["api"]["public_key"],
    _settings["api"]["secret_key"],
    _settings["position"]["symbol"],
    _settings["position"]["coin_precision"],
    _settings["position"]["tp_ratio"],
    _settings["position"]["sl_ratio"],
    _settings["position"]["leverage"],
    _settings["runtime"]["test_mode"],
    _settings["runtime"]["debug_mode"],
    _settings["runtime"]["interval"],
    _settings["runtime"]["sleep_duration"],
    _settings["output"]["csv_path"],
)
