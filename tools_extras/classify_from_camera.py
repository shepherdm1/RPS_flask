from cv2.cv2 import VideoCapture, resize, cvtColor, COLOR_BGR2RGB
from keras.models import load_model
from numpy import array, expand_dims, vstack

model = load_model('../model_saved.h5')
cam = VideoCapture(0)
x = "x"
while (x != "q"):
    x = input("press enter to take a picture:")  # enter q to quit
    trash, img_source = cam.read()
    img_source = array(img_source)
    img_source = vstack([img_source])
    img_source = cvtColor(img_source, COLOR_BGR2RGB)
    img_source = resize(img_source, (300, 200))
    img_source = expand_dims(img_source, axis=0)
    img_source = img_source / 255
    classes = model.predict(img_source, batch_size=10)[0]

    if classes[0] > classes[1] and classes[0] > classes[2]:
        print("paper")
    elif classes[1] > classes[0] and classes[1] > classes[2]:
        print("rock")
    elif classes[2] > classes[0] and classes[2] > classes[1]:
        print("scissors")

print("Ok bye then")
