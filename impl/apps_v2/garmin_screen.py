
import time
from PIL import Image, ImageFont, ImageDraw
from InputStatus import InputStatusEnum
from ast import literal_eval
import math


medium_blue = (0,77,179)
white = (230,255,255)

class GarminScreen: 
    def __init__(self, config, modules, default_actions):
        print("Garmin Screen Test")
        self.modules = modules
        self.default_actions = default_actions

        self.font = ImageFont.truetype("fonts/tiny.otf", 5)

        self.canvas_width = config.getint('System', 'canvas_width', fallback=64)
        self.canvas_height = config.getint('System', 'canvas_height', fallback=32)

        self.text_color = literal_eval(config.get('Garmin Screen', 'text_color',fallback="(255,255,255)"))
        self.control_mode = False


    def generate(self, isHorizontal, inputStatus):    
        if (inputStatus is InputStatusEnum.LONG_PRESS):
            self.control_mode = not self.control_mode
        garmin_module = self.modules['garmin']

        if not self.control_mode:
            if (inputStatus is InputStatusEnum.SINGLE_PRESS):
                self.default_actions['toggle_display']()
                self.title_animation_cnt = 0
                self.artist_animation_cnt = 0
            elif (inputStatus is InputStatusEnum.ENCODER_INCREASE):
                self.default_actions['switch_next_app']()
            elif (inputStatus is InputStatusEnum.ENCODER_DECREASE):
                self.default_actions['switch_prev_app']()
        
        frame = Image.new("RGB", (self.canvas_width, self.canvas_height), (0,0,0))
        draw = ImageDraw.Draw(frame)

        response = garmin_module.getLastActivity()
        if response is not None:
            (distance, duration, speed, hr, cadence) = response
            draw.text((0, 0), convertToMiles(distance), medium_blue, font=self.font)

            draw.text((0, 6), roundValues(hr, 1), medium_blue, font=self.font)

            draw.text((0, 12), convertDuration(duration), medium_blue, font=self.font)

            draw.text((0, 18), convertPace(speed), medium_blue, font=self.font)

            draw.text((0, 24), roundValues(cadence, 2), medium_blue, font=self.font)
        
        return frame

def roundValues(num, digits):
    return str(round(num, digits))

def convertToMiles(meters):
    return str(roundValues(meters*0.000621371192, 2))

def convertDuration(seconds):
    hours = math.floor(seconds / 3600)
    minutes = math.floor((seconds / 60) % 60)
    seconds = (seconds % 60)
    return str(hours) + ":" + str(minutes) + "." + str(seconds)

def convertPace(speed): 
    p = (60 / (speed / 0.44704));
    minutes_pace = math.floor(p);
    seconds_pace = p - minutes_pace;
    return str(minutes_pace) + ":" + str(seconds_pace)