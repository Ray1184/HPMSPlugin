from sys import platform


def get_current_dir():
    import os
    return os.path.dirname(os.path.realpath(__file__))


def get_os():
    if platform == "linux" or platform == "linux2":
        return "linux"
    else:
        return "win"


def system(msg):
    print("[SYSTEM] " + msg)


def severe(msg):
    print("[SEVERE] " + msg)


def debug(msg):
    if log_level <= 2:
        print("[ DEBUG] " + msg)


def info(msg):
    if log_level <= 3:
        print("[  INFO] " + msg)


def trace(msg):
    if log_level <= 1:
        print("[ TRACE] " + msg)


def warn(msg):
    if log_level <= 4:
        print("[  WARN] " + msg)


def set_log_level(logging):
    global log_level
    if logging is None:
        log_level = 5
    else:
        if logging.upper() == "TRACE":
            log_level = 1
        else:
            if logging.upper() == "DEBUG":
                log_level = 2
            else:
                if logging.upper() == "INFO":
                    log_level = 3
                else:
                    if logging.upper() == "WARN":
                        log_level = 4
                    else:
                        log_level = 5
