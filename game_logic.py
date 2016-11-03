import pygame
import random

FPS = 60
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

    # Check for whether the the ball hits the side of the screen or the learningpaddle
    # If the x position of the ball is LTE to the paddle buffer and paddle width(aka hit the side of the screen) and..
    if(ballxPos <= paddle_buff + paddle_width and
        # ... if the y position of the ball + height of the ball is greater than the y position of the AIpaddle and..
        ballyPos + ball_height >= aipaddleyPos and
        # ..if the y position of the ball - the height of the ball is LTE the AIpaddle position + its height
        ballyPos - ball_height <= aipaddleyPos + paddle_height):
        #We change the direction the ball is moving in.
        ballxDir = 1
    elif (ballxPos <= 0):
        ballxDir = 1
        score = -1
        return [score, aipaddleyPos, learningpaddleyPos, ballxPos, ballyPos, ballxDir, ballyDir]

    # Checking if we are ever able to beat the AI
    # If the x position of the ball is within the difference of the windowidth, paddle_width and paddle_buff ...
    if(ballxPos >= window_width - paddle_width - paddle_buff
    # ...and if the y position of the ball plus the height of the ball is greater than or equal to the y position of the learning paddle
        and ballyPos + ball_height >= learningpaddleyPos
        # ... and if the y position of the ball - the height of the ball are less than the y position of the learning paddle + the paddle height
        and ballyPos - ball_height <= learningpaddleyPos + paddle_height):
        # The direction of the ball changes
        ballxDir = -1
    # else if the x position of the ball is greater that the window width - ball width (500 - 15 = 485) aka the ball passes we switch direction
    elif (ballxPos >= window_width - ball_width):
        ballxDir = -1
        score = 1
        return [score, aipaddleyPos, learningpaddleyPos, ballxPos, ballyPos, ballxDir, ballyDir]

    # Finally a check for whether the ball hits either the top of the screen or the bottom.
    # If the ball hits the top, the direction needs to be changed to down and vice versa
    if (ballyPos <= 0):
        ballyPos = 0
        ballyDir =1

    # If the ball hits the bottom, it needs to change direction aswell
    if (ballyPos >= window_height - ball_height):
        ballyPos = window_height - ball_height
        ballyDir = -1
    return[score, aipaddleyPos, learningpaddleyPos, ballxPos, ballxDir, ballyDir]

# Updating AI paddle position.
def updateaiPaddle(action, aipaddleyPos):
    if (action[1] == 1):
        aipaddleyPos = aipaddleyPos - paddlespeed_y

    if (action[2] == 1):
        aipaddleyPos = aipaddleyPos + paddlespeed_y

    if (aipaddleyPos < 0):
        aipaddleyPos = 0
    if (aipaddleyPos > window_height - paddle_height):
        aipaddleyPos = window_height - paddle_height
    return aipaddleyPos

# Updating the learning paddle position.
def updatelearningPaddle(learningpaddleyPos, ballyPos):
    # Move down if ball is in upper half
    if (learningpaddleyPos + paddle_height/2 < ballyPos + ball_height/2):
        learningpaddleyPos = learningpaddleyPos + paddlespeed_y

    # Move the ball up if the ball is in the lower half
    if (learningpaddleyPos + paddle_height/2 > ballyPos + ball_height/2):
        learningpaddleyPos = learningpaddleyPos - paddlespeed_y

    if (learningpaddleyPos < 0):
        learningpaddleyPos = 0

    if (learningpaddleyPos > window_height - paddle_height):
        learningpaddleyPos = window_height - paddle_height
    return learningpaddleyPos

# Defining the game class.
class Pong:
    def __init__(self):
        # We choos a random direction for the ball
        num = random.randint(0,9)
        # Keeping track of the score
        self.tally = 0
        # Paddle positions are
        self.aipaddleyPos = window_height/2 - paddle_height/2
        self.learningpaddleyPos = window_height/2 - paddle_height/2

        # Ball direction
        self.ballxDir = 1
        self.ballyDir = 1

        # Defining the starting point of the ball
        self.ballxPos = window_width/2 - ball_width/2

        # Deciding movement of the ball
        if (0 < num < 3):
            self.ballxDir = 1
            self.ballyDir = 1
        if (3 <= num < 5):
            self.ballxDir = -1
            self.ballyDir = 1
        if (5 <= num < 8):
            self.ballxDir = 1
            self.ballyDir = -1
        if (8 <= num < 10):
            self.ballxDir = -1
            self.ballyDir = 1

        num = random.randint(0,9)

        self.ballyPos = num * (window_height - ball_height)/9

    def getFrame(self):
        pygame.event.pump()
        screen.fill(black)

        drawAIpaddle(self.aipaddleyPos)
        drawLearningpaddle(self.learningpaddleyPos)

        drawBall(self.ballxPos, self.ballyPos)

        #copies the pixels from our surface to a 3D array. we'll use this for Reinforcement Learning
        image_data = pygame.surfarray.array3d(pygame.display.get_surface())

        pygame.display.flip()

        return image_data

    def getNextFrame(self, action):
        pygame.event.pump()
        score = 0
        screen.fill(black)

        self.aipaddleyPos = updateaiPaddle(action, self.aipaddleyPos)
        drawAIpaddle(self.aipaddleyPos)

        self.learningpaddleyPos = updatelearningPaddle(self.aipaddleyPos, self.ballyPos)
        drawLearningpaddle(self.learningpaddleyPos)

        [score, self.aipaddleyPos, self.learningpaddleyPos, self.ballxPos, self.ballxDir, self.ballyDir] = updateBallPos(self.aipaddleyPos, self.learningpaddleyPos, self.ballxPos, self.ballyPos, self.ballxDir, self.ballyDir)

        drawBall(self.ballxPos, self.ballyPos)

        image_data = pygame.surfarray.arra3d(pygame.display.get_surface())
        # This window is updated
        pygame.display.flip()

        self.tally = self.tally + score
        print "Tally : " + str(self.tally)

        return [score, image_data]
