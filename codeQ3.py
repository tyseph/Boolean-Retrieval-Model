import os
import numpy as np
import nltk
import re
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize, TweetTokenizer
from nltk.corpus import stopwords
import streamlit as st
import string
from collections import OrderedDict

# call the nltk downloader
# nltk.download()
# print(nltk.corpus.gutenberg.fileids())
# n=1;



porter = PorterStemmer()
set(stopwords.words('english'))
stop_words = set(stopwords.words('english'))

def read_text_file(file_path, id, doc_list):
    global im
    with open(file_path, 'r', encoding="utf8") as f:
        stuff = f.read()
        final_token_list = preprocessing(stuff)
        #print(final_token_list)
        for i in range(len(final_token_list)):
            if final_token_list[i] not in doc_list.keys():
                doc_list[final_token_list[i]] = {}
                doc_list[final_token_list[i]][id] = []
            else:
                doc_list[final_token_list[i]][id] = []
                
        for k in range(len(final_token_list)):
            #print(final_token_list[k])
            doc_list[final_token_list[k]][id].append(k)
    
    return doc_list
        
        

def preprocessing(final_string):
        # Tokenize.
    #print(final_string)
    # for i in range(len(token_list)):
    #     token_list[i] = re.sub(r"[^a-zA-Z0-9]", "", token_list[i])
    tokenizer = TweetTokenizer()
    token_list = tokenizer.tokenize(final_string)
 
    # Remove punctuations.
    table = str.maketrans('', '', '\t')
    token_list = [word.translate(table) for word in token_list]
    for word in token_list:
        word = porter.stem(word)
        word = re.sub(r"[^a-zA-Z0-9]", "", word)
    punctuations = (string.punctuation).replace("'", "")
    trans_table = str.maketrans('', '', punctuations)
    stripped_words = [word.translate(trans_table) for word in token_list]
    token_list = [str for str in stripped_words if str]
 
    # Change to lowercase.
    token_list =[word.lower() for word in token_list]
    return token_list

def And(pi1, pi2):
    answer = []
    i = 0
    j = 0
    while i < len(pi1) and j < len(pi2):
        if pi1[i] == pi2[j]:
            answer.append(pi1[i])
            i = i+1
            j = j+1
        elif pi1[i] < pi2[j]:
            i = i+1
        elif pi1[i] > pi2[j]:
            j = j+1
    return answer


def Or(pi1, pi2):
    answer = []
    i = 0
    j = 0
    if(len(pi1) == 0):
        return pi2
    if(len(pi2) == 0):
        return pi1
    while i < len(pi1) and j < len(pi2):
        if pi1[i] < pi2[j]:
            answer.append(pi1[i])
            i = i+1
        elif pi1[i] == pi2[j]:
            answer.append(pi1[i])
            i = i+1
            j = j+1
        else:
            answer.append(pi2[j])
            j = j+1

    if(i < len(pi1)):
        s = i
        while s < len(pi1):
            answer.append(pi1[s])
            s = s+1
    if(j < len(pi2)):
        s = j
        while s < len(pi2):
            answer.append(pi2[s])
            s = s+1
            
    return answer


def Not(pi):
    i = 0
    answer = []
    if(pi[0] > 1):
        for m in range(1, pi[0]):
            answer.append(m)

    while i < len(pi)-1:
        dif = pi[i+1]-pi[i]
        # print(dif)
        if dif > 1:
            strt = pi[i]
            fin = pi[i+1]
            for d in range(strt+1, fin):
                answer.append(d)
        i = i+1

    x = pi[len(pi)-1]+1
    for i in range(x, 41):
        answer.append(i)
    return answer

def remove_header_footer(final_string):
    new_final_string = ""
    tokens = final_string.split('\n\n')
 
    # Remove tokens[0] and tokens[-1]
    for token in tokens[1:-1]:
        new_final_string += token+" "
    return new_final_string
 


def inputFunction(key, final_list):
    key = key.split(' ')
    post_list = []
    for i in range(len(key)):
        if(key[i] != 'OR' and key[i] != 'NOT' and key[i] != 'AND'):
            key[i] = porter.stem(key[i])
    for i in key:
        if(i != 'OR' and i != 'NOT' and i != 'AND'):
            if(i in final_list):
                post_list.append(final_list[i])
            else:
                print(i, "word not found")
                post_list.append([])

    print("Posting lists here are : ", post_list)
    #st.write(inputProcess(key, post_list))
    print("Final postings: ", inputProcess(key, post_list))
    
def inputProcess(key, post_list):
    k = 0
    for i in range(len(key)):
        if(key[i] == 'AND'):
            if(key[i+1] != 'NOT'):    
                post_list[k + 1] = And(post_list[k], post_list[k + 1])
            else:
                post_list[k + 1] = Not(post_list[k+1])
                post_list[k + 1] = And(post_list[k], post_list[k + 1])
            k = k + 1
        elif(key[i] == 'OR'):
            if(key[i+1] != 'NOT'):
                post_list[k + 1] = Or(post_list[k], post_list[k + 1])
            else:
                post_list[k + 1] = Not(post_list[k+1])
                post_list[k + 1] = Or(post_list[k], post_list[k + 1])
            k = k + 1
    st.header(post_list[k])
    #print(post_list)
    return post_list[k]



#-----FOLDER PATH-----#
path = "D:\\4th year\IR\IR_assignment"
os.chdir(path)

stemming = [['zz' for i in range(2)] for j in range(880)]
doc_list = dict()
im = 0

#-----ITERATING THROUGH ALL FILES-----#
for file in os.listdir():

    #-----CHECK FILE FORMAT-----#
    if file.endswith(".txt"):
        file_path = f"{path}/{file}"
        file = file.split('t')
        file = file[1].split('.')
        file = int(file[0])
        k = 0
        #-----READ FILE FUNCTION-----#
        if k != 1:
            read_text_file(file_path, file, doc_list)
            k = 1

doc_list = OrderedDict(sorted(dict.items(doc_list)))
# for i in doc_list:
#     st.header(i,": ", doc_list[i])
    
st.header(doc_list)
    

#stemming = sorted(stemming, key=lambda x: x[0])

#-----PRINTS THE SORTED INVERTED INDEX-----#
# print("\n Inverted Index \n")
# final_list.popitem()
# for i in final_list:
#     final_list[i].sort()
#     #print(i, ": ", final_list[i], "\n")

# User Inputs

#key = st.text_input("Enter word to search: ")
key = st.text_input("Enter word to search: ")
inputFunction(key, doc_list)