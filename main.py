import pygame, sys
from random import randint
from pygame import mixer

pygame.init()
clock = pygame.time.Clock()
fps = 600

width = 700
height = 490

mixer.music.load("images/ariel.wav")
mixer.music.play(-1)
mixer.music.set_volume(0.5)

eating_sound = mixer.Sound("images/eating.wav")
hit_sound = mixer.Sound("images/shouting-yeah.wav")

screen = pygame.display.set_mode((width, height))
background = pygame.image.load("images/background1.jpg")
icon = pygame.image.load("images/star.jpeg")
pygame.display.set_icon(icon)
pygame.display.set_caption("Crab Game")
#კიბორჩხალის შემოტანა
standing = pygame.image.load("images/standing.png")
moving1_right = pygame.image.load("images/moving1.png")
moving2_right = pygame.image.load("images/moving2.png")
images = [standing, moving1_right, moving2_right]
class Crab(pygame.sprite.Sprite):
    def __init__(self, images, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = images[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y
        self.speed = 0
        self.score = 0
        self.counter = 0

    def update(self):
        global run
        self.rect.center = [self.x, self.y]
        self.x += self.speed
        self.counter += 1
        if self.counter >= 5:
            self.counter = 0

        if self.speed == 0:
            self.image = images[0]
        elif self.speed > 0:
            if self.counter <= 2:
                self.image = images[1]
            elif self.counter > 2:
                self.image = images[2]
        elif self.speed < 0:
            if self.counter <= 2:
                self.image = pygame.transform.flip(images[1], True, False)
            elif self.counter > 2:
                self.image = pygame.transform.flip(images[2], True, False)
        #საზღვრის კოდი
        if self.x < 50:
            self.x = 50
        if self.x > width - 50:
            self.x = width - 50
        #სიცოცხლის შემოწმება
        if self.score < 0:
            self.kill()
            run = False

crab = Crab(images, width/2, 400)

crabs_group = pygame.sprite.Group()
crabs_group.add(crab)

#საკვების შემოტანა
meat_image = pygame.image.load("images/meat.png")
meat_image = pygame.transform.scale(meat_image, (55, 75))
class Food(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.speed = 0.2

    def update(self):
        self.rect.center = [self.x, self.y]
        self.y += self.speed
        if self.rect.collidepoint(crab.x, crab.y):
            crab.score += 1
            eating_sound.play()
        if self.y > height or self.rect.collidepoint(crab.x, crab.y):
            self.x = randint(50, width - 50)
            self.y = randint(-700, -100)


foods_group = pygame.sprite.Group()
for i in range(4):
    meat = Food(meat_image, randint(50, width-50), randint(-700, -100))
    foods_group.add(meat)



#ჩანგლის შემოტანა
fork_image = pygame.image.load("images/fork.png")
fork_image = pygame.transform.rotate(fork_image, 225)
fork_image = pygame.transform.scale(fork_image, (100, 100))
class Fork(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.speed = 0.3

    def update(self):
        self.rect.center = [self.x, self.y]
        self.y += self.speed
        if crab.rect.collidepoint(self.x, self.y):
            crab.score -= 5
            hit_sound.play()
        if self.y > height or crab.rect.collidepoint(self.x, self.y):
            self.x = randint(50, width - 50)
            self.y = randint(-700, -100)

fork = Fork(fork_image, randint(50, width-50), randint(-700, -100))
fork_group = pygame.sprite.Group()
fork_group.add(fork)

#ქულის ეკრანზე გამოტანა
font = pygame.font.Font(None, 60)
def show_score(font):
    text = font.render(f"Score: {crab.score}", True, (200, 50, 0))
    text_rect = text.get_rect(center=[width/2, 50])
    screen.blit(text, text_rect)
#გამე ოვერის ფუნქცია
font1 = pygame.font.Font(None, 100)
def game_over(font):
    text = font.render("Game Over!", True, (0, 0, 0))
    text_rect = text.get_rect(center=[width/2, height/2])
    screen.blit(text, text_rect)
run = True
while run:
    clock.tick(fps)
    screen.blit(background, (0, 0))
    crabs_group.draw(screen)
    crabs_group.update()
    foods_group.draw(screen)
    foods_group.update()
    fork_group.draw(screen)
    fork_group.update()
    show_score(font)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                crab.speed = 0.2
            if event.key == pygame.K_LEFT:
                crab.speed = -0.2
        if event.type == pygame.KEYUP:
            crab.speed = 0

    pygame.display.update()

game_over(font1)
pygame.display.update()
pygame.time.wait(3000)
pygame.quit()
sys.exit()