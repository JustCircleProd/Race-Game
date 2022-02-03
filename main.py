# отчёт перед началом игры
def startCountdown():
    countdownBackground = pygame.image.load(r'resources\blur_background.png')
    timerFont = pygame.font.Font(r'resources\NotoSans-Bold.ttf', 70)

    for i in reversed(range(0, 4)):
        screen.blit(countdownBackground, (0, 0))
        if i != 0:
            text = timerFont.render(str(i), True, (210, 0, 158))
            screen.blit(text, (350, 250))
        else:
            text = timerFont.render("Вперёд!", True, (210, 0, 158))
            screen.blit(text, (220, 250))

        pygame.display.update()
        time.sleep(1)

    gameLoop()


# главный цикл игры
def gameLoop():
    # запуск фоновой музыки и инициализация звука стоклновения
    pygame.mixer.music.load(r'resources\background_music.mp3')
    pygame.mixer.music.play()

    crashSound = pygame.mixer.Sound(r'resources\crash_sound.mp3')

    # инициализация счёта, шрифта, загрузка изображений
    # инициализация машин и их координат
    score = 0
    highscore = readHighscore()
    fontScore = pygame.font.Font(r'resources\NotoSans-Bold.ttf', 30)

    background = pygame.image.load(r'resources\background.png')

    playerCar = pygame.image.load(r'resources\player_car.png')
    playerCarX = 350
    playerCarY = 495
    playerCarXChange = 0
    playerCarYChange = 0

    botCar1 = pygame.image.load(r'resources\bot_car_1.png')
    botCar1X = random.randint(178, 490)
    botCar1Y = 100
    botCar1YChange = 5

    botCar2 = pygame.image.load(r'resources\bot_car_2.png')
    botCar2X = random.randint(178, 490)
    botCar2Y = 100
    botCar2YChange = 5

    botCar3 = pygame.image.load(r'resources\bot_car_3.png')
    botCar3X = random.randint(178, 490)
    botCar3Y = 100
    botCar3YChange = 5

    run = True
    while run:
        # проверка на события
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # нажатие кнопок, по которым фиксируется изменение координат игровой машины
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    playerCarXChange += 5

                if event.key == pygame.K_LEFT:
                    playerCarXChange -= 5

                if event.key == pygame.K_UP:
                    playerCarYChange -= 5

                if event.key == pygame.K_DOWN:
                    playerCarYChange += 5

            # отжатие кнопок
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    playerCarXChange = 0

                if event.key == pygame.K_LEFT:
                    playerCarXChange = 0

                if event.key == pygame.K_UP:
                    playerCarYChange = 0

                if event.key == pygame.K_DOWN:
                    playerCarYChange = 0

        # проверка на выход игровой машины за границы
        if playerCarX < 178:
            playerCarX = 178
        if playerCarX > 490:
            playerCarX = 490

        if playerCarY < 0:
            playerCarY = 0
        if playerCarY > 495:
            playerCarY = 495

        # отображение изображений
        screen.blit(background, (0, 0))

        screen.blit(playerCar, (playerCarX, playerCarY))

        screen.blit(botCar1, (botCar1X, botCar1Y))
        screen.blit(botCar2, (botCar2X, botCar2Y))
        screen.blit(botCar3, (botCar3X, botCar3Y))

        # отображение текущего и лучшего счёта
        showScore(score, fontScore)
        showHighscore(highscore, fontScore)
        
        # изменение координат игровой машины
        playerCarX += playerCarXChange
        playerCarY += playerCarYChange

        # изменение координат вражеских машин, увеличение счёта
        botCar1Y += botCar1YChange
        botCar2Y += botCar2YChange
        botCar3Y += botCar3YChange

        if botCar1Y > 670:
            botCar1X = random.randint(178, 490)
            botCar1Y = -100
            score += 1
        if botCar2Y > 670:
            botCar2X = random.randint(178, 490)
            botCar2Y = -150
            score += 1
        if botCar3Y > 670:
            botCar3X = random.randint(178, 490)
            botCar3Y = -200
            score += 1

        # проверка на столкновение, в случае его возникновения - игра прекращается
        def isCrash(firstCarX, firstCarY, secondCarX, secondCarY):
            distance = math.sqrt(math.pow(firstCarX-secondCarX, 2) + math.pow(firstCarY - secondCarY, 2))
            return distance < 50

        if isCrash(botCar1X, botCar1Y, playerCarX, playerCarY) or \
           isCrash(botCar2X, botCar2Y, playerCarX, playerCarY) or \
           isCrash(botCar3X, botCar3Y, playerCarX, playerCarY):
           break

        pygame.display.update()

    playerCarXChange = 0
    playerCarYChange = 0
    botCar1YChange = 0
    botCar2YChange = 0
    botCar3YChange = 0

    pygame.mixer.music.stop()
    crashSound.play()

    if score > highscore:
        saveHighscore(score)

    showGameOverScreen(score, highscore)


def readHighscore():
    highscore = open(r'resources\highscore.txt', 'r').read()
    return int(highscore) if highscore else 0


def saveHighscore(score):
    open(r'resources\highscore.txt', 'w').write(str(score))


def showScore(score, fontScore):
    renderedScore = fontScore.render(f"Счёт: {score}", True, (0, 163, 252))
    screen.blit(renderedScore, (570, 280))


def showHighscore(highscore, fontScore):
    renderedHighscore = fontScore.render(f"Рекорд: {highscore}", True, (210, 0, 158))
    screen.blit(renderedHighscore, (570, 310))


def showGameOverScreen(score, highscore):
    gameOverBackground = pygame.image.load(r'resources\gameover_screen.png')
    gameOverFont = pygame.font.Font(r'resources\NotoSans-Bold.ttf', 44)
    run = True

    screen.blit(gameOverBackground,(0,0))
    time.sleep(0.5)

    renderedScore = gameOverFont.render(f"Счёт: {score}", True, (0, 163, 252))
    screen.blit(renderedScore, (320, 230))
    time.sleep(0.5)

    renderedHighscore = gameOverFont.render(f"Рекорд: {highscore}", True, (210, 0, 158))
    screen.blit(renderedHighscore, (280, 280))
    pygame.display.update()

    while run:
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
             if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    startCountdown()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()



# импорты, инициализация окна, запуск главного цикла
if __name__ == '__main__':
    import random
    import math
    import time
    import sys

    import pygame
    pygame.init()
    from pygame.locals import *

    screen = pygame.display.set_mode((798, 600))
    pygame.display.set_caption('Гонка')

    logo = pygame.image.load(r'resources\logo.png')
    pygame.display.set_icon(logo)

    startCountdown()
