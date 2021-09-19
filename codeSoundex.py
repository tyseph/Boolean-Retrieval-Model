import os
import numpy as np
import nltk
import re
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import streamlit as st
# call the nltk downloader
# nltk.download()
# print(nltk.corpus.gutenberg.fileids())
# n=1;

porter = PorterStemmer()
set(stopwords.words('english'))
stop_words = set(stopwords.words('english'))

def soundex(query: str):
    """
    https://en.wikipedia.org/wiki/Soundex
    :param query:
    :return:
    """

    # Step 0: Clean up the query string
    query = query.lower()
    letters = [char for char in query if char.isalpha()]
    #print(query, letters)

    # Step 1: Save the first letter. Remove all occurrences of a, e, i, o, u, y, h, w.

    # If query contains only 1 letter, return query+"000" (Refer step 5)
    if len(query) == 1:
        return query + "000"

    to_remove = ('a', 'e', 'i', 'o', 'u', 'y', 'h', 'w')

    first_letter = letters[0]
    letters = letters[1:]
    letters = [char for char in letters if char not in to_remove]

    if len(letters) == 0:
        return first_letter + "000"

    # Step 2: Replace all consonants (include the first letter) with digits according to rules

    to_replace = {('b', 'f', 'p', 'v'): 1, ('c', 'g', 'j', 'k', 'q', 's', 'x', 'z'): 2,
                  ('d', 't'): 3, ('l',): 4, ('m', 'n'): 5, ('r',): 6}

    first_letter = [value if first_letter else first_letter for group, value in to_replace.items()
                    if first_letter in group]
    letters = [value if char else char
               for char in letters
               for group, value in to_replace.items()
               if char in group]

    # Step 3: Replace all adjacent same digits with one digit.
    letters = [char for ind, char in enumerate(letters)
               if (ind == len(letters) - 1 or (ind+1 < len(letters) and char != letters[ind+1]))]

    # Step 4: If the saved letter’s digit is the same the resulting first digit, remove the digit (keep the letter)
    if first_letter == letters[0]:
        letters[0] = query[0]
    else:
        letters.insert(0, query[0])

    # Step 5: Append 3 zeros if result contains less than 3 digits.
    # Remove all except first letter and 3 digits after it.

    first_letter = letters[0]
    letters = letters[1:]

    letters = [char for char in letters if isinstance(char, int)][0:3]

    while len(letters) < 3:
        letters.append(0)

    letters.insert(0, first_letter)

    string = "".join([str(l) for l in letters])

    #print(string)

    return string

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
    #print(key)
    post_list = []
    for i in range(len(key)):
        if(key[i] != 'OR' and key[i] != 'NOT' and key[i] != 'AND'):
            if(key[i].isalnum() and key[i].isnumeric()==False):
                key[i] = soundex(key[i])
            #key[i] = porter.stem(key[i])
    for i in key:
        if(i != 'OR' and i != 'NOT' and i != 'AND'):
            if(i in final_list):
                post_list.append(final_list[i])
            else:
                print(i, "word not found")
                post_list.append([])

    print("Posting lists here are : ", post_list)
    print("Final postings: ", inputProcess(key, post_list))
    var = inputProcess(key, post_list)
    #st.header(var)
    
def inputProcess(key, post_list):
    k = 0
    if("AND" in key or "OR" in key or "NOT" in key):
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
    else:
        for i in range(len(key)-1):
            post_list[i+1]=And(post_list[i], post_list[i + 1])
        return post_list[i+1]

def read_text_file(file_path, id):
    global im
    with open(file_path, 'r', encoding="utf8") as f:
        # print(f.readlines(),"\n")
        for line in f:
            # reading each word
            for word in line.split():
               # displaying the words
               # print(word, "\t")
                if word not in stop_words:
                    word = re.sub(r"[^a-zA-Z0-9]", "", word)
                    if(word.isnumeric()):
                        stemming[im][0] = word
                        stemming[im][1] = id
                        # print(stemming)
                        im = im+1
                    if(word.isalnum() and word.isnumeric()==False):
                        #word = porter.stem(word)
                        word = soundex(word)
                        # stemming[im].append(word)
                        # stemming[im].append(id)
                        stemming[im][0] = word
                        stemming[im][1] = id
                        # print(stemming)
                        im = im+1
                    #list.append(" ")
                # print(list)
#-----FOLDER PATH-----#
path = "D:\\4th year\IR\IR_assignment"
os.chdir(path)

#nline=[]
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
final_list.popitem()
for i in final_list:
    final_list[i].sort()
    print(i, ": ", final_list[i], "\n")

# User Inputs

key = input("Enter word to search: ")
inputFunction(key, final_list)