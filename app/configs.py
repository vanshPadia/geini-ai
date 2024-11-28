import os
from dotenv import load_dotenv
import logging as log

load_dotenv(override=True)

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
MODEL_TEMPERATURE = 0
MODEL_NAME = "gpt-4o-mini"
LANGFUSE_USER_NAME = os.getenv('LANGFUSE_USER_NAME','genie-dev-user')
INTEGRATION_BASE_URL = os.getenv('INTEGRATION_BASE_URL', 'http://172.17.0.1:8080')
ENABLED_LANGFUSE_METRICS = os.getenv("ENABLED_LANGFUSE_METRICS", "False").lower() == "true"

log.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(levelname)s : %(filename)s #%(lineno)d - %(message)s',
    handlers=[log.StreamHandler()])