import sys
sys.path.append('../')
from rag.query_rag import retrieve_chunks

res = retrieve_chunks("How does water behave around stones?")
for r in res:
    print(r['topic'], "score:", r['score'])
    print(r['text'][:240].replace('\n',' '), "\n---\n")