import logging

# Selenium
PAGE_LOAD_TIMEOUT = 60

# Portals
CLICK_PAY_URL = "https://www.clickpay.com/"

# Logging
BASE_LOGGER_CONFIG = {
    'format': "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    'level': logging.DEBUG,
    'rotating_file_handler': {
        'file_name': 'app.log',
        'max_bytes': 1024 * 1024 * 100,
        'backup_count': 20
    },
}

# Database
DB_URL = 'sqlite:///db/tenants.db'
