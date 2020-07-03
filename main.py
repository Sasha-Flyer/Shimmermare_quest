from copy import deepcopy
from time import time
from helpers import *

def main():
    count = 0
    x, y, z = map(int, input("введите длину граней куба x, y, z через пробел \n").split())
    d = int(input("введите максимальное расстояние луча \n"))
    self_x, self_y, self_z = map(int, input("введите ваши координаты через пробел \n").split())
    target_x, target_y, target_z = map(int, input("введите координаты цели через пробел \n").split())
    start_point_x, start_point_y, start_point_z = self_x, self_y, self_z
    self_points = []
    target_points = []
    exclude_vectors = [[[[]for i in range(181)] for x in range(181)] for y in range(181)]
    # храним все направления векторов до цели и до своего отражения в формате [вектор, расстояние, своё_отражение?],
    # разбив их по секторам с точностью до градуса
    self_points.append([self_x, self_y, self_z])
    target_points.append([target_x, target_y, target_z])
    bottom_x = 0
    top_x = x

    current_top_selfx = self_x
    current_bot_selfx = self_x

    current_top_targetx = target_x
    current_bot_targetx = target_x
    while abs(bottom_x) <= d + x or top_x <= d + x:
        # отражаем исходный куб в одном направлении
        top_limit = False
        current_top_selfx = top_x + abs(top_x - current_top_selfx)
        current_top_targetx = top_x + abs(top_x - current_top_targetx)
        l = howLong(*self_points[0], current_top_targetx, target_y, target_z)
        if l <= d:
            self_points.append([current_top_selfx, self_y, self_z])
            target_points.append([current_top_targetx, target_y, target_z])
            count = appendToExcludeVectors(start_point_x, start_point_y, start_point_z, current_top_selfx, self_y, self_z, exclude_vectors, current_top_targetx, target_y, target_z, l, count)
        else:
            top_limit = True
        top_x += x
        current_bot_selfx = bottom_x - abs(bottom_x - current_bot_selfx)
        current_bot_targetx = bottom_x - abs(bottom_x - current_bot_targetx)
        l = howLong(*self_points[0], current_bot_targetx, target_y, target_z)
        if l <= d:
            self_points.append([current_bot_selfx, self_y, self_z])
            target_points.append([current_bot_targetx, target_y, target_z])
            count = appendToExcludeVectors(start_point_x, start_point_y, start_point_z, current_bot_selfx, self_y, self_z, exclude_vectors, current_bot_targetx, target_y, target_z, l, count)
        elif top_limit:
            break
        bottom_x -= x
    copy = deepcopy(zip(self_points, target_points))
    for (self_x, self_y, self_z), (target_x, target_y, target_z) in copy:
        # теперь отражаем исходный куб и ранние отражения во втором направлении
        bottom_y = 0
        top_y = y
        current_top_selfy = self_y
        current_bot_selfy = self_y
        current_top_targety = target_y
        current_bot_targety = target_y

        while abs(bottom_y) <= d + y or top_y <= d + y:
            top_limit = False
            current_top_selfy = top_y + abs(top_y - current_top_selfy)
            current_top_targety = top_y + abs(top_y - current_top_targety)
            l = howLong(*self_points[0], target_x, current_top_targety, target_z)
            if l <= d:
                self_points.append([self_x, current_top_selfy, self_z])
                target_points.append([target_x, current_top_targety, target_z])
                count = appendToExcludeVectors(start_point_x, start_point_y, start_point_z, self_x, current_top_selfy, self_z, exclude_vectors, target_x, current_top_targety, target_z, l, count)
            else:
                top_limit = True
            top_y += y
            current_bot_selfy = bottom_y - abs(bottom_y - current_bot_selfy)
            current_bot_targety = bottom_y - abs(bottom_y - current_bot_targety)
            l = howLong(*self_points[0], target_x, current_bot_targety, target_z)
            if l <= d:
                self_points.append([self_x, current_bot_selfy, self_z])
                target_points.append([target_x, current_bot_targety, target_z])
                count = appendToExcludeVectors(start_point_x, start_point_y, start_point_z, self_x, current_bot_selfy, self_z, exclude_vectors, target_x, current_bot_targety, target_z, l, count)
            elif top_limit:
                break
            bottom_y -= y
    copy = deepcopy(zip(self_points, target_points))
    for (self_x, self_y, self_z), (target_x, target_y, target_z) in copy:
        # теперь отражаем исходный куб и ранние отражения во третьем направлении
        bottom_z = 0
        top_z = z
        current_top_selfz = self_z
        current_bot_selfz = self_z
        current_top_targetz = target_z
        current_bot_targetz = target_z
        while abs(bottom_z) <= d + z or top_z <= d + z:
            top_limit = False
            current_top_selfz = top_z + abs(top_z - current_top_selfz)
            current_top_targetz = top_z + abs(top_z - current_top_targetz)
            l = howLong(*self_points[0], target_x, target_y, current_top_targetz)
            if l <= d:
                self_points.append([self_x, self_y, current_top_selfz])
                target_points.append([target_x, target_y, current_top_targetz])
                count = appendToExcludeVectors(start_point_x, start_point_y, start_point_z, self_x, self_y, current_top_selfz, exclude_vectors, target_x, target_y, current_top_targetz, l, count)
            else:
                top_limit = True
            top_z += z
            current_bot_selfz = bottom_z - abs(bottom_z - current_bot_selfz)
            current_bot_targetz = bottom_z - abs(bottom_z - current_bot_targetz)
            l = howLong(*self_points[0], target_x, target_y, current_bot_targetz)
            if l <= d:
                self_points.append([self_x, self_y, current_bot_selfz])
                target_points.append([target_x, target_y, current_bot_targetz])
                count = appendToExcludeVectors(start_point_x, start_point_y, start_point_z, self_x, self_y, current_bot_selfz, exclude_vectors,  target_x, target_y, current_bot_targetz, l, count)
            elif top_limit:
                break
            bottom_z -= z
    return count


if __name__ == "__main__":
    t = (time())
    answer = main()
    print(answer)
    print("время выполнения: ", time() - t)
