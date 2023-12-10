import pickle
import time
from collections import Counter

import cv2
import face_recognition
import numpy as np

from gesture import speak_text

with open("encoded-file.p", "rb") as file:
    encoded_list = pickle.load(file)


def recognize_face(samples=5, timeout=10):
    speak_text("Detecting person")
    cap = cv2.VideoCapture(0)

    s_time = time.time()
    detected_names = []
    while True:
        success, img = cap.read()
        img_small = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)

        faces_in_current_frame = face_recognition.face_locations(img_small)
        encode_current_frame = face_recognition.face_encodings(img_small, faces_in_current_frame)

        for encoded_face, face_loc in zip(encode_current_frame, faces_in_current_frame):
            matches = face_recognition.compare_faces(encoded_list[0], encoded_face)
            face_distance = face_recognition.face_distance(encoded_list[0], encoded_face)
            true_indexes = [i for i, value in enumerate(matches) if value]
            if len(true_indexes) == 0:
                continue

            min_value = np.min(face_distance[true_indexes])
            min_index = np.argmin(face_distance[true_indexes])
            if min_value < 0.5:
                print(encoded_list[1][true_indexes[min_index]])
                detected_names.append(encoded_list[1][true_indexes[min_index]])
        if len(detected_names) == samples:
            counts = Counter(detected_names)
            return counts.most_common(1)[0][0]
        if time.time() - s_time > timeout:
            return None
        cv2.imshow("img", img)
        cv2.waitKey(1)


if __name__ == '__main__':
    print(recognize_face())
