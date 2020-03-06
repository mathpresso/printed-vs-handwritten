import os
import sys
from math import exp

from PIL import Image

sys.path.append("../ocrd_typegroups_classifier")
from ocrd_typegroups_classifier.typegroups_classifier import TypegroupsClassifier


img = Image.open(input())
tgc = TypegroupsClassifier.load(os.path.join('ocrd_typegroups_classifier', 'models', 'classifier.tgc'))

result = tgc.classify(img, 150, 12, False)
esum = 0
for key in result:
    esum += exp(result[key])
for key in result:
    result[key] = exp(result[key]) / esum
print(result)
