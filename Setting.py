# settings.py
from configparser import ConfigParser
from pathlib import Path

# Base directory = project root (adjust if needed)
BASE_DIR = Path(__file__).resolve().parent

_config = ConfigParser()
_config.read(BASE_DIR / "config.ini", encoding="utf-8")


class Settings:
    # ---- Database ----
    DB_CONNECTION_STRING: str = _config["Database"]["connection_string"]

    # ---- Parameters ----
    PACKBOX_DIFF_PRICE: int = int(_config["Parameter"]["packBox_diff_price"])

    # ---- Paths (as absolute Path objects) ----
    FARSI_FONT_PATH: Path = BASE_DIR / _config["Paths"]["farsi_font_path"]
    ARIAL_FONT_PATH: Path = BASE_DIR / _config["Paths"]["Arial_font_path"]
    BRAND_IMAGE_PATH: Path = BASE_DIR / _config["Paths"]["brand_image_path"]
    FOOTER_IMAGE_PATH: Path = BASE_DIR / _config["Paths"]["footer_image"]
    OUTPUT_DIR: Path = BASE_DIR / _config["Paths"]["output_dir"]
    ICON_PATH: Path = BASE_DIR / _config["Paths"]["icon_path"]

    PAYMENT_MESSAGE = _config.get("Text", "payment_message")
    PACKBOX_MESSAGE = _config.get("Text", "packBox_message", fallback=None)
    BRAND_TEXT_MESSAGE = _config.get("Text", "brand_text_message")

    # ---- Names ----
    CAT1_NAME: str = _config["Name"]["Cat1"]
    CAT2_NAME: str = _config["Name"]["Cat2"]
    CAT3_NAME: str = _config["Name"]["Cat3"]
    CAT4_NAME: str = _config["Name"]["Cat4"]
    CAT5_NAME: str = _config["Name"]["Cat5"]

    SUB_CAT1_NAME_1: str = _config["Name"]["SUB_Cat1_1"]
    SUB_CAT1_NAME_2: str = _config["Name"]["SUB_Cat1_2"]
    SUB_CAT1_NAME_3: str = _config["Name"]["SUB_Cat1_3"]
    SUB_CAT1_NAME_4: str = _config["Name"]["SUB_Cat1_4"]


settings = Settings()
