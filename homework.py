
class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; Длительность: '
                f'{self.duration:.3f} ч.; Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; Потрачено ккал: '
                f'{self.calories:.3f}.'
                )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        temp = self.action
        distance = temp * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance = self.get_distance()
        mean_speed = distance / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = type(self).__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        info_obj = InfoMessage(training_type,
                               duration,
                               distance,
                               speed,
                               calories
                               )
        return info_obj


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Расчет израсходованных калорий."""
        coef_calorie_1 = 18
        coef_calorie_2 = 20
        hours_in_minutes = 60
        mean_speed = self.get_mean_speed()
        calorie = ((coef_calorie_1 * mean_speed - coef_calorie_2) * self.weight
                   / self.M_IN_KM * self.duration * hours_in_minutes
                   )
        return calorie


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Расчет израсходованных калорий."""
        coef_1 = 0.035
        coef_2 = 2
        coef_3 = 0.029
        speed = self.get_mean_speed()
        weight = self.weight
        height = self.height
        temp = self.duration * 60
        temp_2 = speed ** coef_2 // height
        calorie = weight * ((coef_1 + (temp_2) * coef_3)) * temp
        return calorie


class Swimming(Training):
    """Тренировка: плавание."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
    LEN_STEP = 1.38

    def get_mean_speed(self) -> float:
        """Расчет средней скорости."""
        temp = self.length_pool * self.count_pool
        mean_speed = temp / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Расчет израсходованных калорий."""
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2
        mean_speed = self.get_mean_speed()
        temp = (mean_speed + coeff_calorie_1) * coeff_calorie_2
        calorie = temp * self.weight
        return calorie

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type = {
        'SWM': 'Swimming',
        'RUN': 'Running',
        'WLK': 'SportsWalking'
    }
    training_temp = training_type[workout_type]
    if training_temp == 'Swimming':
        training_obj = Swimming(*data)
    elif training_temp == 'Running':
        training_obj = Running(*data)
    elif training_temp == 'SportsWalking':
        training_obj = SportsWalking(*data)
    return training_obj


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
