# класс для хранения констант
class Constants:
    SCREEN_WIDTH = 798
    SCREEN_HEIGHT = 600

    MAIN_COLOR = (210, 0, 158)
    SECOND_COLOR = (0, 163, 252)

    BOT_CHANGE_Y = 0.6

    ROAD_LEFT_BORDER_X = 178
    ROAD_RIGHT_BORDER_X = 490

    PLAYER_TOP_BORDER = 0
    PLAYER_BOTTOM_BORDER = 495

    BOT_BOTTOM_BORDER = 670

    SCORES_FOR_INCREASE_BOT_SPEED = [15, 50, 90, 140, 200, 300, 450, 700, 1000, 1400, 2000, 2700, 4000, 5700]


# показ стартового экрана
def showStartScreen():
    # отображение фона, инициализация звука нажатия по кнопка
    # создание кнопок и текста для них
    startBackground = pygame.image.load(r'resources\start_screen.png')
    screen.blit(startBackground, (0, 0))

    clickSound = pygame.mixer.Sound(r'resources\click_sound.mp3')

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

    # цикл для работы программы
    while run:
        clicked = False
        # проверка на события выхода и клика
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True

        # по координатам мыши узнаём находится ли она в области кнопки и был ли клик
        mouseX, mouseY = pygame.mouse.get_pos()

        if isInteraction(playBtn, mouseX, mouseY, clicked):
            clickSound.play()
            pygame.mixer.music.stop()
            startGame()
            run = False

        if isInteraction(instructionBtn, mouseX, mouseY, clicked):
            clickSound.play()
            showInstructionScreen()
            run = False
     
        if isInteraction(quitBtn, mouseX, mouseY, clicked):
            clickSound.play()
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

    clickSound = pygame.mixer.Sound(r'resources\click_sound.mp3')

    fontBtn = pygame.font.Font(r'resources\NotoSans-Bold.ttf', 30)

    backText = fontBtn.render("Назад", True, Constants.SECOND_COLOR)
    screen.blit(backText, (350, 500))
    backBtn = pygame.Rect(309, 500, 180, 50)

    run = True

    # цикл для работы программы
    while run:
        clicked = False
        # проверка на события выхода и клика
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True

        # по координатам мыши узнаём находится ли она в области кнопки и был ли клик
        mouseX, mouseY = pygame.mouse.get_pos()

        if isInteraction(backBtn, mouseX, mouseY, clicked):
            clickSound.play()
            showStartScreen()
            run = False

        pygame.display.update()


# отчёт перед началом игры и запуск игры
def startGame():
    countdownBackground = pygame.image.load(r'resources\blur_background.png')
    timerFont = pygame.font.Font(r'resources\NotoSans-Bold.ttf', 70)

    countdownSound = pygame.mixer.Sound(r'resources\countdown_sound.mp3')
    countdownSound.play()

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
    # инициализация звука стоклновения
    pygame.mixer.music.play()
    crashSound = pygame.mixer.Sound(r'resources\crash_sound.mp3')
    increaseSpeedSound = pygame.mixer.Sound(r'resources\increase_speed_sound.mp3')

    # инициализация счёта, рекорда, шрифта, загрузка изображений
    score = 0
    highscore = readHighscore()
    fontScore = pygame.font.Font(r'resources\NotoSans-Bold.ttf', 30)

    background = pygame.image.load(r'resources\background.png')

    # инициализация машин и их координат
    playerCarImage = pygame.image.load(r'resources\player_car.png')
    playerCar = Car(playerCarImage, 350, 495, 0, 0)
    
    botCar1Image = pygame.image.load(r'resources\bot_car_1.png')
    botCar1 = Car(botCar1Image, random.randint(Constants.ROAD_LEFT_BORDER_X, Constants.ROAD_RIGHT_BORDER_X), 100, 0, 5)
    
    botCar2Image = pygame.image.load(r'resources\bot_car_2.png')
    botCar2 = Car(botCar2Image, random.randint(Constants.ROAD_LEFT_BORDER_X, Constants.ROAD_RIGHT_BORDER_X), 100, 0, 5)

    botCar3Image = pygame.image.load(r'resources\bot_car_3.png')
    botCar3 = Car(botCar3Image, random.randint(Constants.ROAD_LEFT_BORDER_X, Constants.ROAD_RIGHT_BORDER_X), 100, 0, 5)

    # инициализация списка счётов, когда скорость машин увеличивается
    valueForChangeBotSpeed = Constants.SCORES_FOR_INCREASE_BOT_SPEED

    run = True

    while run:
        # проверка на события
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # нажатие кнопок, по которым фиксируется изменение координат игровой машины
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    playerCar.changeX += 5
                if event.key == pygame.K_LEFT:
                    playerCar.changeX -= 5
                if event.key == pygame.K_UP:
                    playerCar.changeY -= 5
                if event.key == pygame.K_DOWN:
                    playerCar.changeY += 5

            # отжатие кнопок
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    playerCar.changeX = 0
                if event.key == pygame.K_LEFT:
                    playerCar.changeX = 0
                if event.key == pygame.K_UP:
                    playerCar.changeY = 0
                if event.key == pygame.K_DOWN:
                    playerCar.changeY = 0

        # проверка на выход игровой машины за границы
        if playerCar.X < Constants.ROAD_LEFT_BORDER_X:
            playerCar.X = Constants.ROAD_LEFT_BORDER_X
        if playerCar.X > Constants.ROAD_RIGHT_BORDER_X:
            playerCar.X = Constants.ROAD_RIGHT_BORDER_X

        if playerCar.Y < Constants.PLAYER_TOP_BORDER:
            playerCar.Y = Constants.PLAYER_TOP_BORDER
        if playerCar.Y > Constants.PLAYER_BOTTOM_BORDER:
            playerCar.Y = Constants.PLAYER_BOTTOM_BORDER

        # отображение изображений
        screen.blit(background, (0, 0))

        screen.blit(playerCar.image, (playerCar.X, playerCar.Y))

        screen.blit(botCar1.image, (botCar1.X, botCar1.Y))
        screen.blit(botCar2.image, (botCar2.X, botCar2.Y))
        screen.blit(botCar3.image, (botCar3.X, botCar3.Y))

        # отображение текущего и лучшего счёта
        renderedScore = fontScore.render(f"Счёт: {score}", True, Constants.SECOND_COLOR)
        screen.blit(renderedScore, (570, 280))

        renderedHighscore = fontScore.render(f"Рекорд: {highscore}", True, Constants.MAIN_COLOR)
        screen.blit(renderedHighscore, (570, 310))
        
        # изменение координат игровой машины
        playerCar.move()

        # изменение координат вражеских машин
        botCar1.move()
        botCar2.move()
        botCar3.move()

        # увеличение счёта и сброс координат вражеских машин
        if botCar1.Y > Constants.BOT_BOTTOM_BORDER:
            botCar1.resetPosition(random.randint(178, 490), -100)
            score += 1
        if botCar2.Y > Constants.BOT_BOTTOM_BORDER:
            botCar2.resetPosition(random.randint(178, 490), -150)
            score += 1
        if botCar3.Y > Constants.BOT_BOTTOM_BORDER:
            botCar3.resetPosition(random.randint(178, 490), -200)
            score += 1

        # увеличение скорости вражеских машин
        if score in valueForChangeBotSpeed:
            increaseSpeedSound.play()
            botCar1.increaseSpeed(Constants.BOT_CHANGE_Y)
            botCar2.increaseSpeed(Constants.BOT_CHANGE_Y)
            botCar3.increaseSpeed(Constants.BOT_CHANGE_Y)
            valueForChangeBotSpeed.remove(score)

        # проверка на столкновение машины игрока с другими машинами
        if playerCar.isCrash(botCar1) or playerCar.isCrash(botCar2) or playerCar.isCrash(botCar3):
            run = False

        pygame.display.update()

    # если произошла авария
    # сбрасываем все координаты движения
    playerCar.resetPosition(0, 0)
    botCar1.resetPosition(0, 0)
    botCar2.resetPosition(0, 0)
    botCar3.resetPosition(0, 0)

    # останавливаем фоновую музыку, включаем звук столкновения
    pygame.mixer.music.stop()
    crashSound.play()

    # если нужно сохраняем счёт
    if score > highscore:
        saveHighscore(score)

    # показ экрана с результатами через 1 секунду
    time.sleep(1)

    showResultScreen(score, highscore)


# возвращает лучший результат из файла или 0, если его не было
def readHighscore():
    highscore = open(r'resources\highscore.txt', 'r').read()
    return int(highscore) if highscore else 0


def saveHighscore(score):
    open(r'resources\highscore.txt', 'w').write(str(score))


# показ экрана окончания игры
def showResultScreen(score, highscore):
    # прогрузка изображения, шрифта, звука нажатия кнопки
    resultBackground = pygame.image.load(r'resources\result_screen.png')
    resultFont = pygame.font.Font(r'resources\NotoSans-Bold.ttf', 44)

    clickSound = pygame.mixer.Sound(r'resources\click_sound.mp3')

    # показ изображения
    screen.blit(resultBackground,(0,0))

    pygame.display.update()
    time.sleep(0.5)

    # проигрывание звука и показ счёта после 0.5 секунд
    resultSound = pygame.mixer.Sound(r'resources\result_sound.mp3')
    resultSound.play()

    renderedScore = resultFont.render(f"Счёт: {score}", True, Constants.SECOND_COLOR)
    renderedScoreRect = renderedScore.get_rect(center=(Constants.SCREEN_WIDTH / 2, Constants.SCREEN_HEIGHT / 2 - 25))
    screen.blit(renderedScore, renderedScoreRect)

    pygame.display.update()
    time.sleep(1)

    # показ рекорда после 1 секунды
    renderedHighscore = resultFont.render(f"Рекорд: {highscore}", True, Constants.MAIN_COLOR)
    renderedHighscoreRect = renderedHighscore.get_rect(center=(Constants.SCREEN_WIDTH / 2, Constants.SCREEN_HEIGHT / 2 + 25))
    screen.blit(renderedHighscore, renderedHighscoreRect)

    pygame.display.update()
    time.sleep(1)

    # прогрузка кнопок после 1 секунды
    fontBtn = pygame.font.Font(r'resources\NotoSans-Bold.ttf', 30)

    playAgainText = fontBtn.render("Играть снова", True, Constants.SECOND_COLOR)
    backToMenuText = fontBtn.render("Выход в меню", True, Constants.SECOND_COLOR)
    screen.blit(playAgainText, (150, 440))
    screen.blit(backToMenuText, (425, 440))

    playAgainBtn = pygame.Rect(140, 440, 230, 50)
    backToMenuBtn = pygame.Rect(415, 440, 250, 50)

    run = True

    while run:
        clicked = False
        # события на выход и кнопки
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
             if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True

        mouseX, mouseY = pygame.mouse.get_pos()
        
        if isInteraction(playAgainBtn, mouseX, mouseY, clicked):
            clickSound.play()
            startGame()
            run = False

        if isInteraction(backToMenuBtn, mouseX, mouseY, clicked):
            clickSound.play()
            showStartScreen()
            run = False

        pygame.display.update()


# импорты, инициализация окна, запуск стартового экрана и фоновой музыки
if __name__ == '__main__':
    import random
    import time
    import sys

    import pygame
    pygame.init()
    from pygame.locals import *

    from Car import Car

    screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
    pygame.display.set_caption('Гонка 2D')

    logo = pygame.image.load(r'resources\logo.png')
    pygame.display.set_icon(logo)

    pygame.mixer.music.load(r'resources\background_music.mp3')
    pygame.mixer.music.play()

    showStartScreen()
