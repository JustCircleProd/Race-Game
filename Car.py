import math

# класс машины имеет поля изображения, координаты X, Y и скорости её изменения
class Car:
    def __init__(self, image, X, Y, changeX, changeY):
        self.image = image
        self.X = X
        self.Y = Y
        self.changeX = changeX
        self.changeY = changeY

    # двигает машину на её изменение
    def move(self):
        self.X += self.changeX
        self.Y += self.changeY

    # проверка на столкновение с другой машиной
    def isCrash(self, car):
        distance = math.sqrt(math.pow(self.X - car.X, 2) + math.pow(self.Y - car.Y, 2))
        return distance < 50

    # увеличение скорости для вражеских машин
    def increaseSpeed(self, value):
        self.changeY += value

    # поменять позицию машины
    def resetPosition(self, X, Y):
        self.X = X
        self.Y = Y
