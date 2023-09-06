from clojos_common.util import logger

from climate.util import env

logger.LogConfig().configure(log_level=env.Env().log_level())
