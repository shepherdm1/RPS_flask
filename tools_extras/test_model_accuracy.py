from keras.models import load_model
from numpy import vstack, expand_dims
from keras.preprocessing import image
from keras.preprocessing.image import load_img
from os import listdir
import os
from random import choice

model = load_model('../model_saved.h5')
test_runs = 500
correct = 0

# test the model with test_runs random images
for i in range(test_runs):
    sign = choice([x for x in listdir(r'RPS_dataset')])
    if os.name == 'nt':
        img_source = load_img('RPS_dataset\\' + sign + '\\' + choice([x for x in listdir('RPS_dataset\\' + sign)]),
                              target_size=(200, 300))
    else:
        img_source = load_img('RPS_dataset/' + sign + '/' + choice([x for x in listdir('RPS_dataset/' + sign)]),
                              target_size=(200, 300))
    img_array = image.img_to_array(img_source)
    img_array = expand_dims(img_array, axis=0)

    images = vstack([img_array])
    classes = model.predict(images, batch_size=100)[0]

    result = ''

    if classes[0] > classes[1] and classes[0] > classes[2]:
        result = "paper"
    elif classes[1] > classes[0] and classes[1] > classes[2]:
        result = "rock"
    elif classes[2] > classes[0] and classes[2] > classes[1]:
        result = "scissors"

    if sign == result:
        correct += 1
    else:
        print("-----")
        print("Sign should have been " + sign + ", was " + result + " on try " + str(i))

accuracy = (correct / test_runs) * 100
print("Testing determined an accuracy of " + str(accuracy) + "%")
