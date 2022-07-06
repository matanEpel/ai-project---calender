import os
import pickle
import joblib

import numpy as np
import pandas as pd
from keras import utils, Input, Model
from keras.layers import Dense, Activation, Dropout, Conv1D, GlobalMaxPooling1D, Embedding
from keras.models import Sequential, load_model
from keras.preprocessing import text
from keras_preprocessing.sequence import pad_sequences
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression

DATASET = 'generated_data2.xlsx'
LOGREG_MODEL = 'models/logreg_model.pkl'
NN_MODEL = 'models/nn_model'
NN_TOKENIZER = "tokenizers_and_encoders/nn_tokenize.pickle"
NN_ENCODER = "tokenizers_and_encoders/nn_encoder.pickle"
CNN_MODEL = 'models/cnn_model'
CNN_TOKENIZER = "tokenizers_and_encoders/cnn_tokenize.pickle"

class LearningModel:
    def __init__(self):
        self.df = None
        self.model = None

    def has_model(self):
        return self.model is not None

    def train_and_evalute(self):
        pass

    def classify(self):
        pass


class LogReg(LearningModel):
    def __init__(self):
        super().__init__()
        self.dataset_path = LOGREG_MODEL
        if os.path.exists(LOGREG_MODEL):
            self.model = joblib.load(LOGREG_MODEL)

    def train_and_evaluate(self):
        self.df = pd.read_excel(DATASET)
        self.df.drop(columns=['LABEL'])
        self.df = self.df[pd.notnull(self.df['TITLE'])]
        my_tags = ['TASK', 'MEETING', 'MUST_BE_IN']

        X = self.df['TITLE']
        y = self.df['TYPE']
        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8)
        logreg = Pipeline([('vect', CountVectorizer()),
                           ('tfidf', TfidfTransformer()),
                           ('clf', LogisticRegression(n_jobs=1, C=1e5)),
                           ])
        logreg.fit(X_train, y_train)

        y_pred = logreg.predict(X_test)
        self.model = logreg
        joblib.dump(self.model, LOGREG_MODEL)

        print('accuracy %s' % accuracy_score(y_pred, y_test))
        print(classification_report(y_test, y_pred, target_names=my_tags))

    def classify(self, str):
        p = self.model.predict([str])
        if p[0] == "TASK":
            return 0
        if p[0] == "MEETING":
            return 1
        if p[0] == "MUST_BE_IN":
            return 2



class NN(LearningModel):
    def __init__(self):
        super().__init__()
        if os.path.exists(NN_MODEL):
            self.model = load_model(NN_MODEL)
            # loading
            with open(NN_TOKENIZER, 'rb') as handle:
                self.tokenize = pickle.load(handle)
            with open(NN_ENCODER, 'rb') as handle:
                self.encoder = pickle.load(handle)
        else:
            self.tokenize = None
            self.encoder = None
        self.max_words = 1000
        self.num_classes = 3

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
        self.df = pd.read_excel(DATASET)
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
        self.model.save(NN_MODEL)
        with open(NN_TOKENIZER, 'wb') as handle:
            pickle.dump(self.tokenize, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open(NN_ENCODER, 'wb') as handle:
            pickle.dump(self.encoder, handle, protocol=pickle.HIGHEST_PROTOCOL)

        score = self.model.evaluate(x_test, y_test,
                                    batch_size=batch_size, verbose=1)
        print('Test accuracy:', score[1])

    def classify(self, str):
        x_pred = self.tokenize.texts_to_matrix([str])
        preds = self.model.predict(x_pred)
        classification = np.argmax(preds)
        if classification == 0:
            return 1
        if classification == 1:
            return 2
        if classification == 2:
            return 0

class CNN(LearningModel):

    def __init__(self):
        super().__init__()
        if os.path.exists(CNN_MODEL):
            self.model = load_model(NN_MODEL)
            # loading
            with open(CNN_TOKENIZER, 'rb') as handle:
                self.tokenize = pickle.load(handle)
        else:
            self.tokenize = None
            self.encoder = None
        self.max_tokens = 100
        self.num_classes = 3

    def has_model(self):
        return self.model is not None

    def build_model(self):
        # Build the self.model
        embed_len = 128

        inputs = Input(shape=(self.max_tokens,))
        embeddings_layer = Embedding(input_dim=len(self.tokenize.word_index) + 1, output_dim=embed_len,
                                     input_length=self.max_tokens)
        conv = Conv1D(32, 7, padding="same")  ## Channels last
        dense = Dense(self.num_classes, activation="softmax")

        x = embeddings_layer(inputs)
        x = conv(x)
        from tensorflow import reduce_max
        x = reduce_max(x, axis=1)
        output = dense(x)

        self.model = Model(inputs=inputs, outputs=output)

        self.model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])

        self.model.summary()

    def train_and_evaluate(self):
        self.df = pd.read_excel(DATASET)
        self.df.drop(columns=['LABEL'])
        self.df = self.df[pd.notnull(self.df['TITLE'])]
        my_tags = ['TASK', 'MEETING', 'MUST_BE_IN']

        X = self.df['TITLE']
        y = self.df['TYPE']
        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8)

        self.tokenize = text.Tokenizer()
        self.tokenize.fit_on_texts(X_train)  # only fit on train

        x_train = pad_sequences(self.tokenize.texts_to_sequences(X_train), maxlen=self.max_tokens, padding="post",
                                     truncating="post", value=0.)
        x_test = pad_sequences(self.tokenize.texts_to_sequences(X_train), maxlen=self.max_tokens, padding="post", truncating="post", value=0.)

        self.build_model()
        batch_size = 32
        epochs = 2
        history = self.model.fit(x_train, y_train,
                                 batch_size=batch_size,
                                 epochs=epochs,
                                 verbose=1,
                                 validation_split=0.1)
        self.model.save(CNN_MODEL)
        with open(CNN_TOKENIZER, 'wb') as handle:
            pickle.dump(self.tokenize, handle, protocol=pickle.HIGHEST_PROTOCOL)

        score = self.model.evaluate(x_test, y_test,
                                    batch_size=batch_size, verbose=1)
        print('Test accuracy:', score[1])

    def classify(self, str):
        x_pred = pad_sequences(self.tokenize.texts_to_sequences([str]), maxlen=self.max_tokens, padding="post",
                                     truncating="post", value=0.)
        preds = self.model.predict(x_pred)
        classification = np.argmax(preds)
        if classification == 0:
            return 1
        if classification == 1:
            return 2
        if classification == 2:
            return 0


def classify_assignments_continuous(cls):
    learning_model = cls()
    if not learning_model.has_model():
        learning_model.train_and_evaluate()
    while True:
        inp = input("Assignment:\n")
        if inp == 'quit':
            break
        print(learning_model.classify(inp))
        print()


def classify_assignments(cls, name):
    model = cls()
    if not model.has_model():
        model.train_and_evaluate()
    return model.classify(name)

classify_assignments_continuous(NN)