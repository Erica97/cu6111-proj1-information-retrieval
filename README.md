# cu-e6111-proj1

## Team
Rong Bai, rb3512

Jiawen Li, jl6121

## File list
```
.
├── proj1.tar.gz
│ ├── config.py         # configuration of Google API key, search engine ID and rocchio parameters
│ ├── helper.py         # helper functions
│ ├── main.py           # main entry
│ └── rocchio.py        # rocchio algorithm
├── README.md
└── transcripts.txt     # tests results for "per se", "brin" and "cases"
```
## How to run
### dependencies
```bash
sudo apt install python3.7
pip3 install google-api-python-client
pip3 install nltk
(echo "import nltk"; echo "nltk.download('stopwords')") | python3.7 
```
### run
If query is separated by space, please use double quotes to wrap it.
```bash
python3.7 main <google_api_key> <search_engine_id> <presision> <query>
```
## Design
### Internal Design

In `config.py`, we store the parameters used by the Rocchio algorithm.

In `main.py`, we use Google API to search the query, show the search results, get feedback from users (Y/N), and use method in `rocchio.py` to update the query. The program repeat the process until the query results reach the targeted precision @ 10, or there's not enough information to update query when the precision is 0.

In `helper.py`, we preprocess the query by removing stopwords, then calculate term frequency and document frequency, as well as the TF-IDF for each word in query.

In `Rocchio.py`, we use the user feedback(Y/N), title and description for each result page and use Rocchio algorithm to augment and reorder the query for next iteration.

## External Library
We use `nltk.corpus` to get stopwords.

## Query-modification method
### Preprocess
We split documents into alphanumeric words and remove stopwords provided by `nltk`. We treat title and description of each  search result as a document.

### Get New Keywords
We use a varied Rocchio algorithm to get the augmented query.

$\vec{q}_{t+1} = \alpha \vec{q}_t + \cfrac{\beta}{\text{R}}\sum_{d \in \text{R}}\vec{d} - \cfrac{\gamma}{|\text{NR}|}\sum_{d \in \text{NR}}\vec{d}$

We use tf-idf value to represent word vector.

- Compute term frequence for relevant and non-relevant documents, get $\text{tf}(\text{R})$ and $\text{tf}(\text{NR})$.
- Comute document frequence among relevant and non-relevant documents, get $\text{df}(\text{R})$ and $\text{df}(\text{NR})$.
- Use $\text{tf-idf}(w) = \text{tf}(w) * \log_{10} \cfrac{|D|}{\text{df}(w)}$ to compute $\text{tf-idf}$ of relevant and non-relevant documents.

Then set the parameters as: $\alpha=0, \beta=0.9, \gamma=0.1$. After compute $\vec{q}_{t+1}$, sort it by desending scores and take all keywords with positive score as candidates.

### Reorder

The candidates got by previous step are already reordered. To ensure the original query words are still included, a scan is required. Firstly take topmost $len(\vec{q})+2$ elements as new keywords. If original query are not included, then continue to scan, add old query to list and pop the element with smallest score out. 

## Credentials
Search Engine JSON API Key: `AIzaSyAA6dhVPPVCI-JfqTgWw51WnnrSbbIyaa8`

Search Engine ID: `d8910217929b314ff`
