import math
import nltk
import random
import random as rd
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from typing import List

with open('text8',"r") as f:
    text = f.read()
    
def preprocess_pipeline(data) -> 'list':

    words=re.findall(r"[a-zA-Z']+",data.lower())
   
    chunk_size=30

    tokenized=[]

    for i in range(0, len(words), chunk_size):
        chunk=words[i:i+chunk_size]
        tokenized.append(chunk)
    return tokenized

tokenized=preprocess_pipeline(text)

train,test=train_test_split(tokenized,test_size=0.2,random_state=42)
train,val=train_test_split(train,test_size=0.25,random_state=42)

def count_the_words(sentences) -> dict:

    word_count={}

    for sentence in sentences:

        for token in sentence:
            
            if token not in word_count:

                word_count[token]=1

            else:

                word_count[token]+=1
    return word_count

def handling_oov(tokenized_sentences,count_threshold) -> 'list':

    closed_vocab=[]

    word_count=count_the_words(tokenized_sentences)

    for word,count in word_count.items():

        if count>=count_threshold:

            closed_vocab.append(word)
    return closed_vocab

def unk_tokenize(tokenized_sentences,closed_vocab,unknow_token='<unk>') -> List:
    
    vocabulary=set(closed_vocab)

    new_tokenized_sentences=[]

    for sentence in tokenized_sentences:
        
        new_sentence=[]

        for token in sentence:

            if token in vocabulary:

                new_sentence.append(token)

            else:

                new_sentence.append(unknow_token)

        new_tokenized_sentences.append(new_sentence)
    return new_tokenized_sentences

def cleansing(train_data,test_data,count_threshold):

    vocab=handling_oov(train_data,count_threshold)

    train_data=unk_tokenize(train_data,vocab)

    test_data=unk_tokenize(test_data,vocab)

    return train_data,test_data,vocab

min_count_threshold=5

final_train,final_test,vocab=cleansing(train,test,min_count_threshold)

def count_ngrams(data,n,start_token='<s>',end_token='</s>') -> dict:

    n_grams_count={}

    for sentence in data:

        sentence=[start_token]*(n)+sentence+[end_token]

        sentence=tuple(sentence)

        if(n==1):
            m=len(sentence)
        else:
            m=len(sentence)-1
        
        for i in range(m):

            n_gram=sentence[i:i+n]

            if n_gram not in n_grams_count:

                n_grams_count[n_gram]=1

            else:

                n_grams_count[n_gram]+=1
    return n_grams_count
def prob_for_a_single_word(word,previous_n_gram,n_gram_count,nplus1_gram_count,vocab_size,k=1.0) -> float:

    previous_n_gram=tuple(previous_n_gram)

    previous_n_gram_count=n_gram_count[previous_n_gram] if previous_n_gram in n_gram_count else 0

    denom=previous_n_gram_count+k*vocab_size

    nplus1_gram=previous_n_gram+(word,)

    nplus1_gram_count=nplus1_gram_count[nplus1_gram] if nplus1_gram in nplus1_gram_count else 0

    num=nplus1_gram_count+k

    prob=num/denom

    return prob

def probs(previous_n_gram,n_gram_count,nplus1_gram_count,vocabulary,k=1.0) -> dict:

    previous_n_gram=tuple(previous_n_gram)

    vocabulary= vocabulary + ["e","<unk>"]

    vocab_size=len(vocabulary)

    probabilities={}

    for words in vocabulary:

        prob=prob_for_a_single_word(words,previous_n_gram,n_gram_count,nplus1_gram_count,vocab_size, k)

        probabilities[words]=prob
    return probabilities
def suggest_next_words(prev_word,n_gram_count,nplus1_gram_count,top_k,k)-> List:

    prev_word=prev_word.lower()

    if prev_word not in vocab:
        prev_word="<s>"
    
    probs_dict=probs([prev_word],n_gram_count,nplus1_gram_count,vocab,k)

    excluded = {"<s>", "</s>", "<unk>", "e"}
    filtered = {w: p for w, p in probs_dict.items() if w not in excluded}
 
    sorted_words = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
    return [word for word, _ in sorted_words[:top_k]]