import random
import math
import time
import threading

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Game
from django.utils import timezone

BOARD_SIZE = [800, 500]
PADDLE_SIZE = 50
PADDLE_MOVE = 5
PADDLE_SEGMENTS = 8
BALL_SPEED_INCREMENT = 1.2
BALL_SPEED_INITIAL = 4
BALL_RADIUS = 5
ANGLE_MIN = math.pi / 6
MAX_SPEED = 2222
MAX_FPS = 60
MAX_GAME_DURATION = 15 * 60 #in seconds
MAX_SCORE = 7

#PRECOMPUTATIONS, DONT CHANGE
ANGLE_PER_SEGMENT = (math.pi / 2 - ANGLE_MIN) / (PADDLE_SEGMENTS / 2 - 1)
INITIAL_PADDLES_POS = [(BOARD_SIZE[1] - PADDLE_SIZE) / 2, (BOARD_SIZE[1] - PADDLE_SIZE) / 2]
INITIAL_BALL_POS = [BOARD_SIZE[0] / 2, BOARD_SIZE[1] / 2]
MIN_PERIOD = 1 / MAX_FPS
PADDLE_PLUS_BALL = PADDLE_SIZE + BALL_RADIUS
PADDLE_SEGMENTS_TO_SIZE = PADDLE_SEGMENTS / PADDLE_SIZE
BALL_DIAMETER = BALL_RADIUS * 2
HALF_PADDLE_SEGMENTS = PADDLE_SEGMENTS // 2
BOARD_LENGTH_MINUS_PADDLE = BOARD_SIZE[1] - PADDLE_SIZE


#ball_pos is center
class GameHandler():
    def __init__(self, game_id):
        self.resetPositions(-1)
        self.score = [0, 0]
        self.lastTime = MIN_PERIOD
        self.startTime = time.time()
        self.game_id = game_id
        self.group_name = "game_" + self.game_id
        threading.Thread(target=self.startGame, daemon=True).start()

    def startGame(self):
        while not self.gameEnded():
            initialTime = time.time()
            self.moveY()
            self.moveX()
            async_to_sync(get_channel_layer().group_send) (
                self.group_name, {"type": "state.update", "state": str(self.score[0]) + " " + str(self.score[1]) + " "
                                                                + str(int(self.paddles_pos[0])) + " " + str(int(self.paddles_pos[1])) + " "
                                                                + str(int(self.ball_pos[0])) + " " + str(int(self.ball_pos[1]))}
            )
            endTime = time.time()
            ft_sleep(MIN_PERIOD - (endTime - initialTime))
            self.lastTime = time.time() - initialTime
        if (self.score[0] == self.score[1]):
            self.score[0] += 1
        self.notifyEndGame()
        self.storeResult()

    def gameEnded(self):
        return self.score[0] >= MAX_SCORE or self.score[1] >= MAX_SCORE or time.time() - self.startTime > MAX_GAME_DURATION

    def notifyEndGame(self):
        game = Game.objects.get(game_id=self.game_id)
        winner = game.user1.alias if self.score[0] > self.score[1] else game.user3.alias
        timeout = time.time() - self.startTime > MAX_GAME_DURATION

        if timeout:
            message = "Timeout"
        else:
            message = "Game ended"
        message += ", Winner: " + winner

        async_to_sync(get_channel_layer().group_send) (
            self.group_name, {"type": "end.game", "message": message}
        )

    def moveX(self):
        xpos = self.ball_pos[0] + self.ball_vector[0] * self.lastTime * MAX_FPS
        while xpos - BALL_RADIUS < 0 or xpos + BALL_RADIUS > BOARD_SIZE[0]: #has to be a while to safeguard against multiple bounces at one for insanely fast speeds
            n = 0
            if xpos - BALL_RADIUS < 0:
                if self.hitsPaddle(0):
                    xpos = -xpos + BALL_DIAMETER
                    self.paddleColision(0)
                else:
                    self.score[1] += 1
                    self.resetPositions(0)
                    return
            else:
                if self.hitsPaddle(1):
                    xpos = BOARD_SIZE[0] * 2 - xpos - BALL_DIAMETER
                    self.paddleColision(1)
                else:
                    self.score[0] += 1
                    self.resetPositions(1)
                    return
            n += 1
        self.ball_pos[0] = xpos

    def paddleColision(self, paddle):
        angle = self.segmentToAngle(int((self.ball_pos[1] - self.paddles_pos[paddle]) * PADDLE_SEGMENTS_TO_SIZE))
        norm = vectorNorm(self.ball_vector) * BALL_SPEED_INCREMENT
        norm = norm if norm < MAX_SPEED else MAX_SPEED
        self.ball_vector = [((-1) ** paddle) * math.cos(angle) * norm, -math.sin(angle) * norm]

    def hitsPaddle(self, paddle):
        return self.paddles_pos[paddle] - BALL_RADIUS <= self.ball_pos[1] and self.paddles_pos[paddle] + PADDLE_PLUS_BALL >= self.ball_pos[1]

    def moveY(self):
        ypos = self.ball_pos[1] + self.ball_vector[1] * self.lastTime * MAX_FPS
        while (ypos - BALL_RADIUS < 0 or ypos + BALL_RADIUS > BOARD_SIZE[1]): #has to be a while to safeguard against multiple bounces at one for insanely fast speeds
            if ypos - BALL_RADIUS < 0:
                ypos = -ypos + BALL_DIAMETER
            else:
                ypos = BOARD_SIZE[1] * 2 - ypos - BALL_DIAMETER
            self.ball_vector[1] = -self.ball_vector[1]
        self.ball_pos[1] = ypos

    #0 is ballto 0, 1 same for 1, -1 start
    def resetPositions(self, ball_to):
        self.paddles_pos = INITIAL_PADDLES_POS.copy()
        self.ball_pos = INITIAL_BALL_POS.copy()

        random_angle = (random.random() - 0.5) * math.pi / 2
        if ball_to == 0 or (ball_to == -1 and (random.randint(0, 1) == 0)):
            random_angle += math.pi

        self.ball_vector = [math.cos(random_angle) * BALL_SPEED_INITIAL, math.sin(random_angle) * BALL_SPEED_INITIAL]

    def setPaddlePos(self, id, key):
        if (key == "w"):
            if (self.paddles_pos[id] - PADDLE_MOVE < 0):
                return
            self.paddles_pos[id] -= PADDLE_MOVE
        elif (key == "s"):
            if (self.paddles_pos[id] + PADDLE_MOVE > BOARD_LENGTH_MINUS_PADDLE):
                return
            self.paddles_pos[id] += PADDLE_MOVE

    def segmentToAngle(self, segment):
        if (segment < 0):
            segment = 0
        elif (segment > 7):
            segment = 7
        if (segment >= HALF_PADDLE_SEGMENTS):
            segment -= 1
        return math.pi / 2 - (ANGLE_MIN + segment * ANGLE_PER_SEGMENT)
    
    def storeResult(self):
        game = Game.objects.get(game_id=self.game_id)
        game.score1 = self.score[0]
        game.score2 = self.score[1]
        game.end_time = timezone.now()
        if (self.score[0] > self.score[1]):
            game.user1.wins = game.user1.wins + 1
            game.user3.loses = game.user3.loses + 1
        else:
            game.user3.wins = game.user3.wins + 1
            game.user1.loses = game.user1.loses + 1
        game.user1.save()
        game.user3.save()
        game.save()


def vectorNorm(vec):
    return math.sqrt(pow(vec[0], 2) + pow(vec[1], 2))

def ft_sleep(secs):
    initialTime = time.time()
    endTime = time.time()
    while endTime - initialTime < secs:
        time.sleep(1/10000) #100 microsecs
        endTime = time.time()
