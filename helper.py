import math
import re
from collections import Counter
from itertools import chain
from typing import List, Tuple, Dict
from nltk.corpus import stopwords


def func_tf(docs: List[Tuple[bool, List[str]]]) -> Dict[str, int]:
    content = []
    for d in docs:
        content.extend(d[1])
    return Counter(content)


def func_df(docs: List[Tuple[bool, List[str]]]) -> Dict[str, int]:
    contents = [c for _, c in docs]
    words = Counter(list(chain.from_iterable(contents))).keys()
    df = dict()
    for w in words:
        df[w] = [w in doc for _, doc in docs].count(True)
    return df


def func_tf_idf(tf: Dict[str, int], df: Dict[str, int]) -> Dict[str, float]:
    tf_idf = dict()
    for word in df.keys():
        tf_idf[word] = (tf[word] / len(tf)) * math.log(len(df) / df[word], 10)
    return tf_idf


def preprocess(content: str) -> List[str]:
    return list(
        filter(lambda x: x not in stopwords.words('english'), re.sub('[^0-9a-z]+', ' ', content.lower()).split()))
