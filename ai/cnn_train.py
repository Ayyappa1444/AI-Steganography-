import tensorflow as tf
from tensorflow.keras import layers, models
import os

IMG_SIZE = 128
BATCH = 16

def load_data():
    ds = tf.keras.preprocessing.image_dataset_from_directory(
        "dataset",
        image_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH,
        label_mode="binary"
    )
    return ds

def train():
    model = models.Sequential([
        layers.Rescaling(1./255, input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        layers.Conv2D(32, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])

    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    ds = load_data()
    model.fit(ds, epochs=5)
    model.save("ai/stego_cnn.h5")

if __name__ == "__main__":
    train()
