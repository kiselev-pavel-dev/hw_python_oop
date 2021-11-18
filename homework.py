from dataclasses import dataclass
from typing import ClassVar


@dataclass
class UnsupportedTypeTraining(Exception):
    """Исключение для неподдерживаемых типов тренировки."""
    print(Exception)


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; Длительность: '
                f'{self.duration:.3f} ч.; Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; Потрачено ккал: '
                f'{self.calories:.3f}.'
                )


@dataclass
class Training:
    """Базовый класс тренировки."""

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    action: int
    duration: float
    weight: float

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

    COEF_CALORIE_1: ClassVar[int] = 18
    COEF_CALORIE_2: ClassVar[int] = 20
    HOURS_IN_MINUTES: ClassVar[int] = 60

    def get_spent_calories(self) -> float:
        """Расчет израсходованных калорий."""
        mean_speed = self.get_mean_speed()
        temp = self.COEF_CALORIE_1 * mean_speed - self.COEF_CALORIE_2
        calorie = (temp * self.weight
                   / self.M_IN_KM * self.duration * self.HOURS_IN_MINUTES
                   )
        return calorie


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEF_1: ClassVar[float] = 0.035
    COEF_2: ClassVar[float] = 2
    COEF_3: ClassVar[float] = 0.029
    HOURS_IN_MINUTES: ClassVar[int] = 60
    height: float

    def get_spent_calories(self) -> float:
        """Расчет израсходованных калорий."""

        speed = self.get_mean_speed()
        weight = self.weight
        height = self.height
        temp = self.duration * self.HOURS_IN_MINUTES
        temp_2 = speed ** self.COEF_2 // height
        calorie = weight * ((self.COEF_1 + temp_2 * self.COEF_3)) * temp
        return calorie


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: ClassVar[float] = 1.38
    COEF_1: ClassVar[float] = 1.1
    COEF_2: ClassVar[int] = 2
    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        """Расчет средней скорости."""
        temp = self.length_pool * self.count_pool
        mean_speed = temp / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Расчет израсходованных калорий."""
        mean_speed = self.get_mean_speed()
        temp = (mean_speed + self.COEF_1) * self.COEF_2
        calorie = temp * self.weight
        return calorie

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in training_type.keys():
        raise UnsupportedTypeTraining('Неподдерживаемый тип тренировки')
    training_class = training_type[workout_type]
    training_obj = training_class(*data)
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
