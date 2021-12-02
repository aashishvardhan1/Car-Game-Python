from os import path
import pygame
import time
import math
from utils import scale_image, blit_rotate_center

GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("imgs/track.png"), 0.9)

TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH = pygame.image.load("imgs/finish.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (95,250)

RED_CAR = scale_image(pygame.image.load("imgs/red-car.png"), 0.45)
GREEN_CAR = scale_image(pygame.image.load("imgs/green-car.png"), 0.45)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Racing Game")

FPS = 60
PATH = [(142, 177), (139, 145), (139, 116), (137, 93), (128, 76), (118, 72), (106, 69), (94, 
65), (81, 65), (74, 71), (67, 76), (59, 81), (58, 92), (55, 99), (54, 108), (53, 116), (52, 126), (52, 134), (51, 354), (52, 360), (53, 369), (56, 379), (60, 387), (64, 394), (70, 402), (74, 409), (248, 576), (260, 580), (269, 581), (286, 582), (295, 580), (306, 571), (314, 561), (323, 550), (323, 535), (326, 518), (325, 504), (326, 485), (329, 467), (330, 447), (334, 430), (341, 416), (350, 402), (361, 394), (374, 388), (390, 386), (408, 386), (424, 389), (442, 395), (453, 399), (463, 408), (473, 426), (475, 439), (478, 454), (478, 470), (480, 485), (482, 506), (482, 519), (484, 539), (487, 558), (495, 570), (506, 577), (526, 586), (545, 586), (561, 582), (576, 574), (584, 562), (590, 546), (594, 528), (594, 500), (592, 479), (592, 455), (591, 434), (591, 409), (591, 389), (590, 366), (590, 352), (587, 333), (581, 315), (568, 308), (550, 297), (534, 295), 
(513, 294), (495, 292), (346, 290), (334, 278), (331, 262), (330, 246), (325, 226), (338, 219), (362, 212), (542, 208), (554, 207), (568, 201), (579, 188), (582, 174), (586, 155), (586, 136), (583, 74), (566, 71), (547, 70), (518, 70), (498, 66), (467, 67), (270, 58), (254, 65), (238, 73), (226, 87), (224, 103), (224, 122), (219, 284), (218, 293), (214, 294), 
(214, 304), (214, 309), (203, 319), (187, 324), (173, 330), (155, 324), (146, 306), (141, 284)]

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()
    
    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal
    
    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0


class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (150,200)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration/2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel*0.8
        self.move()

class ComputerCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (120,200)

    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel

    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5)

    def draw(self, win):
        super().draw(win)
        self.draw_points(win)


def draw(win, images, player_car, computer_car):
    for img, pos in images:
        win.blit(img, pos) 

    player_car.draw(win)
    computer_car.draw(win)
    pygame.display.update()

def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_SPACE]:
        player_car.reduce_speed()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()
    
    if not moved:
        player_car.reduce_speed()


run = True
clock = pygame.time.Clock()
images = [(GRASS, (0,0)), (TRACK, (0,0)), (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]
player_car = PlayerCar(4, 4)
computer_car = ComputerCar(4, 4, PATH)

while run:
    clock.tick(FPS)

    draw(WIN, images, player_car, computer_car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break


    move_player(player_car)

    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()

    finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POSITION)
    if finish_poi_collide != None:
        if finish_poi_collide[1] == 0:
            player_car.bounce()
        else:
            player_car.reset()
            print("FINISHED")

print(computer_car.path)
pygame.quit()