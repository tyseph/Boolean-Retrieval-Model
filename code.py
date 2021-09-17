import os
import numpy as np
import nltk
import re
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# call the nltk downloader
# nltk.download()
# print(nltk.corpus.gutenberg.fileids())
# n=1;

porter = PorterStemmer()
set(stopwords.words('english'))
stop_words = set(stopwords.words('english'))


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

    if(len(pi1) < len(pi2)):
        s = len(pi1)
        while s < len(pi2):
            answer.append(pi2[s])
            s = s+1
    elif(len(pi1) > len(pi2)):
        s = len(pi2)
        while s < len(pi1):
            answer.append(pi1[s])
            s = s+1
    else:
        answer.append(pi1[i])

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
    return post_list[k]
    
            
    # for i in post_list.keys():
    #     print(i)
    #     print("Not of ", key[0], "is: ", Not(post_list[i]))
    #     print("And of ", key[0], " and ", key[2], "is: ", And(post_list[i], post_list[i + 1]))
    #     print("Or of ", key[0], " and ", key[2], "is: ", Or(post_list[i], post_list[i + 1]))
    #print(type(x), type(post_list[0]))


def read_text_file(file_path, id):
    global im
    with open(file_path, 'r', encoding="utf8") as f:
        for line in f:
            #-----READ EACH WORD-----#
            for word in line.split():
               #-----REMOVING STOP WORDS-----#
                if word not in stop_words:
                    word = re.sub(r"[^a-zA-Z0-9]", "", word)
                    #-----STEMMING-----#
                    if(word.isalnum()):
                        word = porter.stem(word)
                        stemming[im][0] = word
                        stemming[im][1] = id
                        im = im+1


#-----FOLDER PATH-----#
path = "D:\\4th year\IR\IR_assignment"
os.chdir(path)

stemming = [['zz' for i in range(2)] for j in range(880)]
post_li = []

im = 0

#-----ITERATING THROUGH ALL FILES-----#
for file in os.listdir():

    #-----CHECK FILE FORMAT-----#
    if file.endswith(".txt"):
        file_path = f"{path}/{file}"
        file = file.split('t')
        file = file[1].split('.')
        file = int(file[0])

        #-----READ FILE FUNCTION-----#
        read_text_file(file_path, file)

stemming = sorted(stemming, key=lambda x: x[0])

k = 0
linked_list_data = dict()

for word in range(0, 880):
    if (stemming[word][0]) not in linked_list_data.values():
        linked_list_data[k] = stemming[word][0]
        k = k+1

final_list = {}
vocab = []

for i in linked_list_data.values():
    temp_list = []
    for j in range(len(stemming)):
        if (i == stemming[j][0]) and (stemming[j][1] not in temp_list):
            temp_list.append(stemming[j][1])
        final_list[i] = temp_list

#-----PRINTS THE SORTED INVERTED INDEX-----#
print("\n Inverted Index \n")
for i in final_list:
    final_list[i].sort()
    print(i, ": ", final_list[i], "\n")

# User Inputs

key = input("Enter word to search: ")
inputFunction(key, final_list)
