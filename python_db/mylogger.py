import logging
# 로그 파일 생성
# 소프트웨어나 시스템 실행중 발생하는 이벤트를 시간 순서대로 기록한 파일
# 버그 추적 / 사용자 활동 모니터링 및 다양한 용도로 사용
# 로그레벨 (warning, error, info, debug....)

def make_logger(fileNm, name=None):
    # 로그 생성
    logger = logging.getLogger(name)
    # 로거 레벨 설정 ( DEBUG로 설정 시 모두 처리 됨)
    logger.setLevel(logging.DEBUG)
    # 출력 포멧 설정
    formatter = (logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - (message)s)"))
    # handler 설정
    console = logging.StreamHandler()
    file_handler = logging.FileHandler(filename = fileNm)
    # handler level 설정
    console.setLevel(logging.INFO)
    file_handler.setLevel(logging.DEBUG) # DEBUG - INFO - WARNING - ERROR - CRITICAL
    # 출력 포멧 설정
    console.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # logger에 추가
    logger.addHandler(console)
    logger.addHandler(file_handler)
    return logger