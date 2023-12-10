import os
import pickle

import cv2
import face_recognition


def find_encodings(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    encoding = face_recognition.face_encodings(img)[0]
    return encoding


if __name__ == '__main__':
    user_names = []
    encoded_images = []
    for user in os.scandir("dataset/"):
        name = user.name.split(".")[0]
        print(name)
        user_names.append(name)
        encoded_images.append(find_encodings(cv2.imread(user.path)))

    with open("encoded-file.p", "wb") as file:
        pickle.dump([encoded_images, user_names], file)
