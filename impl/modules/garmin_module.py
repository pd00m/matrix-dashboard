import configparser
from queue import LifoQueue
from threading import Thread
import time
import datetime

from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarminConnectAuthenticationError,
)

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
lastweek = today - datetime.timedelta(days=7)


class GarminModule:
    def __init__(self, config):
        self.last_activity = None
        self.activity_queue = LifoQueue()
        self.sleep_queue = LifoQueue()

        self.invalid = False
        print("Garmin Module has been initiated")

        ## Initialize Garmin api with your credentials
        try:
            # client_id = config["Garmin"]["email"]
            # client_password = config["Garmin"]["password"]
            # self.api = Garmin(client_id, client_password)
            # self.api.login()

            self.thread = Thread(
                target=garminLogin,
                args=(
                    self.activity_queue,
                    self.sleep_queue,
                    config["Garmin"]["email"],
                    config["Garmin"]["password"],
                ),
            )
            self.thread.start()

        except Exception as e:
            print("[Garmin Module] error trying to authenticate", e)
            self.invalid = True

    def getLastActivity(self):
        if not self.activity_queue.empty():
            self.last_activity = self.activity_queue.get()
            self.activity_queue.queue.clear()
        # last_activity = self.api.get_last_activity()
        return (
            self.last_activity["distance"],
            self.last_activity["duration"],
            self.last_activity["averageSpeed"],
            self.last_activity["averageHR"],
            self.last_activity["averageRunningCadenceInStepsPerMinute"],
        )

    def getSleedData(self):
        sleep_data = self.api.get_sleep_data(today)
        sleep = sleep_data["dailySleepDTO"]
        sleeplevels = sleep_data["sleepLevels"]
        return (
            get_attribute(sleep, "unmeasurableSleepSeconds", 0),
            get_attribute(sleep, "deepSleepSeconds", 0),
            get_attribute(sleep, "lightSleepSeconds", 0),
            get_attribute(sleep, "remSleepSeconds", 0),
            get_attribute(sleep, "averageRespirationValue", ""),
            get_attribute(sleep, "awakeSleepSeconds", 0),
            get_attribute(sleep, "sleepStartTimestampGMT", 0),
            get_attribute(sleep, "sleepEndTimestampGMT", 0),
            sleeplevels,
        )


def garminLogin(activity_queue, sleep_queue, email, pw):
    # try:
    #     print("[Garmin Module] attempting to log in again. ", email, pw)
    #     self.api = Garmin(email, pw)
    #     self.api.login()
    # except Exception as e:
    #     print("[Garmin Module] error trying to authenticate", e)
    #     self.invalid = True
    lastTimeCall = 0

    while True:
        currTime = time.time()
        if currTime - lastTimeCall >= 600:
            try:
                print("[Garmin Module] attempting to log in again. ", email, pw)
                api_call = Garmin(email, pw)
                api_call.login()
                activity_queue.put(api_call.get_last_activity())
                sleep_queue.put(api_call.get_sleep_data(today))
                lastTimeCall = currTime
            except Exception as e:
                print("[Garmin Module] error trying to authenticate", e)
                pass


# def garminLogin(self, email, pw):
#     try:
#         print("[Garmin Module] attempting to log in again. ", email, pw)
#         self.api = Garmin(email, pw)
#         self.api.login()
#     except Exception as e:
#         print("[Garmin Module] error trying to authenticate", e)
#         self.invalid = True


def get_attribute(data, attribute, default_value):
    return data.get(attribute) or default_value
