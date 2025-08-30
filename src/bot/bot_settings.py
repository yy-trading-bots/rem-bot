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
    _settings["API"]["PUBLIC_KEY"],
    _settings["API"]["SECRET_KEY"],
    _settings["POSITION"]["SYMBOL"],
    _settings["POSITION"]["COIN_PRECISION"],
    _settings["POSITION"]["TP_RATIO"],
    _settings["POSITION"]["SL_RATIO"],
    _settings["POSITION"]["LEVERAGE"],
    _settings["RUNTIME"]["TEST_MODE"],
    _settings["RUNTIME"]["DEBUG_MODE"],
    _settings["RUNTIME"]["INTERVAL"],
    _settings["RUNTIME"]["SLEEP_DURATION"],
    _settings["OUTPUT"]["CSV_PATH"],
)
