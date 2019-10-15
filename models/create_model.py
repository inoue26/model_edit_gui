# create model
from keras.models import Model
from keras.layers import Input, Dense, concatenate

input_ = Input(shape=(3,))
dense1 = Dense(3)
dense2 = Dense(10)

h = dense1(input_)
h1 = dense1(h)
h2 = dense2(h)

h = concatenate([h1, h2], axis=-1)
output_ = Dense(3)(h)

model = Model(input_, output_)

model.save('./model.h5')