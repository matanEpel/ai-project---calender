import os
import pickle

import keras
import numpy as np
import pandas as pd
from keras import utils
from keras.layers import Dense, Activation, Dropout
from keras.models import Sequential
from keras.preprocessing import text
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


class NN:

    def __init__(self):
        if os.path.exists('saved_model'):
            self.model = keras.models.load_model('saved_model')
            # loading
            with open('tokenizer.pickle', 'rb') as handle:
                self.tokenize = pickle.load(handle)
            with open('encoder.pickle', 'rb') as handle:
                self.encoder = pickle.load(handle)
        else:
            self.model = None
            self.tokenize = None
            self.encoder = None
        self.max_words = 1000
        self.df = pd.read_excel('generated_data.xlsx')

    def has_model(self):
        return self.model is not None

    def build_model(self):
        # Build the self.model
        self.model = Sequential()
        self.model.add(Dense(512, input_shape=(self.max_words,)))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(self.num_classes))
        self.model.add(Activation('softmax'))

        self.model.compile(loss='categorical_crossentropy',
                           optimizer='adam',
                           metrics=['accuracy'])

    def train_and_evaluate(self):
        self.df.drop(columns=['LABEL'])
        self.df = self.df[pd.notnull(self.df['TITLE'])]
        my_tags = ['TASK', 'MEETING', 'MUST_BE_IN']

        X = self.df['TITLE']
        y = self.df['TYPE']
        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8)

        self.tokenize = text.Tokenizer(num_words=self.max_words, char_level=False)
        self.tokenize.fit_on_texts(X_train)  # only fit on train

        x_train = self.tokenize.texts_to_matrix(X_train)
        x_test = self.tokenize.texts_to_matrix(X_test)

        self.encoder = LabelEncoder()
        self.encoder.fit(y_train)
        y_train = self.encoder.transform(y_train)
        y_test = self.encoder.transform(y_test)

        self.num_classes = np.max(y_train) + 1
        y_train = utils.np_utils.to_categorical(y_train, self.num_classes)
        y_test = utils.np_utils.to_categorical(y_test, self.num_classes)

        self.build_model()
        batch_size = 32
        epochs = 2
        history = self.model.fit(x_train, y_train,
                                 batch_size=batch_size,
                                 epochs=epochs,
                                 verbose=1,
                                 validation_split=0.1)
        self.model.save('saved_model')
        with open('tokenizer.pickle', 'wb') as handle:
            pickle.dump(self.tokenize, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open('encoder.pickle', 'wb') as handle:
            pickle.dump(self.encoder, handle, protocol=pickle.HIGHEST_PROTOCOL)

        score = self.model.evaluate(x_test, y_test,
                                    batch_size=batch_size, verbose=1)
        print('Test accuracy:', score[1])

    def classify(self, str):
        self.num_classes = 3
        x_pred = self.tokenize.texts_to_matrix([str])

        y_pred = utils.np_utils.to_categorical(self.encoder.transform(["TASK"]), self.num_classes)
        score = self.model.evaluate(x_pred, y_pred,
                                    batch_size=1, verbose=0)
        task_pr = score[1]

        y_pred = utils.np_utils.to_categorical(self.encoder.transform(["MEETING"]), self.num_classes)
        score = self.model.evaluate(x_pred, y_pred,
                                    batch_size=1, verbose=0)
        meet_pr = score[1]

        y_pred = utils.np_utils.to_categorical(self.encoder.transform(["MUST_BE_IN"]), self.num_classes)
        score = self.model.evaluate(x_pred, y_pred,
                                    batch_size=1, verbose=0)
        must_pr = score[1]

        if task_pr == 1.0:
            return "TASK"

        if meet_pr == 1.0:
            return "MEETING"

        if must_pr == 1.0:
            return "MUST_BE_IN"


def classify_assignments():
    nn = NN()
    if not nn.has_model():
        nn.train_and_evaluate()
    while True:
        inp = input("Assignment:\n")
        if inp == 'quit':
            break
        print(nn.classify(inp))
        print()

classify_assignments()