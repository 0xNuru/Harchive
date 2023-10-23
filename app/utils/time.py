#!/usr/bin/env python3

# some time convertion implementations
# written by Hamza <cyb3rguru>


from datetime import datetime


def compare_time(utcTimeValue: datetime.utcnow, duration: int) -> bool:
    """_summary_: 
    compares the stored utctime value with
    the duration specified in minutes

    Args:
        utcTimeValue (_type_): _description_
        duration (_type_): _description_
    """
    storedTime = utcTimeValue
    currentTime = datetime.utcnow()
    diff = currentTime - storedTime
    diff_seconds = diff.seconds
    minute_diff = diff_seconds // 60

    if minute_diff > duration:
        return True
    
    else:
        return False
    
def getRemain_time(utcTimeValue: datetime.utcnow) -> [bool, int]:
    """_summary_: 
    compares the stored utctime value with
    the duration specified in minutes

    Args:
        utcTimeValue (_type_): _description_
        duration (_type_): _description_
    """
    storedTime = utcTimeValue
    currentTime = datetime.utcnow()
    diff = currentTime - storedTime
    diff_seconds = diff.seconds
    minute_diff = diff_seconds // 60

    return minute_diff