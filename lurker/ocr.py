import numpy as np
from os import listdir
from os.path import isfile, join
from PIL import Image


class BaseOCR:
    def __init__(self, dataset_path):
        items = listdir(dataset_path)
        self.means = {}
        for item in items:
            examples = listdir(join(dataset_path, item))
            mean = np.mean(([np.array(Image.open(join(dataset_path, item, example))) for example in examples]), axis=0)
            self.means[item] = mean

    def predict(self, image):
        results = {}
        for char in self.means:
            results[char] = np.sqrt(np.mean((image - self.means[char]) ** 2))

        return min(results, key=results.get)


class PriceDigitsOCR(BaseOCR):
    def __init__(self, dataset_path, height):
        super().__init__(dataset_path)
        self.height = height

    def predict(self, price_image):
        means = np.mean(price_image, axis=0)
        means_nonz = (means != 0)
        means_oz = (means == 0)

        # Обнаружение пустого пространства по бокам
        padding = means_nonz.argmax(axis=0)

        result = ""
        offset = padding
        while offset < price_image.width - padding:
            # Обнаружение следующего нулевого столбца
            char_end = offset + means_oz[offset:].argmax(axis=0)

            if char_end - offset > 20:
                char_end = offset + (char_end - offset) // 2

            # Пропуск пустого пространства между символами
            if char_end == offset:
                offset += 1
                continue
            # Обрезка символа
            char = price_image.crop((offset, price_image.height // 2 - self.height // 2, char_end,
                                     price_image.height // 2 + self.height // 2))
            # Нормализация размера
            char = self.__expand2square(char, (0))
            # Сохранение в массив символов
            result += super().predict(char)
            # Перемещение курсора в конец текущего символа
            offset = char_end

        price_str = result.replace('q', '').replace('d', '')

        if len(price_str) == 0:
            return 0
        else:
            return int(price_str)

    def __expand2square(self, pil_img, background_color):
        width, height = pil_img.size
        if width == height:
            return pil_img
        elif width > height:
            raise Exception("Character width > height")
        else:
            result = Image.new(pil_img.mode, (height, height), background_color)
            result.paste(pil_img, ((height - width) // 2, 0))
            return result