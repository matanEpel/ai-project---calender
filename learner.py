# import numpy as np
# import pandas as pd
# import tensorflow as tf
#
# from keras import layers
# from keras.layers import TextVectorization
#
#
# def df_to_dataset(dataframe, shuffle=True, batch_size=32):
#     df = dataframe.copy()
#     labels = df.pop('LABEL')
#     df = {key: value[:, tf.newaxis] for key, value in dataframe.items()}
#     ds = tf.data.Dataset.from_tensor_slices((dict(df), labels))
#     if shuffle:
#         ds = ds.shuffle(buffer_size=len(dataframe))
#     ds = ds.batch(batch_size)
#     return ds
#
#
# df = pd.read_excel("generated_data.xlsx")
# df = df.drop(columns=['LENGTH', 'TYPE'])
# train, val, test = np.split(df.sample(frac=1), [int(0.8 * len(df)), int(0.9 * len(df))])
# raw_train_ds = df_to_dataset(train, batch_size=32)
# raw_val_ds = df_to_dataset(val, batch_size=32)
# raw_test_ds = df_to_dataset(test, batch_size=32)
#
# # Model constants.
# max_features = 20000
# embedding_dim = 128
# sequence_length = 90
#
# # Now that we have our custom standardization, we can instantiate our text
# # vectorization layer. We are using this layer to normalize, split, and map
# # strings to integers, so we set our 'output_mode' to 'int'.
# # Note that we're using the default split function,
# # and the custom standardization defined above.
# # We also set an explicit maximum sequence length, since the CNNs later in our
# # model won't support ragged sequences.
# vectorize_layer = TextVectorization(
#     max_tokens=max_features,
#     output_mode="int",
#     output_sequence_length=sequence_length,
# )
#
# text_ds = raw_train_ds.map(lambda x, y: x)
# vectorize_layer.adapt(text_ds)
#
#
# def vectorize_text(text, label):
#     text = tf.expand_dims(text, -1)
#     return vectorize_layer(text), label
#
#
# # Vectorize the data.
# train_ds = raw_train_ds.map(vectorize_text)
# val_ds = raw_val_ds.map(vectorize_text)
# test_ds = raw_test_ds.map(vectorize_text)
#
# # A integer input for vocab indices.
# inputs = tf.keras.Input(shape=(None,), dtype="int64")
#
# # Next, we add a layer to map those vocab indices into a space of dimensionality
# # 'embedding_dim'.
# x = layers.Embedding(max_features, embedding_dim)(inputs)
# x = layers.Dropout(0.5)(x)
#
# # Conv1D + global max pooling
# x = layers.Conv1D(128, 7, padding="valid", activation="relu", strides=3)(x)
# x = layers.Conv1D(128, 7, padding="valid", activation="relu", strides=3)(x)
# x = layers.GlobalMaxPooling1D()(x)
#
# # We add a vanilla hidden layer:
# x = layers.Dense(128, activation="relu")(x)
# x = layers.Dropout(0.5)(x)
#
# # We project onto a single unit output layer, and squash it with a sigmoid:
# predictions = layers.Dense(1, activation="sigmoid", name="predictions")(x)
#
# model = tf.keras.Model(inputs, predictions)
#
# # Compile the model with binary crossentropy loss and an adam optimizer.
# model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
#
# epochs = 6
#
# # Fit the model using the train and test datasets.
# model.fit(train_ds, validation_data=val_ds, epochs=epochs)
#
# model.evaluate(test_ds)
import numpy as np
from tensorflow import keras
import tensorflow as tf

loaded_model = keras.models.load_model("fitted_model")

end_to_end_model = keras.Sequential([
  keras.Input(shape=(1,), dtype="string"),
  vectorize_layer,
  loaded_model,
  keras.layers.Activation('softmax')
])

end_to_end_model.compile(
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False), optimizer="adam", metrics=['accuracy']
)
end_to_end_model.summary()


predictions=loaded_end_to_end_model.predict(['Meeting with Ophir'])
print(np.argmax(predictions[0]))
print(np.argmax(predictions[1]))