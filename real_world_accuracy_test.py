from cv2.cv2 import VideoCapture, resize, cvtColor, COLOR_BGR2RGB
from keras.models import load_model
from numpy import array, expand_dims, vstack

model = load_model('model_saved.h5')
cam = VideoCapture(0)
runs_per = 0
inp = ""

while True:
    runs_per = int(input("How many times would you like to run each test? "))
    if runs_per <= 0:
        print("Please enter a number greater than 0")
    elif runs_per == "q":
        print("Ok bye then")
        quit()
    else:
        break

correct = {
    "rock": 0,
    "paper": 0,
    "scissors": 0
}
incorrect = {
    "rock-paper": 0,
    "rock-scissors": 0,
    "paper-rock": 0,
    "paper-scissors": 0,
    "scissors-rock": 0,
    "scissors-paper": 0
}


def predict():
    trash, img_source = cam.read()
    img_source = array(img_source)
    img_source = vstack([img_source])
    img_source = cvtColor(img_source, COLOR_BGR2RGB)
    img_source = resize(img_source, (300, 200))
    img_source = expand_dims(img_source, axis=0)
    img_source = img_source / 255
    classes = model.predict(img_source, batch_size=10)[0]

    if classes[0] > classes[1] and classes[0] > classes[2]:
        return "paper"
    elif classes[1] > classes[0] and classes[1] > classes[2]:
        return "rock"
    elif classes[2] > classes[0] and classes[2] > classes[1]:
        return "scissors"


print("--------------------\n    ROCK TESTING\n--------------------")
for i in range(runs_per):
    if input("hold up rock and press enter:") == "q":
        print("Ok bye then")
        quit()
    prediction = predict()
    if prediction == "rock":
        correct["rock"] += 1
    elif prediction == "paper":
        incorrect["rock-paper"] += 1
    elif predict() == "scissors":
        incorrect["rock-scissors"] += 1
    print("test number ", i + 1, " gave result: ", prediction)

print("--------------------\n    PAPER TESTING\n--------------------")
for i in range(runs_per):
    if input("hold up paper and press enter:") == "q":
        print("Ok bye then")
        quit()
    prediction = predict()
    if prediction == "rock":
        incorrect["paper-rock"] += 1
    elif prediction == "paper":
        correct["paper"] += 1
    elif predict() == "scissors":
        incorrect["paper-scissors"] += 1
    print("test number ", i + 1, " gave result: ", prediction)

print("--------------------\n    SCISSORS TESTING\n--------------------")
for i in range(runs_per):
    if input("hold up scissors and press enter:") == "q":
        print("Ok bye then")
        quit()
    prediction = predict()
    if prediction == "rock":
        incorrect["scissors-rock"] += 1
    elif prediction == "paper":
        incorrect["scissors-paper"] += 1
    elif predict() == "scissors":
        correct["scissors"] += 1
    print("test number ", i + 1, " gave result: ", prediction)

print("--------------------\n    FINAL RESULTS\n--------------------")
print("The machine guessed the following signs correctly:\nRock: ",
      correct["rock"], "\nPaper: ", correct["paper"], "\nScissors: ", correct["scissors"])

print("Of the signs guessed incorrectly, the machine classified:\n", incorrect["rock-paper"], " rock as paper\n",
      incorrect["rock-scissors"], " rock as scissors\n", incorrect["paper-rock"], " paper as rock\n",
      incorrect["paper-scissors"], " paper as scissors\n", incorrect["scissors-paper"], " scissors as paper\n",
      incorrect["scissors-rock"], " scissors as rock\n")

rock_accuracy = (correct["rock"] / runs_per)*100
paper_accuracy = (correct["paper"] / runs_per)*100
scissors_accuracy = (correct["scissors"] / runs_per)*100
print("This results in accuracies of ", str(rock_accuracy), "% for rock ", str(paper_accuracy), "% for for paper, and ",
      str(scissors_accuracy), "% for scissors.\nOverall, this gives the machine a real world accuracy of ",
      str((rock_accuracy + paper_accuracy + scissors_accuracy) / (runs_per * 3)), "%")
