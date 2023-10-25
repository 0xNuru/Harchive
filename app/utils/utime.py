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
    minute_diff = diff_seconds / 60

    if minute_diff > duration:
        return True
    
    else:
        return False
    
def getRemain_time(utcTimeValue: datetime.utcnow, duration: int) -> [int, int]:
    """_summary_: 
    compares the stored utctime value with
    the duration specified in minutes

    Args:
        utcTimeValue (_type_): _description_
        duration (_type_): _description_
    """
    current_time = datetime.utcnow()
    time_difference = current_time - utcTimeValue
    remaining_duration = (duration * 60) - time_difference.seconds
    
    # Extract remaining minutes and seconds
    remaining_minutes = int(remaining_duration // 60)
    remaining_seconds = int(remaining_duration % 60)
    
    return remaining_minutes, remaining_seconds
