#!/usr/bin/env python

import sys
from typing import List

from googleapiclient.discovery import build
from rocchio import Rocchio, Page


def main(api_key, engine_id, target_precision, query: List[str]):
    precision = 0
    pages = []

    while True:
        print('Parameters:')
        print('Client key  =', api_key)
        print('Engine key  =', engine_id)
        print(f'Query       = {" ".join(query)}')
        print('Precision   =', target_precision)
        relevant_count = 0
        service = build("customsearch", "v1", developerKey=api_key)
        rsp = service.cse().list(
            q=' '.join(query),
            cx=engine_id,
        ).execute()

        print('Google Search Results:')
        print('======================')

        if 'items' in rsp:
            pages = [Page(title=res['title'], url=res['link'], description=res['snippet']) for res in rsp['items']]
            for idx, p in enumerate(pages):
                print('Result', idx+1)
                print(f'[\nURL: {p.url}\nTitle: {p.title}\nSummary: {p.description}\n]\n')

                is_relevant = ''
                while is_relevant.strip() not in ['Y', 'N']:
                    is_relevant = input('Relevant (Y/N)? ')

                if is_relevant == 'Y':
                    relevant_count += 1
                    p.related = True
                else:
                    p.related = False
                precision = relevant_count / len(pages)
        else:
            print('no results')

        print('======================')
        print('FEEDBACK SUMMARY')
        print(f'Query       = {" ".join(query)}')
        print('Precision: ', precision)

        if precision == 0 or len(pages) < 10:
            print('can not augment query')
            break
        elif precision < target_precision:
            print('Still below the desired precision of', target_precision)
            print('Indexing results ....')
            augment, query = Rocchio().update(pages, query)

            print('Augmenting by:', ''.join(augment))
            print(' ')
        else:
            print('Desired precision reached, done')
            break


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('usage: main <google_api_key> <search_engine_id> <precision> <query>')
        exit(1)
    google_api_key = sys.argv[1]
    engine_id = sys.argv[2]
    precis = float(sys.argv[3])
    q = sys.argv[4]

    main(google_api_key, engine_id, precis, q.split())
