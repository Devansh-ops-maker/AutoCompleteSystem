from Trie.trie import TrieNode
from db.Cassandra import session
from n_grams.n_gram import suggest_next_words
from model_loader import bigram_count,trigram_count,vocab

trie=TrieNode()
loaded_prefix=set()

def load_prefix_into_trie(prefix):

    if prefix in loaded_prefix:
        return
    
    query="""
         SELECT word FROM prefixes
         WHERE prefix=%s
         LIMIT 10000
      """
    rows=session.execute(query,(prefix,))

    for row in rows:
        trie.insert(row.word)
    
    loaded_prefix.add(prefix)

def get_suggestions(curr_word,prev_word)-> dict:

    curr_word=curr_word.strip().lower()
    prev_word=prev_word.strip().lower()

    if not curr_word:
        suggestions=suggest_next_words(
            prev_word=prev_word or "<s>",
            n_gram_count=bigram_count,
            nplus1_gram_count=trigram_count,
            vocab=vocab,
            top_k=5
        )
        return {"suggestions": suggestions}
    load_prefix_into_trie(curr_word)
    suggestions=trie.starts_with(curr_word)
    return {"suggestions": suggestions}