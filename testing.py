import nltk
import os,glob, sys
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re
import string
from nltk.tokenize import word_tokenize
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn import svm,naive_bayes
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
pd.set_option('display.max_colwidth', None)

current_dir = os.getcwd()
current_dir = current_dir.replace('\\','/')

def cleaning_data(data_test):  
    ##Lower_case
    lower_case = data_test.str.lower()

    ##Number removal
    num_removal = lower_case.str.replace('\d+', '')

    ##symbol removal
    sym_removal = num_removal.str.replace('[^\w\s]','')

    ##whitespace removal
    white_removal = sym_removal.str.strip()

    ##Stemming
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    stem = [stemmer.stem(basic_word) for basic_word in white_removal]

    ##tokenization
    token = [word_tokenize(text)for text in stem]

    ##stopword
    liststopword = set (stopwords.words('indonesian'))

    kl = []
    for text_stop in token:
      new = []
      for x in text_stop:
        if x not in liststopword: 
          new.append(x)

      kl.append(str(new))

    cleaned_data = pd.DataFrame(kl)

    return cleaned_data

model_fold = current_dir + '/' + 'model_data'
vector_fold = current_dir + '/' + 'vectorizer'
folder_datatest = current_dir + '/' + 'datatest/'

model = pickle.load(open(model_fold, 'rb'))
vector = pickle.load(open(vector_fold, 'rb'))

csv_test = pd.read_csv(folder_datatest+'test_data.csv',delimiter=None,sep='>',header=None,encoding='utf-8')

print('Cleaning process .....')
new_data = cleaning_data(csv_test[0])

print('Predict data .....')
testing = vector.transform(new_data[0])
pred_svm = model.predict(testing)
print((pred_svm[:20]))

csv_test['Predict'] = pred_svm

try:
    csv_test.to_csv('Predict.csv',header=None,sep='>',index=None)
    print('Done')
except:
    print('Close File')
    sys.exit()
