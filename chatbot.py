import nltk
import numpy as np
import tflearn
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import random
import tensorflow
import json

with open("intents.json") as file:
    data = json.load(file)

word = []
labels = []
docs = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])

    if intent["tag"] not in labels:
        labels.append(intent["tag"])
words = [stemmer.stem(w.lower()) for w in words if  w not in "?"]
words = sorted(list(set(words)))

labels = sorted(labels)
trainig = []
output = []

out_empty = [0 for _  in  range(len(labels))]
for x,doc in enumerate(docs_x):
    bag =[]
    wrds = [stemmer.stem(w) for w in doc]

    for w in words:
        if  w in wrds:
            bag.append(1)
        else:
            bag.append(0)
    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] =1

    trainig.append(bag)
    output.append(output_row)

trainig= numpy.array(trainig)
output = numpy.array(output)

tensorflow.reset_default_graph()

net= tflearn.input_data(shape=[None, len(trainig[0])])
net=tflearn.fully_connected(net,8)
net=tflearn.fully_connected(net,8)
net= tflearn.fully_connected(net, len(output[0]),activation="softmax")
net= tflearn.regression(net)
model = tflearn.DNN(net)
model.fit(trainig,output,n_epoch=1000, batch_size=8, show_metric=True)
model.save("nodel.tflearn")