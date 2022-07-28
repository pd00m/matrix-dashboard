import queue
import socket
import sys, os, time, copy, inspect
from InputStatus import InputStatusEnum
from PIL import Image, ImageFont, ImageDraw

washed_out_navy = (109, 104, 117)
white = (230, 255, 255)


def main():
    print("Starting....")
    currentdir = os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe()))
    )
    font = ImageFont.truetype("fonts/tiny.otf", 5)
    parentdir = os.path.dirname(currentdir)
    sys.path.append(parentdir + "/rpi-rgb-led-matrix/bindings/python")
    from rgbmatrix import RGBMatrix, RGBMatrixOptions

    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.chain_length = 1
    options.parallel = 1
    options.brightness = 100
    options.pixel_mapper_config = "U-mapper;Rotate:180"
    options.gpio_slowdown = 1
    options.pwm_lsb_nanoseconds = 80
    options.limit_refresh_rate_hz = 150
    options.hardware_mapping = "regular"  # If you have an Adafruit HAT: 'adafruit-hat'
    options.drop_privileges = False
    matrix = RGBMatrix(options=options)
    print(parentdir + "/rpi-rgb-led-matrix/bindings/python")
    frame = Image.new("RGB", (64, 32), (0, 0, 0))
    matrix.SetImage(frame)
    draw = ImageDraw.Draw(frame)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    draw.text(
        (8, 0),
        "Test",
        white,
        font=font,
    )
    draw.text(
        (0, 0),
        ip_address,
        white,
        font=font,
    )
    print("Ip address: ", ip_address)
    while True:

        time.sleep(0.5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted with Ctrl-C")
        sys.exit(0)
