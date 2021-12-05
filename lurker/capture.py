from time import sleep
import d3dshot
import numpy as np

# Классы для захвата изображения из игры

class BaseCapture:
    def __init__(self, rect, threshold=100):
        self._threshold = threshold
        self._rect = rect

    def _process_image(self, screenshot):
        # Обрезаем картинку + оставляем только красный канал
        grayscale = screenshot[self._rect[1]:self._rect[3], self._rect[0]:self._rect[2], :1]
        grayscale = np.reshape(grayscale, grayscale.shape[:2])
        # Накладываем фильтр по яркости пикселей
        idx = grayscale[:, :] > self._threshold
        grayscale[:, :] = 0
        grayscale[idx] = 255

        return grayscale


class Capture(BaseCapture):
    def __init__(self, rect, threshold=100):
        super().__init__(rect, threshold)
        sleep(2)
        self._instance = d3dshot.create(capture_output="numpy")

    def screenshot(self):
        return self._process_image(self._instance.screenshot())


class DebugCapture(BaseCapture):
    def __init__(self, rect, screenshot, threshold=100):
        super().__init__(rect, threshold)
        self._screenshot = screenshot

    def screenshot(self):
        return self._process_image(self._screenshot)
