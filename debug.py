from time import sleep
from PIL import Image
import numpy as np

from lurker.capture import Capture, DebugCapture
from lurker.nwconfig import NWUI
from lurker.processors import BuyOrdersProcessor

if __name__ == '__main__':
    screenshot = np.array(Image.open("storage/110.png"))
    capture = DebugCapture(NWUI.orders_rect, screenshot)
    processor = BuyOrdersProcessor()
    images = processor.process(Image.fromarray(capture.screenshot(), 'L'))

    for t in images:
        print(t)