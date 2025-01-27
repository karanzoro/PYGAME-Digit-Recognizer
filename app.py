import pygame
import sys
from pygame.locals import *
import numpy as np
import tensorflow as tf
import cv2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WINDOWSIZEX = 640
WINDOWSIZEY = 480
BOUNDARYINC = 5
IMAGESAVE = False

# Load the TensorFlow/Keras model
MODEL = tf.keras.models.load_model("./bestmodel.keras")
LABELS = {0: "Zero", 1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine"}

pygame.init()
FONT = pygame.font.Font("freesansbold.ttf", 18)
DISPLAYSURF = pygame.display.set_mode((WINDOWSIZEX, WINDOWSIZEY))
WHITE_INT = DISPLAYSURF.map_rgb(WHITE)
pygame.display.set_caption("Digit Board")
DISPLAYSURF.fill(BLACK)
iswriting = False
number_xcord = []
number_ycord = []
img_ctr = 1
PREDICT = True

while True: 

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEMOTION and iswriting:
            xcord, ycord = event.pos
            pygame.draw.circle(DISPLAYSURF, WHITE, (xcord, ycord), 4, 0)
            number_xcord.append(xcord)
            number_ycord.append(ycord)
            
        if event.type == MOUSEBUTTONDOWN:
            iswriting = True

        if event.type == MOUSEBUTTONUP:
            iswriting = False

            if number_xcord and number_ycord:  # Ensure the lists are not empty
                number_xcord = sorted(number_xcord)
                number_ycord = sorted(number_ycord)

                rect_min_x = max(number_xcord[0] - BOUNDARYINC, 0)
                rect_max_x = min(WINDOWSIZEX, number_xcord[-1] + BOUNDARYINC)
                rect_min_y = max(number_ycord[0] - BOUNDARYINC, 0)
                rect_max_y = min(WINDOWSIZEY, number_ycord[-1] + BOUNDARYINC)

                number_xcord = []
                number_ycord = []

                img_arr = np.array(pygame.PixelArray(DISPLAYSURF))[rect_min_x:rect_max_x, rect_min_y:rect_max_y].T.astype(np.float32)

                if IMAGESAVE:
                    cv2.imwrite(f"image_{img_ctr}.png", img_arr)
                    img_ctr += 1

                if PREDICT:
                    image = cv2.resize(img_arr, (28, 28))
                    image = np.pad(image, (10, 10), 'constant', constant_values=0)
                    image = cv2.resize(image, (28, 28)) / 255.0  # Normalize to [0, 1] range

                    # Perform prediction
                    prediction = MODEL.predict(image.reshape(1, 28, 28, 1))
                    label = str(LABELS[np.argmax(prediction)]).title()

                    textSurfaceObj = FONT.render(label, True, RED, WHITE)
                    textRectObj = textSurfaceObj.get_rect()
                    textRectObj.left, textRectObj.bottom = rect_min_x, rect_max_y

                    DISPLAYSURF.blit(textSurfaceObj, textRectObj)

                pygame.draw.rect(DISPLAYSURF, RED, (rect_min_x, rect_min_y, rect_max_x - rect_min_x, rect_max_y - rect_min_y), 3)

        if event.type == KEYDOWN:
            if event.unicode == "n":
                DISPLAYSURF.fill(BLACK)
    
    pygame.display.update()
