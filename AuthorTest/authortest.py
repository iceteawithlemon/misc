#Python 3.2
#28/07/13
#Author recognition (unfinished)
import re

#declaring variables
word_count=[]
count=0
#Get file title. File should be ANSCII .txt
file=input("File? ")+".txt"
#Opening file and copying contents to "text"
in_file = open(file, "rt")
text = in_file.read()
in_file.close()
#Removing punctuation and symbols, converting all to lowercase and splitting string into a list of words
text=re.sub('[^A-Za-z ]+', '', text).lower().split()

#Counting words: this is still a bit buggy, as adds a new entry for each word regardless of whether it already exists
for word in text:
#this line counts the total words in the text
    count+=1
    for tup in word_count:
        if tup[0] == word:
            tup[1]+=1
            break
    word_count.append([word, 1])

#Sorts list of words by their count, and keeps only the 100 most common
word_count=sorted(word_count, key=lambda x: x[1], reverse=True)
del word_count[100:]
word_percent=word_count
#Displaying words & percentage of occurence in descending order
for i in word_percent:
    i[1]=round((i[1]/count)*100, 2)
    print("Word: ", i[0], " Percentage: ", i[1], "%") 


            
    



