import win32gui
from PIL import ImageGrab
import pyautogui
from time import sleep

from lurker.nwconfig import NWUI


class GameWindow:
    def __init__(self, window_name) -> None:
        self.hwnd = win32gui.FindWindow(None, window_name)
        if self.hwnd == 0:
            raise Exception(f'Window "{window_name}" is not found!')

        self.rect = win32gui.GetWindowRect(self.hwnd)
        print(self.rect)

    def capture(self):
        return ImageGrab.grab(bbox=self.rect)

    def moveTo(self, x, y):
        pyautogui.moveTo(self.rect[0] + x, self.rect[1] + y)

    def clickTo(self, x, y):
        pyautogui.moveTo(self.rect[0] + x, self.rect[1] + y)
        sleep(0.1)
        pyautogui.click()

    def write(self, text):
        pyautogui.write(text, interval=0.1)

    def press(self, key):
        pyautogui.press(key)

    def hotkey(self, key1, key2):
        pyautogui.hotkey(key1, key2)

    def hold_key(self, key, duration):
        pyautogui.keyDown(key)
        sleep(duration)
        pyautogui.keyUp(key)

    def tp_search(self, text):
        self.clickTo(NWUI.search_clear_btn[0], NWUI.search_clear_btn[1])
        self.clickTo(NWUI.search_input[0], NWUI.search_input[1])
        self.write(text)
        self.clickTo(NWUI.search_result[0], NWUI.search_result[1])

    def anti_afk(self):
        self.press('esc')
        self.hold_key('s', 0.5)
        self.hold_key('w', 0.5)
        self.press('e')
        sleep(1)