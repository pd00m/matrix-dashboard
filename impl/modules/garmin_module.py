
import time
import datetime

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
        
        client_id = config['Garmin']['email']
        client_password = config['Garmin']['password']
        api = Garmin(client_id, client_password)
        api.login()

        print(api.get_full_name())