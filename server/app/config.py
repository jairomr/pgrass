from dynaconf import Dynaconf
from loguru import logger

logger.add("../sys.log")

settings = Dynaconf(
    envvar_prefix="POTSA",
    settings_files=["settings.toml", ".secrets.toml"],
    environments=True,
    load_dotenv=True
)