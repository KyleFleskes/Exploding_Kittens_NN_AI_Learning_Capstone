# This class is used to train the NN with the generated data.
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Activation, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
import tensorflow.compat.v2.feature_column as feature_column
import os.path
import pandas as pd
import numpy as np
import tensorflow as tf
config = tf.compat.v1.ConfigProto(gpu_options=tf.compat.v1.GPUOptions(
    per_process_gpu_memory_fraction=0.8)
    # device_count = {'GPU': 1}
)
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)
tf.compat.v1.keras.backend.set_session(session)


class training:

    def __init__(self, model_fpath):
        self.model_fpath = model_fpath

        # if a neural network does not exist then create one.
        if os.path.isfile(self.model_fpath) is False:
            print("!!!Creating new model!!!")
            self.model = self.create_model()
            self.save_model()

        # load previously created model.
        else:
            self.model = tf.keras.models.load_model(self.model_fpath)
            print("!!!!Loading model from file!!!!")

    # creates a new model with an input layer with 12 nodes, 2 hiddens layers each with size 11 and 10 respectively
    # and 1 output layers each with size 10.
    def create_model(self):
        model = Sequential([
            # creates first hidden layer(Second overall layer),
            Dense(units=14, input_shape=(15,), activation='relu'),
            # with 15 nodes,
            # with an input layer of shape (1,).
            Dense(units=14, activation='relu'),
            # create an output layer with 13 output nodes.
            Dense(units=13, activation='sigmoid')
        ])
        model.compile(optimizer=Adam(learning_rate=0.0001),
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])

        return model

    # saves the current state of the model.
    def save_model(self):
        self.model.save(self.model_fpath)
        print("!!!Model saved!!!")

    def train(self, data_fpath):
        if os.path.isfile(data_fpath) is False:
            print("Could not find data!!!!")
            return

        d_train = pd.read_csv(data_fpath)

        print(d_train.head())

        INPUT_COLUMNS = ["Exploding Kitten", "Attack", "Skip", "Favor",\
                "Shuffle", "See-The-Future", "Draw-From-Bottom", "Defuse",\
                "Taco", "Watermelon", "Potato", "Beard", "Rainbow",\
                "Last Card Played Index", "Cards in Deck"]

        OUTPUT_COLUMNS = ["Attack Winrate", "Skip Winrate", "Favor Winrate", "Shuffle Winrate",\
                "See-The-Future Winrate", "Draw-From-Bottom Winrate", "Defuse Winrate",\
                "Taco Winrate", "Watermelon Winrate", "Potato Winrate", "Beard Winrate",\
                "Rainbow Winrate", "Draw Winrate"]
       
        input_columns = d_train.copy()
        output_columns = d_train.copy()

        # remove output data from input data.
        for feature_name in OUTPUT_COLUMNS:
            input_columns.pop(feature_name)
        
        # remove input data from output data.
        for feature_name in INPUT_COLUMNS:
            output_columns.pop(feature_name)
        
        print(input_columns.head())
        print()
        print(output_columns.head())
        
        #self.model.fit()

