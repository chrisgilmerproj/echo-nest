import re
import sched
import time

from amazon_echo import Echo
import nest
from nest import utils as nest_utils
import pychromecast
from pychromecast.controllers.media import MediaController
from secrets import *  # nopep8

scheduler = sched.scheduler(time.time, time.sleep)
echo = Echo(echo_username, echo_password)
napi = nest.Nest(nest_username, nest_password)

# Constants
TEMP_REGEX = r'^(?:set )?(?:the )?(?:temperature )?(?:to )?((\w+)\s+(\w+)*)\s*degrees$'  # nopep8
CAST_REGEX = r'^(?:turn )?(?:on )?(?:the )?(television|tv|chromecast)$'  # nopep8

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


def enable_chromecast():
    """
    Turn on the chromecast
    """
    cast_name = "Library"
    print("Turning on the '{}' chromecast".format(cast_name))
    cast = pychromecast.get_chromecast(friendly_name=cast_name)
    media = MediaController()
    cast.register_handler(media)
    time.sleep(1)
    print("Attempting to play media")
    media.play_media('http://upload.wikimedia.org/wikipedia/commons/7/7f/Pug_portrait.jpg', 'jpg')  # nopep8
    time.sleep(30)
    cast.quit_app()


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
            cast_regex = re.compile(CAST_REGEX)
            m_temp = temp_regex.match(todo)
            m_cast = cast_regex.match(todo)
            if m_temp:
                temp = convert_temp(m_temp)
                if temp:
                    set_temp(napi, temp)
            elif m_cast:
                enable_chromecast()

    scheduler.enter(5, 1, main, (scheduler,))


if __name__ == "__main__":
    try:
        scheduler.enter(0, 1, main, (scheduler,))
        scheduler.run()
    except KeyboardInterrupt:
        pass
