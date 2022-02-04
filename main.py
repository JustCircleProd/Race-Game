class Constants:
    SCREEN_WIDTH = 798
    SCREEN_HEIGHT = 600

    MAIN_COLOR = (210, 0, 158)
    SECOND_COLOR = (0, 163, 252)


# показ стартового экрана
def showStartScreen():
    # отображение фона, создание кнопок и текста для них
    startBackground = pygame.image.load(r'resources\start_screen.png')
    screen.blit(startBackground, (0, 0))

    fontBtn = pygame.font.Font(r'resources\NotoSans-Bold.ttf', 30)

    playText = fontBtn.render("Играть", True, Constants.SECOND_COLOR)
    instructionText = fontBtn.render("Инструкция", True, Constants.SECOND_COLOR)
    quitText = fontBtn.render("Выход", True, Constants.SECOND_COLOR)

    screen.blit(playText, (120, 440))
    screen.blit(instructionText, (300, 440))
    screen.blit(quitText, (580, 440))

    playBtn = pygame.Rect(100, 440, 150, 50)
    instructionBtn = pygame.Rect(280, 440, 240, 50)
    quitBtn = pygame.Rect(560, 440, 150, 50)

    run = True

    while run:
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True

        mouseX, mouseY = pygame.mouse.get_pos()

        if isInteraction(playBtn, mouseX, mouseY, clicked):
            run = False
            startGame()

        if isInteraction(instructionBtn, mouseX, mouseY, clicked):
            run = False
            showInstructionScreen()
     
        if isInteraction(quitBtn, mouseX, mouseY, clicked):
            run = False

        pygame.display.update()


# функция для проверки было ли взаимодействие с кнопкой
# её анимация и возврат ответа: была ли кликнута кнопка
def isInteraction(button, mouseX, mouseY, clicked):
    if button.collidepoint(mouseX, mouseY):
            pygame.draw.rect(screen, Constants.MAIN_COLOR, button, 5)
            if clicked:
                return True
    else:  
        pygame.draw.rect(screen, Constants.SECOND_COLOR, button, 5)

    return False


# показ экрана с инструкцией
def showInstructionScreen():
    instructionBackground = pygame.image.load(r'resources\instruction_screen.png')
    screen.blit(instructionBackground, (0, 0))

    fontBtn = pygame.font.Font(r'resources\NotoSans-Bold.ttf', 30)

    backText = fontBtn.render("Назад", True, Constants.SECOND_COLOR)
    screen.blit(backText, (350, 500))
    backBtn = pygame.Rect(309, 500, 180, 50)

    run = True

    while run:
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True

        mouseX, mouseY = pygame.mouse.get_pos()

        if isInteraction(backBtn, mouseX, mouseY, clicked):
            run = False
            showStartScreen()

        pygame.display.update()


# отчёт перед началом игры
def startGame():
    countdownBackground = pygame.image.load(r'resources\blur_background.png')
    timerFont = pygame.font.Font(r'resources\NotoSans-Bold.ttf', 70)

    for i in reversed(range(0, 4)):
        screen.blit(countdownBackground, (0, 0))
        if i != 0:
            text = timerFont.render(str(i), True, Constants.SECOND_COLOR)
            screen.blit(text, (350, 250))
        else:
            text = timerFont.render("Вперёд!", True, Constants.MAIN_COLOR)
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

    valueForChangeBotSpeed = [15, 50, 90, 140, 200, 300, 450, 700, 1000, 1400, 2000, 2700]

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
        renderedScore = fontScore.render(f"Счёт: {score}", True, Constants.SECOND_COLOR)
        screen.blit(renderedScore, (570, 280))

        renderedHighscore = fontScore.render(f"Рекорд: {highscore}", True, Constants.MAIN_COLOR)
        screen.blit(renderedHighscore, (570, 310))
        
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

        if score in valueForChangeBotSpeed:
            botCar1YChange += 0.6
            botCar2YChange += 0.6
            botCar3YChange += 0.6
            valueForChangeBotSpeed.remove(score)

        # проверка на столкновение, в случае его возникновения - игра прекращается
        def isCrash(firstCarX, firstCarY, secondCarX, secondCarY):
            distance = math.sqrt(math.pow(firstCarX-secondCarX, 2) + math.pow(firstCarY - secondCarY, 2))
            return distance < 50

        if isCrash(botCar1X, botCar1Y, playerCarX, playerCarY) or \
           isCrash(botCar2X, botCar2Y, playerCarX, playerCarY) or \
           isCrash(botCar3X, botCar3Y, playerCarX, playerCarY):
           break

        pygame.display.update()

    # если произошла авария, сбрасываем все координаты движения
    # останавливаем музыку, включаем звук аварии
    # сохраняем счёт, показываем экран окончания игры
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


# показ экрана окончания игры
def showGameOverScreen(score, highscore):
    gameOverBackground = pygame.image.load(r'resources\gameover_screen.png')
    gameOverFont = pygame.font.Font(r'resources\NotoSans-Bold.ttf', 44)
    run = True

    screen.blit(gameOverBackground,(0,0))
    time.sleep(0.5)

    renderedScore = gameOverFont.render(f"Счёт: {score}", True, Constants.SECOND_COLOR)
    renderedScoreRect = renderedScore.get_rect(center=(Constants.SCREEN_WIDTH / 2, Constants.SCREEN_HEIGHT / 2 - 25))
    screen.blit(renderedScore, renderedScoreRect)
    time.sleep(0.5)

    renderedHighscore = gameOverFont.render(f"Рекорд: {highscore}", True, Constants.MAIN_COLOR)
    renderedHighscoreRect = renderedHighscore.get_rect(center=(Constants.SCREEN_WIDTH / 2, Constants.SCREEN_HEIGHT / 2 + 25))
    screen.blit(renderedHighscore, renderedHighscoreRect)

    fontBtn = pygame.font.Font(r'resources\NotoSans-Bold.ttf', 30)

    playAgainText = fontBtn.render("Играть снова", True, Constants.SECOND_COLOR)
    backToMenuText = fontBtn.render("Выход в меню", True, Constants.SECOND_COLOR)
    screen.blit(playAgainText, (150, 440))
    screen.blit(backToMenuText, (425, 440))

    playAgainBtn = pygame.Rect(140, 440, 230, 50)
    backToMenuBtn = pygame.Rect(415, 440, 250, 50)

    while run:
        clicked = False
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
             if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True

        mouseX, mouseY = pygame.mouse.get_pos()

        if isInteraction(playAgainBtn, mouseX, mouseY, clicked):
            run = False
            startGame()

        if isInteraction(backToMenuBtn, mouseX, mouseY, clicked):
            run = False
            showStartScreen()

        pygame.display.update()


# импорты, инициализация окна, запуск главного цикла
if __name__ == '__main__':
    import random
    import math
    import time
    import sys

    import pygame
    pygame.init()
    from pygame.locals import *

    screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
    pygame.display.set_caption('Гонка 2D')

    logo = pygame.image.load(r'resources\logo.png')
    pygame.display.set_icon(logo)

    showStartScreen()
