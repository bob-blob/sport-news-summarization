from collections import Counter
from operator import itemgetter
import math

def cosine_similarity(s1, s2):
    vector1 = Counter(s1.split())
    vector2 = Counter(s2.split())

    intersection = set(vector1.keys()) & set(vector2.keys())
    numerator = sum([vector1[x]] * vector2[x] for x in intersection)

    sum1 = sum([vector1[x]**2 for x in vector1.keys()])
    sum2 = sum([vector2[x]**2 for x in vector2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator