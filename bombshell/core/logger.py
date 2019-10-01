import logging


class Logger:
    log = logging.getLogger()

    @classmethod
    def info(cls, msg: str, output=False):
        cls.log.info("{}".format(msg))
        if output:
            cls.output_log('info', msg)

    @classmethod
    def warning(cls, msg: str, output=False):
        cls.log.warning("{}".format( msg))
        if output:
            cls.output_log('warning', msg)

    @classmethod
    def debug(cls, msg: str, output=False):
        cls.log.debug("{}".format(msg ))
        if output:
            cls.output_log('debug', msg)

    @classmethod
    def error(cls, msg: str, output=False):
        cls.log.error("{}".format(msg))
        if output:
            cls.output_log('error', msg)

    @classmethod
    def output_log(cls, level: str, msg: str):
        print("[{}]: {}".format(level.upper(), msg))
