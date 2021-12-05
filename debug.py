from time import sleep
from PIL import Image
import numpy as np

from lurker.capture import Capture, DebugCapture
from lurker.nwconfig import NWUI
from lurker.processors import BuyOrdersProcessor

if __name__ == '__main__':
    screenshot = np.array(Image.open("storage/NewWorld_3oNeEesJ7o.jpg"))
    capture = DebugCapture(NWUI.orders_rect, screenshot)
    processor = BuyOrdersProcessor()
    bytes = capture.screenshot()
    images = processor.process(bytes)

    for t in images:
        print(t)