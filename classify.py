import os
import json
import sys
from math import exp

from PIL import Image

sys.path.append("../ocrd_typegroups_classifier")
from ocrd_typegroups_classifier.typegroups_classifier import TypegroupsClassifier

PATH = sys.argv[1]
ans = PATH.split('/')[-2]
img = Image.open(PATH)
tgc = TypegroupsClassifier.load(os.path.join('ocrd_typegroups_classifier', 'models', 'classifier.tgc'))

with open('results.txt', 'a') as f:
    result = tgc.classify(img, 150, 10, False)
    esum = 0
    for key in result:
        esum += exp(result[key])
    for key in result:
        result[key] = exp(result[key]) / esum

    if result[ans] < 0.5:
        f.write(sys.argv[1] + '\n')

