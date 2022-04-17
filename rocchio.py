from collections import Counter
from dataclasses import dataclass
from itertools import chain
from typing import List, Tuple

from config import alpha, gamma, beta
from helper import func_tf, func_df, preprocess, func_tf_idf


@dataclass
class Page:
    title: str
    url: str
    description: str
    related: bool = False


class Rocchio:
    def __init__(self):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def update(self, pages: List[Page], query: List[str]) -> Tuple[List[str], List[str]]:
        docs = [(p.related, preprocess(f'{p.title} {p.description}')) for p in
                pages]
        docs_r = list(filter(lambda d: d[0], docs))
        docs_nr = list(filter(lambda d: not d[0], docs))

        tf_r = func_tf(docs_r)
        tf_nr = func_tf(docs_nr)
        df_r = func_df(docs_r)
        df_nr = func_df(docs_nr)
        tf_idf_r = func_tf_idf(tf_r, df_r)
        tf_idf_nr = func_tf_idf(tf_nr, df_nr)

        all_contents = [c for _, c in docs]
        all_words = dict(Counter(list(chain.from_iterable(all_contents)))).keys()
        vec = dict().fromkeys(all_words, 0)

        for k in tf_idf_r:
            vec[k] += self.beta * tf_idf_r[k]/len(docs_r)
        for k in tf_idf_nr:
            vec[k] -= self.gamma * tf_idf_nr[k]/len(docs_nr)

        candidates_with_score = sorted(vec.items(), key=lambda x: x[1], reverse=True)
        candidates = []
        for i in range(min(len(query)+2, len(candidates_with_score))):
            if candidates_with_score[i][1] > 0:
                candidates.append(candidates_with_score[i][0])
        excluded = [q for q in query if q not in candidates]
        new_query = [*excluded, *candidates[:len(candidates)-len(excluded)]]
        
        augment = [w for w in new_query if w not in query]
            
        return augment, new_query
