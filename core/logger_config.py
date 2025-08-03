import os, logging
from datetime import datetime
from logging.config import dictConfig

from core.settings import settings

# Ensure the monitoring folder exists
monitoring_folder = settings.MONITORING_DIR
if not os.path.exists(monitoring_folder):
    os.makedirs(monitoring_folder, exist_ok=True)

if not os.path.exists(os.path.join(monitoring_folder, "app")):
    os.makedirs(os.path.join(monitoring_folder, "app"), exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d")
app_log_filename = os.path.join(monitoring_folder, f"app/app_{timestamp}.log")
monitoring_log_filename = os.path.join(monitoring_folder, f"monitoring_{timestamp}.log")
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": app_log_filename,
        },
        "monitoring_file": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": monitoring_log_filename,
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file", "monitoring_file"],
    },
}

dictConfig(logging_config)
logger = logging.getLogger(__name__)
# logger.info("Logger configured successfully.")