import logging
import os.path
from pathlib import Path

# Исходныя папка проекта
from dotenv import load_dotenv

# Корневая директория проекта
BASE_DIR = Path(__file__).parent.parent

# Общий уровень логирования
LOGGING_LEVEL = logging.DEBUG

# Общая кодировка проекта
ENCODING = 'utf-8'

load_dotenv(os.path.join(BASE_DIR, '.env'))

# Настройки доступа к Telemetron Api
TELEMETRON_CLIENT_ID = os.getenv('TELEMETRON_CLIENT_ID', default='client_id')
TELEMETRON_CLIENT_SECRET = os.getenv('TELEMETRON_CLIENT_SECRET',
                                     default='client_secret')
TELEMETRON_GRANT_TYPE = os.getenv('TELEMETRON_GRANT_TYPE',
                                  default='password')
TELEMETRON_PASSWORD = os.getenv('TELEMETRON_PASSWORD',
                                default='client_password')
TELEMETRON_LOGIN = os.getenv('TELEMETRON_LOGIN', default='client_login')
TELEMETRON_SCOPE = os.getenv('TELEMETRON_SCOPE', default='teleport')

# SQLITE3_DATABASE_FILE = os.path.join(BASE_DIR, 'sqlite3.db')

# Настройки бота Telegram
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
