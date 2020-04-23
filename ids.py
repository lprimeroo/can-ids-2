from keras.initializers import Constant
import numpy as np
from keras.layers import Input
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Flatten, Bidirectional, Conv1D
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer


def tokenize_data(sentences, vocab_size=10000):
    T = Tokenizer(num_words=vocab_size + 1, oov_token='UNK')
    T.fit_on_texts(sentences)

    data = T.texts_to_sequences(sentences)

    word_to_idx = T.word_index
    idx_to_word = {v: k for k, v in word_to_idx.items()}

    return data, word_to_idx, idx_to_word, T


def get_data(file):
    can_ids = []
    with open(file) as f:
        data = f.read().splitlines()
        for row in data:
            can_data = row.split(' ')
            can_id = can_data[2].split('#')[0]
            can_ids.append(can_id)
    return can_ids


def get_X_Y_data(data, output_class=57, sl_window=10):
    global word_to_idx, idx_to_word, training_data
    X_data, Y_data = [], []
    for i in range(len(data) - sl_window - 1):
        initial_data = [x[0] for x in data[i:i + sl_window]]
        y = [0] * output_class
        y[data[i + sl_window][0]] = 1
        X_data.append(initial_data)
        Y_data.append(y)
    return X_data, Y_data


def detect(model_type):
    training_data = get_data('./data/RenaultClio/full_data_capture.log')
    testing_data = get_data('./data/RenaultClio/dosattack.log')
    dos_data = get_data('./data/RenaultClio/dosattack.log')

    data, word_to_idx, idx_to_word, T = tokenize_data(training_data, 56)
    X_train, Y_train = get_X_Y_data(data, 57, 40)
    X_test, Y_test = get_X_Y_data(T.texts_to_sequences(testing_data),  57, 40)
    X_train = pad_sequences(X_train, 40)
    X_test = pad_sequences(X_test, 40)
    dos_X_test, dos_Y_test = get_X_Y_data(T.texts_to_sequences(dos_data),  57, 40)
    dos_X_test = pad_sequences(dos_X_test, 40)
    dos_Y_test = np.matrix(dos_Y_test)

    Y_train = np.matrix(Y_train)
    Y_test = np.matrix(Y_test)
    epochs = 10

    model = Sequential()
    model.add(Embedding(57, 40,
                        input_length=40))
    model.add(LSTM(70, activation='relu',
                dropout=0.1, return_sequences=True))
    model.add(Flatten())
    model.add(Dense(10, activation='relu'))
    model.add(Dense(57, activation='softmax'))
    # model.compile(optimizer='adam', loss='categorical_crossentropy',
    #               metrics=['accuracy'])
    # print(model.summary())

    # model.fit(X_train, Y_train, validation_data=(
    #     X_test, Y_test), epochs=epochs, batch_size=50, shuffle=True)

    # model.save_weights('./weights')
    model.load_weights('./weights')


    classes = model.predict_classes(dos_X_test)
    predictions = model.predict(dos_X_test)
    anomalies = 0
    confidence = 0.999


    for i, pred in enumerate(classes):
        if pred == np.argmax(dos_Y_test[i]):
            continue
        else:
            val = predictions[i][np.argmax(dos_Y_test[i])]
            if confidence < 1 - val:
                anomalies += 1

    print("Anomalies is ", anomalies/len(predictions))