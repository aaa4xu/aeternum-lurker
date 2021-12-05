from lurker.capture import Capture
from lurker.game import GameWindow
from time import time, sleep
from lurker.nwconfig import NWUI
from lurker.processors import BuyOrdersProcessor
from PIL import Image
import requests
import os

game = GameWindow("New World")
capture = Capture(NWUI.orders_rect)
processor = BuyOrdersProcessor()

if __name__ == '__main__':
    sleep(5)
    game.anti_afk()
    timestamp = int(time())
    os.makedirs(f'screens/{timestamp}')

    resp = requests.get(url='http://192.168.1.90:3401/api/watchlist')
    items = resp.json()

    for item in items:
        game.tp_search(item['search_query'])
        sleep(2)

        tp_image = Image.fromarray(capture.screenshot(), 'L')
        tp_image.save(f'screens/{timestamp}/{item["name"]}.png')

        orders = processor.process(tp_image)

        requests.post('http://192.168.1.90:3401/api/v2/prices', json={
            "item": item['name'],
            "orders": orders,
            "timestamp": timestamp
        })

        # try:
        #     orders = processor.process(tp_image)
        #
        #     requests.post('http://192.168.1.90:3401/api/v2/prices', json={
        #         "item": item['name'],
        #         "orders": orders,
        #         "timestamp": timestamp
        #     })
        # except ValueError:
        #     print(f"{timestamp} {item['name']}: ERROR: OCR is failed")
        # except requests.exceptions.RequestException:
        #     print(f"{timestamp} {item['name']}: ERROR: API request failed")

    game.anti_afk()
    sleep_duration = 9 * 60 - (time() - timestamp)
    print(f'Sleep for {sleep_duration}sec')
    sleep(sleep_duration)
