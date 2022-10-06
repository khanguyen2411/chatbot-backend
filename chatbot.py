import random
import nltk
import pickle
import numpy as np
import json
from nltk.stem import WordNetLemmatizer
import pandas as pd
from tensorflow.python.keras.models import load_model


lematizer = WordNetLemmatizer()
with open('../intent/intents.json', encoding="utf8") as json_data:
    intents = json.load(json_data)


words = pickle.load(open('../words.pkl', 'rb'))
classes = pickle.load(open('../classes.pkl', 'rb'))
model = load_model('../chatbot.h5')


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lematizer.lemmatize(word) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list


def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intent = intents_json['intents']
    for i in list_of_intent:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result


def answer(message):
    ints = predict_class(message)
    res = get_response(ints, intents)
    return res

# while True:
#     message = input()
#     ints = predict_class(message)
#     res = get_response(ints, intents)
#     print(res)

