import mylogger
log = mylogger.make_logger("test.log", "logger_test 파일")

log.debug("debug test")
log.info("info test")
log.warning("warning test")

try:
    result = 2 / 0
except Exception as e:
    log.exception(str(e))

log.critical("!!!!!!!!")
