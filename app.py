import re
import sched
import time

from amazon_echo import Echo
import nest
from nest import utils as nest_utils
import wolframalpha

from secrets import *  # nopep8


scheduler = sched.scheduler(time.time, time.sleep)
echo = Echo(echo_username, echo_password)
napi = nest.Nest(nest_username, nest_password)
wa_client = wolframalpha.Client(wolframalpha_app_id)


def set_temp(napi, temp):
    """
    Set the temperature given an integer value in degrees F
    """
    for device in napi.devices:
        f_temp = temp
        device.temperature = nest_utils.f_to_c(f_temp)
        print("Setting nest temp to {} degrees".format(f_temp))


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
            temp_regex = re.compile(r'^set temperature (\w+\s*\w+)+ degrees$')
            m = temp_regex.match(todo)
            if m:
                spoken_temp = m.group(1)
                res = wa_client.query(spoken_temp)
                temp = int(res.pods[0].text)
                set_temp(napi, temp)

    scheduler.enter(5, 1, main, (scheduler,))


if __name__ == "__main__":
    try:
        scheduler.enter(0, 1, main, (scheduler,))
        scheduler.run()
    except KeyboardInterrupt:
        pass
