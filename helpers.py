from math import degrees, atan


def collinear(v1, v2, l1, l2, epsilon=1e-08):
    if not l1 or not l2:
        # нулевой вектор не может быть коллинеарным
        return False
    unit_v1 = [v1[0] / l1, v1[1] / l1, v1[2] / l1]
    unit_v2 = [v2[0] / l2, v2[1] / l2, v2[2] / l2]
    return unit_v1[0] - epsilon < unit_v2[0] < unit_v1[0] + epsilon and unit_v1[1] - epsilon < unit_v2[1] < unit_v1[
        1] + epsilon and unit_v1[2] - epsilon < unit_v2[2] < unit_v1[2] + epsilon


def sort(x, y):
    if x == y == 0:
        return 91  # выделяем для этого отдельный сектор в массиве.
    if x == 0 and y < 0: return -90
    if x == 0 and y > 0: return 90
    return int(degrees(atan(y / x)))


def howLong(x1, y1, z1, x2, y2, z2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5


def appendToExcludeVectors(x1, y1, z1, x2, y2, z2, arr, target_x, target_y, target_z, target_length, answer):
    # заносит все уникальные вектора в список и считает количество занесенных векторов, указывающих до цели.
    # ИДЕЯ ДЛЯ ОПТИМИЗАЦИИ: сразу записывать в список единичные вектора unit_v1???
    vector = [x2 - x1, y2 - y1, z2 - z1]
    target_vector = [target_x - x1, target_y - y1, target_z - z1]
    sector1, sector2, sector3 = sort(vector[1], vector[0]), \
                                sort(vector[2], vector[0]), \
                                sort(vector[2], vector[1])
    ar = arr[sector1][sector2][sector3]
    sector1, sector2, sector3 = sort(target_vector[1], target_vector[0]), \
                                sort(target_vector[2], target_vector[0]), \
                                sort(target_vector[2], target_vector[1])
    target_arr = arr[sector1][sector2][sector3]
    length = howLong(x1, y1, z1, x2, y2, z2)
    new_vector = [vector, length, True]
    new_target = [target_vector, target_length, False]
    for i in range(len(target_arr)):
        a = target_arr[i]
        v = a[0]

        if collinear([v[0], v[1], v[2]], [target_vector[0], target_vector[1], target_vector[2]], a[1], target_length):
            if target_length < a[1]:
                # если длина нового вектора меньше - значит старый не выполняет требования задачи.
                is_old_self = a[2]
                target_arr[i] = new_target
                if is_old_self:
                    # вектор до цели пересекает цель раньше, чем это ранее делал вектор до отражения самого себя
                    answer += 1
                    break
                else:
                    # вектор до цели пересекает цель раньше, чем это ранее делал вектор до отражения самого себя
                    break
            else:
                # этот вектор уже пересекался с чем-то раньше. он нам больше не интересен
                break
    else:
        # вектор без препятствий доходит до цели
        answer += 1
        target_arr.append(new_target)

    for i in range(len(ar)):
        a = ar[i]
        v = a[0]
        if collinear([v[0], v[1], v[2]], [vector[0], vector[1], vector[2]], a[1], length):
            if length < a[1]:
                is_old_self = a[2]
                ar[i] = new_vector
                if not is_old_self:
                    # вектор до своего отражения достигает раньше, чем ранее засчитанный вектор до цели. Вычитаем ранее засчитанный вектор до цели.
                    answer -= 1
                    return answer
                else:
                    return answer
            else:
                return answer
    else:
        ar.append(new_vector)
        return answer
