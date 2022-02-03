# главный цикл игры
def gameLoop():
    # загрузка изображений, инициализация машин и координат игровой машины
    background = pygame.image.load(r'resources\background.png')

    playerCar = pygame.image.load(r'resources\player_car.png')
    playerCarX = 350
    playerCarY = 495
    playerCarXChange = 0
    playerCarYChange = 0

    botCar1 = pygame.image.load(r'resources\bot_car_1.png')
    botCar2 = pygame.image.load(r'resources\bot_car_2.png')
    botCar3 = pygame.image.load(r'resources\bot_car_3.png')

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
            
        # отображение изображений
        screen.blit(background, (0, 0))

        screen.blit(playerCar, (playerCarX, playerCarY))

        screen.blit(botCar1,(200,100))
        screen.blit(botCar2,(300,100))
        screen.blit(botCar3,(400,100))

        # изменение координат игровой машины
        playerCarX += playerCarXChange
        playerCarY += playerCarYChange

        pygame.display.update()


# импорты, инициализация окна, запуск главного цикла
if __name__ == '__main__':
    import pygame
    pygame.init()
    from pygame.locals import *

    screen = pygame.display.set_mode((798, 600))
    pygame.display.set_caption('Гонка')

    logo = pygame.image.load(r'resources\logo.png')
    pygame.display.set_icon(logo)

    gameLoop()

    