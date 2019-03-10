import csv, os, sys

class CarBase:
    csv_car_type = 0
    csv_brand = 1
    csv_passenger_seats_count = 2
    csv_photo_file_name = 3
    csv_body_whl = 4
    csv_carrying = 5
    csv_extra = 6

    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)
    
    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]

    
class Car(CarBase):
    car_type = 'car'
    
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)
    
    @classmethod
    def instance(cls, row):
        return cls(
            row[cls.csv_brand],
            row[cls.csv_photo_file_name],
            row[cls.csv_carrying],
            row[cls.csv_passenger_seats_count]
        )


class Truck(CarBase):
    car_type = 'truck'
    
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        try:
            self.body_height, self.body_length, self.body_width = (float(i) for i in body_whl.lower().split("x", 2))
        except ValueError:
            self.body_length = 0.0
            self.body_width = 0.0
            self.body_height = 0.0
    
    def get_body_volume(self):
        return self.body_height * self.body_length * self.body_width
    
    @classmethod
    def instance(cls, row):
        return cls(
            row[cls.csv_brand],
            row[cls.csv_photo_file_name],
            row[cls.csv_carrying],
            row[cls.csv_body_whl]
        )

class SpecMachine(CarBase):
    car_type = 'spec_machine'
    
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra

    @classmethod
    def instance(cls, row):
        return cls(
            row[cls.csv_brand],
            row[cls.csv_photo_file_name],
            row[cls.csv_carrying],
            row[cls.csv_extra]
        )

def get_car_list(csv_filename):
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        car_list = []
        class_dict = {
            car_class.car_type: car_class for car_class in (Car, Truck, SpecMachine)
        }
        for row in reader:
            try:
                car_type = row[CarBase.csv_car_type]
            except IndexError:
                #пропускаем пустые строки
                continue
            try:
                car_list.append(class_dict[car_type].instance(row))
            except (KeyError, ValueError, IndexError):
                continue

    
    return car_list
    
print(get_car_list(sys.argv[1]))