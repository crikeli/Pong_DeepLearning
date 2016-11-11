import pygame #helps us make GUI games in python
import random #help us define which direction the ball will start moving in

#frame rate per second
FPS = 60

#size of our window
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

#size of our paddle
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60
#distance from the edge of the window
PADDLE_BUFFER = 10

#size of our ball
BALL_WIDTH = 10
BALL_HEIGHT = 10

#speeds of our paddle and ball
PADDLE_SPEED = 2
BALL_X_SPEED = 3
BALL_Y_SPEED = 2

#RGB colors for our paddle and ball
WHITE = (255, 255, 255)
GREEN = (124,252,0)
SALMON = (255,160,122)
BLACK = (0, 0, 0)

#initialize our screen using width and height vars
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#draw our ball
def drawBall(ballXPos, ballYPos):
    #small rectangle, create it
    ball = pygame.Rect(ballXPos, ballYPos, BALL_WIDTH, BALL_HEIGHT)
    #draw it
    pygame.draw.rect(screen, WHITE, ball)


def drawLearningPaddle(LearningPaddleYPos):
    #crreate it
    LearningPaddle = pygame.Rect(PADDLE_BUFFER, LearningPaddleYPos, PADDLE_WIDTH, PADDLE_HEIGHT)
    #draw it
    pygame.draw.rect(screen, SALMON, LearningPaddle)


def drawAIPaddle(AIPaddleYPos):
    #create it, opposite side
    AIPaddle = pygame.Rect(WINDOW_WIDTH - PADDLE_BUFFER - PADDLE_WIDTH, AIPaddleYPos, PADDLE_WIDTH, PADDLE_HEIGHT)
    #draw it
    pygame.draw.rect(screen, GREEN, AIPaddle)


#update the ball, using the paddle posistions the balls positions and the balls directions
def updateBall(LearningPaddleYPos, AIPaddleYPos, ballXPos, ballYPos, ballXDirection, ballYDirection):

    #update the x and y position
    ballXPos = ballXPos + ballXDirection * BALL_X_SPEED
    ballYPos = ballYPos + ballYDirection * BALL_Y_SPEED
    score = 0

    #checks for a collision, if the ball hits the left side, our learning agent
    if (
                        ballXPos <= PADDLE_BUFFER + PADDLE_WIDTH and ballYPos + BALL_HEIGHT >= LearningPaddleYPos and ballYPos - BALL_HEIGHT <= LearningPaddleYPos + PADDLE_HEIGHT):
        #switches directions
        ballXDirection = 1
    #past it
    elif (ballXPos <= 0):
        #negative score
        ballXDirection = 1
        score = -1
        return [score, LearningPaddleYPos, AIPaddleYPos, ballXPos, ballYPos, ballXDirection, ballYDirection]

    #check if hits the other side
    if (
                        ballXPos >= WINDOW_WIDTH - PADDLE_WIDTH - PADDLE_BUFFER and ballYPos + BALL_HEIGHT >= AIPaddleYPos and ballYPos - BALL_HEIGHT <= AIPaddleYPos + PADDLE_HEIGHT):
        #switch directions
        ballXDirection = -1
    #past it
    elif (ballXPos >= WINDOW_WIDTH - BALL_WIDTH):
        #positive score
        ballXDirection = -1
        score = 1
        return [score, LearningPaddleYPos, AIPaddleYPos, ballXPos, ballYPos, ballXDirection, ballYDirection]

    #if it hits the top
    #move down
    if (ballYPos <= 0):
        ballYPos = 0;
        ballYDirection = 1;
    #if it hits the bottom, move up
    elif (ballYPos >= WINDOW_HEIGHT - BALL_HEIGHT):
        ballYPos = WINDOW_HEIGHT - BALL_HEIGHT
        ballYDirection = -1
    return [score, LearningPaddleYPos, AIPaddleYPos, ballXPos, ballYPos, ballXDirection, ballYDirection]

#update the paddle position
def updateLearningPaddle(action, LearningPaddleYPos):
    #if move up
    if (action[1] == 1):
        LearningPaddleYPos = LearningPaddleYPos - PADDLE_SPEED
    #if move down
    if (action[2] == 1):
        LearningPaddleYPos = LearningPaddleYPos + PADDLE_SPEED

    #don't let it move off the screen
    if (LearningPaddleYPos < 0):
        LearningPaddleYPos = 0
    if (LearningPaddleYPos > WINDOW_HEIGHT - PADDLE_HEIGHT):
        LearningPaddleYPos = WINDOW_HEIGHT - PADDLE_HEIGHT
    return LearningPaddleYPos


def updateAIPaddle(AIPaddleYPos, ballYPos):
    #move down if ball is in upper half
    if (AIPaddleYPos + PADDLE_HEIGHT/2 < ballYPos + BALL_HEIGHT/2):
        AIPaddleYPos = AIPaddleYPos + PADDLE_SPEED
    #move up if ball is in lower half
    if (AIPaddleYPos + PADDLE_HEIGHT/2 > ballYPos + BALL_HEIGHT/2):
        AIPaddleYPos = AIPaddleYPos - PADDLE_SPEED
    #don't let it hit top
    if (AIPaddleYPos < 0):
        AIPaddleYPos = 0
    #dont let it hit bottom
    if (AIPaddleYPos > WINDOW_HEIGHT - PADDLE_HEIGHT):
        AIPaddleYPos = WINDOW_HEIGHT - PADDLE_HEIGHT
    return AIPaddleYPos


#game class
class PongGame:
    def __init__(self):
        #random number for initial direction of ball
        num = random.randint(0,9)
        #keep score
        self.tally = 0
        #initialie positions of paddle
        self.LearningPaddleYPos = WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2
        self.AIPaddleYPos = WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2
        #and ball direction
        self.ballXDirection = 1
        self.ballYDirection = 1
        #starting point
        self.ballXPos = WINDOW_WIDTH/2 - BALL_WIDTH/2

        #randomly decide where the ball will move
        if(0 < num < 3):
            self.ballXDirection = 1
            self.ballYDirection = 1
        if (3 <= num < 5):
            self.ballXDirection = -1
            self.ballYDirection = 1
        if (5 <= num < 8):
            self.ballXDirection = 1
            self.ballYDirection = -1
        if (8 <= num < 10):
            self.ballXDirection = -1
            self.ballYDirection = -1
        #new random number
        num = random.randint(0,9)
        #where it will start, y part
        self.ballYPos = num*(WINDOW_HEIGHT - BALL_HEIGHT)/9

    #
    def getPresentFrame(self):
        #for each frame, calls the event queue, like if the main window needs to be repainted
        pygame.event.pump()
        #make the background black
        screen.fill(BLACK)
        #draw our paddles
        drawLearningPaddle(self.LearningPaddleYPos)
        drawAIPaddle(self.AIPaddleYPos)
        #draw our ball
        drawBall(self.ballXPos, self.ballYPos)
        #copies the pixels from our surface to a 3D array. we'll use this for RL
        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        #updates the window
        pygame.display.flip()
        #return our surface data
        return image_data

    #update our screen
    def getNextFrame(self, action):
        pygame.event.pump()
        score = 0
        screen.fill(BLACK)
        #update our paddle
        self.LearningPaddleYPos = updateLearningPaddle(action, self.LearningPaddleYPos)
        drawLearningPaddle(self.LearningPaddleYPos)
        #update evil AI paddle
        self.AIPaddleYPos = updateAIPaddle(self.AIPaddleYPos, self.ballYPos)
        drawAIPaddle(self.AIPaddleYPos)
        #update our vars by updating ball position
        [score, self.LearningPaddleYPos, self.AIPaddleYPos, self.ballXPos, self.ballYPos, self.ballXDirection, self.ballYDirection] = updateBall(self.LearningPaddleYPos, self.AIPaddleYPos, self.ballXPos, self.ballYPos, self.ballXDirection, self.ballYDirection)
        #draw the ball
        drawBall(self.ballXPos, self.ballYPos)
        #get the surface data
        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        #update the window
        pygame.display.flip()
        #record the total score
        self.tally = self.tally + score
        print "Tally is " + str(self.tally)
        #return the score and the surface data
        return [score, image_data]
