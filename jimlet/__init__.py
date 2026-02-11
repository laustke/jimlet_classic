"""
Jimlet Text-to-Speech Converter.
Classic Edition.

Check out the current version of Jimlet TTS Converter at https://jimlet.com.
It includes the newest voice engine, multilingual support, easy Windows installation,
and many extended features.
"""


__copyright__ = "© 2026 Jimlet.com"
__license__ = "Non-commercial"
__edition__ = "Classic: Early functional edition"
__version__ = "0.6"

import os
import sys
from pathlib import Path
import logging
from platformdirs import user_config_dir
from .set_loggers import set_screen_logger, set_file_logger
from . import config as conf

logger = logging.getLogger(__name__)

def _get_data_path() -> Path:
    p = Path(user_config_dir(conf.APP_NAME, conf.APP_AUTHOR))
    p.mkdir(parents=True, exist_ok=True)

    return p

data_path = _get_data_path()

logger = logging.getLogger(__name__)

if conf.LOG_TO == "screen":
    set_screen_logger(logger)
else:
    log_fname = (data_path / "jimlet.log").absolute()
    set_file_logger(logger, log_fname, conf.LOG_LEVEL)


def _get_proj_path():
    p = Path(__file__).parent.parent
    return p

proj_path = _get_proj_path()

