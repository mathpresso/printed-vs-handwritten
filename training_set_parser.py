import base64
import json
import os
from io import BytesIO
from random import random

from PIL import Image

printed_cnt = 0
hand_cnt = 0
PATH = './lines/training'


def parse_training_set(file, old_printed_cnt, old_hand_cnt):
    try:
        with open(file, 'r') as f:
            d = json.load(f)
            IM = Image.open(BytesIO(base64.b64decode(d['imageData'])))
    except Exception as e:
        print(e)
        return old_printed_cnt, old_hand_cnt
    printed_cnt = 0
    hand_cnt = 0
    printeds = []
    hands = []

    for sp in d['shapes']:
        if 'Word' not in sp['label']:
            continue
        if len(sp) < 2:
            continue
        is_printed = ('Printed' in sp['label'])
        is_hand = ('Hand' in sp['label'])
        ps = sp['points']
        x0, y0 = ps[0]
        x1, y1 = ps[1]

        l, t, r, b = int(min(x0, x1)), int(min(y0, y1)), int(max(x0, x1)), int(max(y0, y1))
        if l >= r or t >= b:
            continue

        # IM.save('image.png')
        if is_printed:
            if int(random() * (2 ** 31)) % 40 == 0:
                new_im = IM.crop((l, t, r, b))
                printeds.append(new_im)
        if is_hand:
            new_im = IM.crop((l, t, r, b))
            hands.append(new_im)

        for im in printeds:
            im.save(f'{PATH}/printed/{old_printed_cnt}.png')
            old_printed_cnt += 1
        for im in hands:
            im.save(f'{PATH}/handwritten/{old_hand_cnt}.png')
            old_hand_cnt += 1
    return old_printed_cnt, old_hand_cnt


for f in os.listdir(f'{PATH}/set'):
    printed_cnt, hand_cnt = parse_training_set(f'{PATH}/set/{f}', printed_cnt, hand_cnt)
    print(printed_cnt, hand_cnt)
