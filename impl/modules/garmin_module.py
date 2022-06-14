
import time
import datetime
from math import ceil

from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarminConnectAuthenticationError,
)

class GarminModule: 
    def __init__(self, config):
        self.invalid = False
        print("Garmin Module has been initiated")

        ## Initialize Garmin api with your credentials
        try:
            client_id = config['Garmin']['email']
            client_password = config['Garmin']['password']
            self.api = Garmin(client_id, client_password)
            self.api.login()

            print(self.api.get_last_activity())
        except Exception as e:
            print("[Garmin Module] error trying to authenticate",e)
            self.invalid = True

    def getLastActivity(self):
        last_activity = self.api.get_last_activity()
        print("distance: ", last_activity['distance'])
        return (ceil(last_activity['distance'] * 100 / 100.0))