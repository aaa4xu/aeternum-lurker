from lurker.capture import Capture
from lurker.game import GameWindow
from time import time, sleep
from lurker.nwconfig import NWUI
from lurker.processors import BuyOrdersProcessor
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

        try:
            tp_image = capture.screenshot()
            orders = processor.process(bytes)
            for x in orders:
                print(x)

            # tp_image = game.capture()
            # price_image = price_ocr.crop_tpost(tp_image)
            # price_image.save(f"screens/{timestamp}/{item['name']}-tp.png")
            # prices = [price_ocr.process(price_image)]
            #
            # with open(f"screens/{timestamp}/{item['name']}-ocr.txt", "w") as text_file:
            #     text_file.writelines([str(x) for x in prices])
            #
            # # prices = list((map(lambda x: int(x), filter(lambda x: len(x) > 0, prices))))
            # print(f"{item['name']}: {str(prices[0] / 100)}")
            #
            # index = 0
            # requests.post('http://192.168.1.90:3401/api/price', json={
            #     "item": item['name'],
            #     "index": index,
            #     "price": prices[index],
            #     "timestamp": timestamp
            # })
        except ValueError:
            print(f"{item['name']}: ERROR: OCR is failed")
        except requests.exceptions.RequestException as e:
            print(f"{item['name']}: ERROR: API Request failed")
        except IndexError:
            print(f"{item['name']}: list index out of range")

    game.anti_afk()
    sleep_duration = 14 * 60 - (time() - timestamp)
    print(f'Sleep for {sleep_duration}sec')
    sleep(sleep_duration)