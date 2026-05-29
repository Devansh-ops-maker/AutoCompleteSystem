import nltk
from sklearn.model_selection import train_test_split
from n_grams.n_gram import preprocess_pipeline,cleansing,count_ngrams

with open('text8',"r") as f:
    text = f.read()

tokenized=preprocess_pipeline(text)

train,test=train_test_split(tokenized,test_size=0.2,random_state=42)
train,val=train_test_split(train,test_size=0.25,random_state=42)

MIN_COUNT=5

final_train,final_test,vocab=cleansing(train,test,MIN_COUNT)


bigram_count=count_ngrams(final_train,1)
trigram_count=count_ngrams(final_train,2)

all=[]