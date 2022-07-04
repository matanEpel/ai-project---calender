import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras.layers import TextVectorization
from sklearn.model_selection import train_test_split

df = pd.read_excel("generated_data.xlsx")
df = df.drop(columns=['LENGTH', 'TYPE'])

features, targets = df['TITLE'], df['LABEL']

train_features, test_features, train_targets, test_targets = train_test_split(
    features, targets,
    train_size=0.8,
    test_size=0.1,
    random_state=42,
    shuffle=True,
    stratify=targets
)

train_features, val_features, train_targets, val_targets = train_test_split(
    train_features, train_targets,
    train_size=0.8,
    test_size=0.1,
    random_state=42,
    shuffle=True,
    stratify=train_targets
)

# train X & Y
train_text_ds_raw = tf.data.Dataset.from_tensor_slices(
            tf.cast(train_features.values, tf.string)
)
train_cat_ds_raw = tf.data.Dataset.from_tensor_slices(
            tf.cast(train_targets.values, tf.int64),

)
# test X & y
test_text_ds_raw = tf.data.Dataset.from_tensor_slices(
            tf.cast(test_features.values, tf.string)
)
test_cat_ds_raw = tf.data.Dataset.from_tensor_slices(
            tf.cast(test_targets.values, tf.int64),
)

# val X & Y
val_text_ds_raw = tf.data.Dataset.from_tensor_slices(
            tf.cast(val_features.values, tf.string)
)
val_cat_ds_raw = tf.data.Dataset.from_tensor_slices(
            tf.cast(val_targets.values, tf.int64),
)

# Model constants.
max_features = 20000
embedding_dim = 128
sequence_length = 90

# Now that we have our custom standardization, we can instantiate our text
# vectorization layer. We are using this layer to normalize, split, and map
# strings to integers, so we set our 'output_mode' to 'int'.
# Note that we're using the default split function,
# and the custom standardization defined above.
# We also set an explicit maximum sequence length, since the CNNs later in our
# model won't support ragged sequences.
vectorize_layer = TextVectorization(
    max_tokens=max_features,
    output_mode="int",
    output_sequence_length=sequence_length,
)

vectorize_layer.adapt(train_features)
vocab = vectorize_layer.get_vocabulary()

def convert_text_input(sample):
    text = sample
    text = tf.expand_dims(text, -1)
    return tf.squeeze(vectorize_layer(text))

# Train X
train_text_ds = train_text_ds_raw.map(convert_text_input,
                                  num_parallel_calls=tf.data.experimental.AUTOTUNE)
# Test X
test_text_ds = test_text_ds_raw.map(convert_text_input,
                                  num_parallel_calls=tf.data.experimental.AUTOTUNE)
# Val X
val_text_ds = val_text_ds_raw.map(convert_text_input,
                                  num_parallel_calls=tf.data.experimental.AUTOTUNE)

train_ds = tf.data.Dataset.zip(
    (
            train_text_ds,
            train_cat_ds_raw
     )
)

test_ds = tf.data.Dataset.zip(
    (
            test_text_ds,
            test_cat_ds_raw
     )
)

val_ds = tf.data.Dataset.zip(
    (
            val_text_ds,
            val_cat_ds_raw
     )
)


batch_size = 64
AUTOTUNE = tf.data.experimental.AUTOTUNE
buffer_size= train_ds.cardinality().numpy()

train_ds = train_ds.shuffle(buffer_size=buffer_size)\
                   .batch(batch_size=batch_size,drop_remainder=True)\
                   .cache()

test_ds = test_ds.shuffle(buffer_size=buffer_size)\
                   .batch(batch_size=batch_size,drop_remainder=True)\
                   .cache()

val_ds = val_ds.shuffle(buffer_size=buffer_size)\
                   .batch(batch_size=batch_size,drop_remainder=True)\
                   .cache()


############## MODEL ##################
inputs_tokens = layers.Input(shape=(sequence_length,), dtype=tf.int32)
embedding_layer = layers.Embedding(max_features, 256)
x = embedding_layer(inputs_tokens)
x = layers.Flatten()(x)
outputs = layers.Dense(3)(x)
model = keras.Model(inputs=inputs_tokens, outputs=outputs)

loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
metric_fn = tf.keras.metrics.SparseCategoricalAccuracy()
model.compile(optimizer="adam", loss=loss_fn, metrics=metric_fn)


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
# predictions = layers.Dense(1, name="predictions")(x)

# model = tf.keras.Model(inputs, predictions)
#
# # Compile the model with binary crossentropy loss and an adam optimizer.
# model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
# model.summary()

epochs = 3

# Fit the model using the train and test datasets.
model.fit(train_ds, validation_data=val_ds, epochs=epochs, verbose=1)

model.evaluate(test_ds)

model.save("fitted_model")