import cv2 as cv
import mediapipe as mp
import numpy as np


class handDetector():
    """
    class that deals with the hand processing of the project
    """

    def __init__(self, mode = False, max_hands = 1):
        # setup
        self.max_hands = max_hands
        self.mode = mode
        # hand drawing stuff
        self.hands = mp.solutions.hands.Hands(self.mode, self.max_hands)
        self.drawing = mp.solutions.drawing_utils

    def detect_hands(self, img, draw=True):
        """
        Detects hands from images and draws them if requested

        returns image with annotations
        """
        img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB) # I think we need RGB
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks and draw:
            for hand_landmark in self.results.multi_hand_landmarks:
                self.drawing.draw_landmarks(img, hand_landmark,
                        mp.solutions.hands.HAND_CONNECTIONS)
        return img


    def detect_landmarks(self, shape: tuple):
        """
        Detecting hands from given image
        args:
            - img: image to grab hands from
        returns:
            - list of landmarks on the hand
        """
        landmarks = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[0] # should only be one
            for id, landmark in enumerate(my_hand.landmark):
                height, width, _ = shape
                x, y = int(landmark.x * width), int(landmark.y * height)
                landmarks.append([id, x, y])

        return landmarks
    
    def detect_finger_mode(self, landmarks):
        """
        This function takes in the image with detected hand signs and tells us
        if we are in drawing mode or not

        we do this by getting the dot product of 2 vectors (of index and middle
        fingers)

        """
        index_vector = [landmarks[8][1] - landmarks[6][1], landmarks[8][2] - landmarks[6][2]]
        middle_vector = [landmarks[12][1] - landmarks[10][1], landmarks[12][2]
                - landmarks[10][2]]
        val = np.dot(index_vector, middle_vector)
        val /= (index_vector[0]**2 + index_vector[1]**2)**.5
        val /= (middle_vector[0]**2 + middle_vector[1]**2)**.5
        return val

def main():

    cap = cv.VideoCapture(0)
    detector = handDetector()

    while True:
        _, img = cap.read()
        img = detector.detect_hands(img)

        landmark_list = detector.detect_landmarks(img.shape)
        if len(landmark_list) != 0:
            val = detector.detect_finger_mode(landmark_list)
            print(val, landmark_list[4])

        cv.imshow('Camera', img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
