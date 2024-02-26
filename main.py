from keras.models import load_model
from time import sleep
import tensorflow as tf
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
import serial  # Import serial library

# Initialize serial communication with Arduino
arduino = serial.Serial('COM8', 9600)  # Adjust COM port as needed
sleep(2)  # Wait for connection to establish

face_classifier = cv2.CascadeClassifier(r'C:\Users\user\Sentiment2\Emotion_Detection_CNN\haarcascade_frontalface_default.xml')
classifier = load_model(r'C:\Users\user\Sentiment2\Emotion_Detection_CNN\sssupermodel.h5')

emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    labels = []
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
        gray_img = gray[y:y+h, x:x+w]

        # Resize the image to (48, 48)
        resized_img = cv2.resize(gray_img, (48, 48))

        # Prepare the image for prediction
        input_img = np.expand_dims(np.expand_dims(resized_img, axis=-1), axis=0)

        predictions = classifier.predict(input_img)
        max_prob_index = np.argmax(predictions)
        predicted_emotion = emotion_labels[max_prob_index]

        print("Predicted Emotion:", predicted_emotion)

        label_position = (x, y)
        cv2.putText(frame, predicted_emotion, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Map emotion to corresponding Arduino command
        emotion_to_command = {
            'Angry': 'A',
            'Disgust': 'D',
            'Fear': 'F',
            'Happy': 'H',
            'Neutral': 'N',
            'Sad': 'S',
            'Surprise': 'X'
        }
        command = emotion_to_command.get(predicted_emotion, '')
        if command:
            arduino.write(command.encode())  # Send command to Arduino

    cv2.imshow('Emotion Detector', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        arduino.write(b'O')  # Send command to turn off the LEDs
        sleep(1)
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()  # Close the serial connection
