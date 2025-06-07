import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping
import os
import keras
from keras import layers

from sklearn.metrics import classification_report, confusion_matrix

import numpy as np
import pandas as pd


file_location = os.path.join("data", "animal_dt_frame.csv")
def loadprocesseddata():
    train_df = pd.read_csv(file_location)
    train_generator = create_generators(train_df)
    return train_generator


def create_generators(train_df, batch_size=32, img_size=(64, 64)):

    train_datagen = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        vertical_flip=True,
        fill_mode='nearest',
        brightness_range=[0.2, 1.8],
        channel_shift_range=50.0,
        rescale=1./255
    )

    train_generator = train_datagen.flow_from_dataframe(
        dataframe=train_df,
        x_col="folder",
        y_col="animal",
        target_size=img_size,
        batch_size=batch_size,
        class_mode="categorical",
        shuffle=True
    )

    return train_generator


def prepare_for_train(dftrain):
    train_generator = create_generators(dftrain)
    return train_generator

def get_labels_from_dataset(dataset):
    labels = [label for _, label in dataset]
    return np.concatenate(labels, axis=0)
    
def build_cnn_model(hp, n_classes=4):
    activation = hp.Choice("activation", values=["relu", "tanh", "elu"])
    n_conv_layers = hp.Int("n_conv_layers", min_value=2, max_value=5, step=1)
    n_filters = hp.Int("n_filters", min_value=16, max_value=64, step=8)
    kernel_size_val = hp.Choice("kernel_size", values=[3, 5])
    learning_rate = hp.Float("learning_rate", min_value=1e-5, max_value=1e-2, sampling="log")
    decay_steps = hp.Int("decay_steps", min_value=1000, max_value=10000, step=1000)
    decay_rate = hp.Float("decay_rate", min_value=0.9, max_value=0.999, step=0.001)
    dropout_rate = hp.Float("dropout_rate", min_value=0.2, max_value=0.5, step=0.05)
    batch_norm = hp.Choice("batch_norm", values=[True, False])
    optimizer_choice = hp.Choice("optimizer", values=["sgd", "RMSprop", "adam", "AdamW"])

    learning_rate_schedule = keras.optimizers.schedules.CosineDecayRestarts(
        initial_learning_rate=learning_rate,
        first_decay_steps=decay_steps
    )

    if optimizer_choice == "sgd":
        optimizer = keras.optimizers.SGD(learning_rate=learning_rate_schedule)
    elif optimizer_choice == "RMSprop":
        optimizer = keras.optimizers.RMSprop(learning_rate=learning_rate_schedule)
    else:
        optimizer = keras.optimizers.Adam(learning_rate=learning_rate_schedule)

    model = keras.Sequential()

    model.add(layers.Conv2D(
        filters=n_filters,
        kernel_size=(kernel_size_val, kernel_size_val),
        use_bias=not batch_norm,
        padding='same',
        input_shape=(64, 64, 3)
    ))
    if batch_norm:
        model.add(layers.BatchNormalization())
    model.add(layers.Activation(activation))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    for i in range(n_conv_layers - 1):
        filters = max(n_filters * (2 ** i), 32)
        model.add(layers.Conv2D(
            filters=filters,
            kernel_size=(kernel_size_val, kernel_size_val),
            use_bias=not batch_norm,
            padding='same'
        ))
        if batch_norm:
            model.add(layers.BatchNormalization())
        model.add(layers.Activation(activation))
        model.add(layers.MaxPooling2D(pool_size=(2, 2)))
        model.add(layers.Dropout(dropout_rate))

    model.add(layers.GlobalAveragePooling2D())

    n_dense_units = hp.Int("n_dense_units", min_value=32, max_value=256, step=32)
    model.add(layers.Dense(units=n_dense_units, use_bias=not batch_norm))
    if batch_norm:
        model.add(layers.BatchNormalization())
    model.add(layers.Activation(activation))
    model.add(layers.Dropout(dropout_rate))

    model.add(layers.Dense(n_classes, activation="softmax"))

    model.compile(loss="CategoricalCrossentropy", optimizer=optimizer, metrics=["accuracy"])

    return model