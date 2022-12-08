import socket

import cv2
import mediapipe as mp
from google.protobuf.json_format import MessageToDict


def float_to_str(f):
    float_string = repr(f)
    if 'e' in float_string:  # detect scientific notation
        digits, exp = float_string.split('e')
        digits = digits.replace('.', '').replace('-', '')
        exp = int(exp)
        zero_padding = '0' * (abs(int(exp)) - 1)  # minus 1 for decimal point in the sci notation
        sign = '-' if f < 0 else ''
        if exp > 0:
            float_string = '{}{}{}.0'.format(sign, digits, zero_padding)
        else:
            float_string = '{}0.{}{}'.format(sign, zero_padding, digits)
    return float_string


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ('127.0.0.1', 5052)

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print('Ignoring empty camera frame.')
            continue

        image = cv2.flip(image, 1)
        image.flags.writeable = False
        imgHeight, imgWidth, c = image.shape
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        handLeft = []
        handRight = []
        if results.multi_hand_landmarks:
            for i, handedness_raw in enumerate(results.multi_handedness):
                handedness = MessageToDict(handedness_raw.classification[0])
                if handedness['label'] == 'Left':
                    for landmark in results.multi_hand_landmarks[i].landmark:
                        handLeft.append(
                            float_to_str(landmark.x * imgWidth) + ',' +
                            float_to_str(landmark.y * imgHeight) + ',' +
                            float_to_str(landmark.z * imgWidth)
                        )
                if handedness['label'] == 'Right':
                    for landmark in results.multi_hand_landmarks[i].landmark:
                        handRight.append(
                            float_to_str(landmark.x * imgWidth) + ',' +
                            float_to_str(landmark.y * imgHeight) + ',' +
                            float_to_str(landmark.z * imgWidth)
                        )
            handLeft = ' ' if len(handLeft) == 0 else '/'.join(handLeft)
            handRight = ' ' if len(handRight) == 0 else '/'.join(handRight)
            strData = str.encode(handLeft + ';' + handRight)
            sock.sendto(strData, serverAddressPort)
            print(strData)
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()

# while True:
#     # Get image frame
#     success, image = cap.read()
#     # Flip the image so it works like a mirror
#     image = cv2.flip(image, 1)
#     # Find the hand and its landmarks
#     hands, image = detector.findHands(image)  # with draw
#     # hands = detector.findHands(img, draw=False)  # without draw
#     data = []
#
#     if hands:
#         # Hand 1
#         hand = hands[0]
#         lmList = hand["lmList"]  # List of 21 Landmark points
#         for lm in lmList:
#             data.extend([lm[0], h - lm[1], lm[2]])
#
#         sock.sendto(str.encode(str(data)), serverAddressPort)
#
#     # Display
#     cv2.imshow("Image", image)
#     cv2.waitKey(1)
