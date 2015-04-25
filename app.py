import re
import sched
import time

from amazon_echo import Echo
import nest
from nest import utils as nest_utils

from secrets import *  # nopep8

scheduler = sched.scheduler(time.time, time.sleep)
echo = Echo(echo_username, echo_password)
napi = nest.Nest(nest_username, nest_password)

TEMP_REGEX = r'^(?:set )?(?:the )?(?:temperature )?(?:to )?((\w+)\s+(\w+)*)\s*degrees$'  # nopep8

# Only allow temps between 50 - 79 degrees
ones_dict = {'one': 1,
             'two': 2,
             'three': 3,
             'four': 4,
             'five': 5,
             'six': 6,
             'seven': 7,
             'eight': 8,
             'nine': 9}
tens_dict = {'fifty': 50,
             'sixty': 60,
             'seventy': 70}


def set_temp(napi, temp):
    """
    Set the temperature given an integer value in degrees F
    """
    for device in napi.devices:
        f_temp = temp
        device.temperature = nest_utils.f_to_c(f_temp)
        print("Setting nest temp to {} degrees".format(f_temp))


def convert_temp(m):
    """
    Convert a matched re phrase to an integer
    """
    temp_spoken = m.group(1)
    temp_tens = m.group(2)
    temp_ones = m.group(3)
    temp = tens_dict.get(temp_tens, None)
    if temp:
        if temp_ones:
            temp += ones_dict.get(temp_ones, 0)
    else:
        print("Cannot set temperature to '{}' degrees".format(temp_spoken))  # nopep8
    return temp


def main(scheduler):
    """
    Get the last todo item and determine if Nest
    should be set to Away Mode, Home Mode, or made
    to change the temperature.
    """

    todo = echo.get_latest_todo()
    if todo:
        todo = todo.lower()
        print("Task: '{}'".format(todo))
        if todo in ["set away", "set a way"]:
            napi.structures[0].away = True
            print("Setting Nest to away mode")
        elif todo == "set home":
            napi.structures[0].away = False
            print("Setting Nest to home mode")
        else:
            temp_regex = re.compile(TEMP_REGEX)
            m = temp_regex.match(todo)
            if m:
                temp = convert_temp(m)
                if temp:
                    set_temp(napi, temp)

    scheduler.enter(5, 1, main, (scheduler,))


if __name__ == "__main__":
    try:
        scheduler.enter(0, 1, main, (scheduler,))
        scheduler.run()
    except KeyboardInterrupt:
        pass
