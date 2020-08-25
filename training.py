import nltk
import os,glob
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re
import string
from nltk.tokenize import word_tokenize
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.model_selection import train_test_split
from sklearn import svm,naive_bayes
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
import pickle
import time

pd.set_option('display.max_colwidth', None)

current_dir = os.getcwd()
current_dir = current_dir.replace('\\','/')
folder_dataset = current_dir + '/' + 'datatrain/'

def cleaning_data (data_train):
    ##Lower_case
    lower_case = data_train.str.lower()

    ##Number
    num_removal = lower_case.str.replace('\d+', '')

    ##symbol
    sym_removal = num_removal.str.replace('[^\w\s]','')

    ##whitespace
    white_removal = sym_removal.str.strip()

    ##Stemming
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    stem = [stemmer.stem(basic_word) for basic_word in white_removal]

    ##rcsv[6].to_csv(folder_dataset+'okkk_1.csv', index=False)
    ##rcsv = pd.read_csv(folder_dataset+'okkk_1.csv',delimiter=None,sep='>',header=None)

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

rcsv = pd.read_csv(folder_dataset+'train_data.csv',delimiter=None,sep='>',header=None)    #var

print('Cleaning process .....')
new_data = cleaning_data (rcsv[0])

##rcsv[8].to_csv(folder_dataset+'clear_2.csv',index=False)

##inp = pd.read_csv(folder_dataset+'clear.csv',sep='delimiter',header=None)
##print(inp[0])

x_train,x_test,y_train,y_test = train_test_split(new_data[0],rcsv[1],test_size=0.2,random_state=23)
print('x_train: '+str(len(x_train)))
print('y_train: '+str(len(y_train)))
print('x_test: '+str(len(x_test)))
print('y_test: '+str(len(y_test)))

tfidf_vect = TfidfVectorizer()

x_train_tfidf = tfidf_vect.fit_transform(x_train)
x_test_tfidf = tfidf_vect.transform(x_test)

##naive_bayes
##naive = naive_bayes.MultinomialNB()
##naive.fit(x_train_tfidf,y_train)
##
##pred_nb = naive.predict(x_test_tfidf)
##print(str(accuracy_score(pred_nb,y_test)*100))
##
##print(encoder.inverse_transform(pred_nb[-20:]))
##print('\n')
##print(encoder.inverse_transform(y_test[-20:]))

##svm
print("Training process")
svm_meth = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
svm_meth.fit(x_train_tfidf,y_train)

pred_svm = svm_meth.predict(x_test_tfidf)
print('Accuracay: ' + str(accuracy_score(pred_svm,y_test)*100))

print((pred_svm[-5:]))
print('\n')
print((y_test[-5:]))

##print('\n')
##print(x_test[-20:])

##Export model
print('Export Model')
file_model = 'model_data_2'
file_tfdif = 'vectorizer_2'

pickle.dump(svm_meth,open(file_model,'wb'))
pickle.dump(tfidf_vect, open(file_tfdif, 'wb'))
