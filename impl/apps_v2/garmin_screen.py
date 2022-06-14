
import time
from PIL import Image, ImageFont, ImageDraw
from InputStatus import InputStatusEnum
from ast import literal_eval

garmin_blue = (0,77,179)

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
            (distance) = response
            print("distance from screen: ", distance)
            draw.text((0, 0), distance, garmin_blue, font=self.font)
        

        return frame