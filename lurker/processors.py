from PIL import Image
from lurker.nwconfig import NWUI
from lurker.ocr import DigitsOCR, BaseOCR


class BuyOrdersProcessor:
    def __init__(self):
        self.price_ocr = DigitsOCR("datasets/price-digits", 40, 20)
        self.amount_ocr = DigitsOCR("datasets/amount-digits", 40, 20)
        self.towns_ocr = BaseOCR("datasets/towns")

    def process(self, image):
        orders = [image.crop((0, x * NWUI.order_height, image.width, (x + 1) * NWUI.order_height)) for x in range(NWUI.orders_per_page)]
        orders = [{ 'town': self.__predict_town(x), 'price': self.__predict_price(x), 'amount': self.__predict_amount(x) } for x in orders]
        return [order for order in orders if order['price'] > 0]

    def debug_save_towns(self, image_bytes):
        image = Image.fromarray(image_bytes, 'L')
        orders = [image.crop((0, x * NWUI.order_height, image.width, (x + 1) * NWUI.order_height)) for x in
                  range(NWUI.orders_per_page)]

        for x in range(len(orders)):
            self.__town_image(orders[x]).save(f"debug-{x}.png")

    def __town_image(self, order_image):
        return order_image.crop((NWUI.order_town_offset, 0, order_image.width, order_image.height))

    def __predict_town(self, order_image):
        return self.towns_ocr.predict(self.__town_image(order_image))

    def __predict_price(self, order_image):
        price_image = order_image.crop((
            NWUI.price_x - NWUI.price_width // 2,
            0,
            NWUI.price_x + NWUI.price_width // 2,
            order_image.height
        ))
        return self.price_ocr.predict(price_image)

    def __predict_amount(self, order_image):
        amount_image = order_image.crop((
            NWUI.amount_x - NWUI.amount_width // 2,
            0,
            NWUI.amount_x + NWUI.amount_width // 2,
            order_image.height
        ))
        return self.amount_ocr.predict(amount_image)