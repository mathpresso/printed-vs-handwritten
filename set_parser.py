import base64
import json
import os
from io import BytesIO
from random import random

from PIL import Image

printed_cnt = 0
hand_cnt = 0
PATH = '/Users/nutella/printed-vs-handwritten/lines/training'


def parse_training_set(file, old_printed_cnt, old_hand_cnt):
    try:
        with open(file, 'r') as f:
            d = json.load(f)
            IM = Image.open(BytesIO(base64.b64decode(d['imageData'])))
    except Exception as e:
        print(e)
        return old_printed_cnt, old_hand_cnt
    printeds = []
    hands = []

    for sp in d['shapes']:
        if 'Word' not in sp['label']:
            continue
        is_printed = ('Printed' in sp['label'])
        is_hand = ('Hand' in sp['label'])
        ps = sp['points']
        if len(ps) < 2:
            continue
        x0, y0 = ps[0]
        x1, y1 = ps[1]

        l, t, r, b = int(min(x0, x1)), int(min(y0, y1)), int(max(x0, x1)), int(max(y0, y1))
        if l >= r or t >= b:
            continue

        # IM.save('image.png')
        if is_printed:
            if int(random() * (2 ** 31)) % 15 == 0:
                new_im = IM.crop((l, t, r, b))
                new_im.save(f'{PATH}/printed/{old_printed_cnt}.png')
                old_printed_cnt += 1
        if is_hand:
            new_im = IM.crop((l, t, r, b))
            new_im.save(f'{PATH}/handwritten/{old_hand_cnt}.png')
            old_hand_cnt += 1
    return old_printed_cnt, old_hand_cnt


for f in os.listdir(f'/Users/nutella/Desktop/set'):
    printed_cnt, hand_cnt = parse_training_set(f'/Users/nutella/Desktop/set/{f}', printed_cnt, hand_cnt)
    print(printed_cnt, hand_cnt)
    if printed_cnt > 3000 and hand_cnt > 3000:
        break
