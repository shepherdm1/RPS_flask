from flask import Flask, render_template, request
from cv2 import imdecode, cvtColor, IMREAD_COLOR, COLOR_BGR2RGB
from keras.models import load_model
from numpy import expand_dims, frombuffer, array, uint8
from base64 import b64decode
from random import choice

# Load pretrained classification model
model = load_model('model_saved.h5')

# instatiate flask app
app = Flask(__name__, template_folder='./templates')

# convert image to keras friendly, predict class
def predict(img_source):
    img = expand_dims(img_source, axis=0)
    classes = model.predict(img, batch_size=10)[0]
    if classes[0] > classes[1] and classes[0] > classes[2]:
        result = "paper"
    elif classes[1] > classes[0] and classes[1] > classes[2]:
        result = "rock"
    elif classes[2] > classes[0] and classes[2] > classes[1]:
        result = "scissors"
    return result

# decide winner based on predicted class and random cpu choice
def decide_winner(player_choice):
    cpu_choice = choice(['rock', 'paper', 'scissors'])
    if player_choice == cpu_choice:
        return [player_choice, cpu_choice, "tied"]
    elif player_choice == "scissors" and cpu_choice == "rock":
        return [player_choice, cpu_choice, "lost"]
    elif player_choice == "rock" and cpu_choice == "paper":
        return [player_choice, cpu_choice, "lost"]
    elif player_choice == "paper" and cpu_choice == "scissors":
        return [player_choice, cpu_choice, "lost"]
    else:
        return [player_choice, cpu_choice, "won"]

# serve the webpage
@app.route('/')
def index():
    return render_template("index.html")

# recieve and respond when image is sent from client side
@app.route('/get_image', methods=['POST', 'GET'])
def get_image():
    image_encoded = request.values['imageBase64']
    img_bytes = b64decode(image_encoded)
    img_arr = frombuffer(img_bytes, dtype=uint8)
    img = imdecode(img_arr, flags=IMREAD_COLOR)  # change to grayscale if wanted
    img = cvtColor(array(img), COLOR_BGR2RGB)
    img = img / 255
    condition = decide_winner(predict(img))
    return "You chose " + condition[0] + " and the computer chose " + condition[1] + " so you " + condition[2] + "."


if __name__ == '__main__':
    app.run()
