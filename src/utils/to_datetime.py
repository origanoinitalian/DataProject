import time

def to_datetime(epoch_time: int) -> str:
    return time.strftime("%Y-%m-%d", time.gmtime(epoch_time))
    
