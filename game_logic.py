import random
import pygame

# Defining the window size for the game
window_width = 500
window_height = 500

# Defining the size of the side paddles
paddle_height = 80
paddle_width = 20

# Defining the distance between the paddle and the window_height
paddle_buff = 10

# Defining the size of the "rectangular ball"
ball_height = 15
ball_width = 15

# Defining how fast the "ball" and paddle can move in the game space
# "Ball" speed in the x direction
ballspeed_x = 3
# "Ball" speed in the y direction
ballspeed_y = 2
# Paddle speed in the y direction(it only moves in the y direction)
paddlespeed_y = 2

# Defining the color schemes of the "ball" and paddle
# Background Color
black = (0,0,0)
# "Ball" Color
white = (255,255,255)
# AI Paddle Color
green = (124,252,0)
# Learning Paddle Color
salmon = (255,160,122)

# Initializing the screen using the predefined widow dimensions
screen = pygame.display.set_mode((window_width, window_height))

# Drawing the assets using pygame.

# Drawing the ball
def drawBall(ballxPos, ballyPos):
    # Defining the attributes of the ball
    ball = pygame.Rect(ballxPos, ballyPos, ball_width, ball_height)
    # Drawing the ball (where, color, what)
    pygame.draw.rect(screen, white, ball)

# Drawing the AI paddle
def drawAIpaddle(aipaddleyPos):
    aipaddle = pygame.Rect(paddle_buff, aipaddleyPos, paddle_width, paddle_height)
    pygame.draw.rect(screen, green, aipaddle)

# Drawing the learning Paddle
def drawLearningpaddle(learningpaddleyPos):
    learningpaddle = pygame.Rect(paddle_buff, learningpaddleyPos, paddle_width, paddle_height)
    pygame.draw.rect(screen, salmon, learningpaddle)

# The next step is updating the ball position which is going to be
# a function of the paddles, the ball and the
# direction the ball is travelling in.

def updateBallPos(aipaddleyPos, learningpaddleyPos, ballxPos, ballyPos, ballxDir, ballyDir):
    # The x position of the ball is updated as the ball moves in the game space
    ballxPos = ballxPos + ballyDir * ballspeed_x
    # The y position of the ball is updated as the ball moves in the game space
    ballyPos = ballyPos + ballyDir * ballspeed_y
    score = 0

    # If the x position of the ball is LTE to the paddle buffer and paddle width(aka hit the side of the screen) and..
    if(ballxPos <= paddle_buff + paddle_width and
       # ... if the y position of the ball + height is greater than the y position of the AIpaddle and..
       ballyPos + ball_height >= aipaddleyPos and
       # ..if the y position of the ball - the height of the ball is LTE the AIpaddle position + its height
       ballyPos - ball_height <= aipaddleyPos + paddle_height):
       #We change the direction the ball is moving in.
        ballxDir = 1
    elif (ballxPos <= 0):
        ballxDir = 1
        score = -1
        return [score, aipaddleyPos, ballxPos, ballyPos, ballxDir]
