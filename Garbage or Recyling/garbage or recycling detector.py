# Running on an Online IDE might not work
# WORKS BEST ON MONITORS
# If you're running using a laptop that is connected to a monitor, make sure to stay on your IDE till a window opens up
# The window might open up in the background, ALT+TAB to find it!
# To run this code you will need to install the following packages:
# pip install tensorflow
# pip install pygame
# pip install opencv-python
# pip install --upgrade Pillow
# pip install numpy



import pygame
import random
import cv2
from pygame.locals import *
from model import classifying, convertion

#camera setup
pygame.init()
camera = cv2.VideoCapture(0)

#screen setup
screen = pygame.display.set_mode((1200, 1000))
pygame.display.set_caption('Garbage or Recycling detector')

#color setup
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#fonts
bigfont = pygame.font.SysFont(None, 80)
regularfont = pygame.font.SysFont(None, 36)

#defining what should be recycled and what should be thrown in garbage
def garb_recy(result):
    if result == "Plastic-Bottles":
        return "Recycle It!"
    if result == "Paper/Cardboard":
        return "Recycle It!"
    if result == "Glass":
        return "Recycle It!"
    if result == "Plastics":
        return "Recycle It!"
    if result == "Coated-Paper-Products":
        return "GARBAGE!"
    if result == "Styrofoam":
        return "GARBAGE!"


def gui():
    screen.fill(BLACK)
    pygame.time.set_timer(pygame.USEREVENT, 3000, True)
    running = True
    while running:
        pygame.display.update()
        
        #instruction labels
        instruct_label = regularfont.render("Instructions:", True, WHITE)
        instruct_label_rect = instruct_label.get_rect()
        instruct_label_rect.left = 400
        instruct_label_rect.top = 60
        screen.blit(instruct_label, instruct_label_rect)

        instruct_label = regularfont.render("1. Only place your object in the camera", True, WHITE)
        instruct_label_rect = instruct_label.get_rect()
        instruct_label_rect.left = 400
        instruct_label_rect.top = 100
        screen.blit(instruct_label, instruct_label_rect)

        instruct_label = regularfont.render("2. Press on the Replay button if the AI ", True, WHITE)
        instruct_label_rect = instruct_label.get_rect()
        instruct_label_rect.left = 400
        instruct_label_rect.top = 140
        screen.blit(instruct_label, instruct_label_rect)

        instruct_label = regularfont.render("doesn't classify your object correctly", True, WHITE)
        instruct_label_rect = instruct_label.get_rect()
        instruct_label_rect.left = 400
        instruct_label_rect.top = 180
        screen.blit(instruct_label, instruct_label_rect)
        
        instruct_label = regularfont.render("3. Keep in mind that it can only identify the following: ", True, WHITE)
        instruct_label_rect = instruct_label.get_rect()
        instruct_label_rect.left = 400
        instruct_label_rect.top = 220
        screen.blit(instruct_label, instruct_label_rect)
        
    
        instruct_label = regularfont.render("Plastic Bottles, Paper or Cardboard, Glass", True, WHITE)
        instruct_label_rect = instruct_label.get_rect()
        instruct_label_rect.left = 400
        instruct_label_rect.top = 260
        screen.blit(instruct_label, instruct_label_rect)
        
        instruct_label = regularfont.render("Coated Paper Products, Styrofoam, Plastics ", True, WHITE)
        instruct_label_rect = instruct_label.get_rect()
        instruct_label_rect.left = 400
        instruct_label_rect.top = 300
        screen.blit(instruct_label, instruct_label_rect)  
                
        #camera update
        ret, frame = camera.read()
        image = convertion(frame)
        screen.blit(image, (20, 70))
        pygame.display.update()
        
        for event in pygame.event.get():
            #close window
            if event.type == QUIT:
                pygame.quit()
             #classiying image as garbage or recycling
            elif event.type == pygame.USEREVENT:
                
                #running the camera through the AI
                pygame.image.save(image, 'img/result_image.png')
                result = classifying('img/result_image.png', 'keras_model.h5')
                result_label = regularfont.render(result, True, WHITE)
                result_label_rect = result_label.get_rect()
                result_label_rect.left = 100
                result_label_rect.top = 350
                screen.blit(result_label, result_label_rect)
                
                
                #using the logic to display the results
                output = garb_recy(result)
                output_label = bigfont.render(output, True, WHITE)
                output_label_rect = output_label.get_rect()
                output_label_rect.left = 50
                output_label_rect.top = 400
                screen.blit(output_label, output_label_rect)
                
                
                #replaying the program if there were errors or you want to check another object
                replay_button = pygame.image.load('img/replay.png')
                replay_button = pygame.transform.scale(replay_button,(222,245))
                screen.blit(replay_button, (100, 500))
            
            elif event.type == MOUSEBUTTONDOWN:
                if (100 < event.pos[0] < (100+222)) and (500 < event.pos[1] < (500+245)):
                    running = False
                    gui()
                               
gui()