import mysql.connector
import random

class CarPark:
    def __init__(self, id, name, location, parking_spaces, handicap_spaces, ev_charging_spaces):
        self.id = id
        self.name = name
        self.location = location
        self.parking_spaces = parking_spaces
        self.handicap_spaces = handicap_spaces
        self.ev_charging_spaces = ev_charging_spaces

    def has_available_space(self):
        return any(space == 1 for space in self.parking_spaces)

    def has_available_specialized_space(self, space_type):
        if space_type == 'handicap':
            return self.handicap_spaces > 0
        elif space_type == 'ev_charging':
            return self.ev_charging_spaces > 0
        else:
            return False

class ParkingAlgorithm:
    def __init__(self, connection):
        self.connection = connection
        self.time_intervals = {
            'low': 5,
            'medium': 10,
            'high': 15
        }
        self.walk_time = 15

    def fetch_car_parks_from_database(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM car_parks")
        car_parks = []
        for row in cursor.fetchall():
            car_parks.append(CarPark(row['id'], row['name'], (row['location_x'], row['location_y']),
                                      list(map(int, row['parking_spaces'].split(','))), row['handicap_spaces'],
                                      row['ev_charging_spaces']))
        cursor.close()
        return car_parks

    def calculate_time(self, start_location, end_location, traffic_density):
        x1, y1 = start_location
        x2, y2 = end_location
        time_interval = self.time_intervals[traffic_density]
        return abs(x2 - x1) * time_interval + abs(y2 - y1) * time_interval

    def find_optimal_car_park(self, user_location, destination_location, requires_specialized_space=None):
        car_parks = self.fetch_car_parks_from_database()
        time_to_carpark = {}
        for car_park in car_parks:
            if car_park.has_available_space():
                if requires_specialized_space:
                    if not car_park.has_available_specialized_space(requires_specialized_space):
                        continue
                drive_time = self.calculate_time(user_location, car_park.location, self.traffic_density)
                walk_time = self.calculate_time(car_park.location, destination_location, 'low')
                total_time = drive_time + walk_time
                time_to_carpark[car_park] = total_time

        sorted_carparks = sorted(time_to_carpark.items(), key=lambda x: x[1])
        available_carparks = [car_park for car_park, time in sorted_carparks if car_park.has_available_space()]
        return available_carparks

    def simulate(self, user_location, destination_location, requires_specialized_space=None):
        car_parks = self.find_optimal_car_park(user_location, destination_location, requires_specialized_space)
        if car_parks:
            print("List of car parks in order of best option:")
            for i, car_park in enumerate(car_parks, start=1):
                print(f"{i}. {car_park.name}")
                print(f"Location: {car_park.location}")
                print(f"Parking Spaces: {car_park.parking_spaces}")
                print(f"Handicap Spaces: {car_park.handicap_spaces}")
                print(f"EV Charging Spaces: {car_park.ev_charging_spaces}")
                print()
        else:
            print("No available parking spaces.")

if __name__ == "__main__":
    connection = mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="your_database"
    )
    algorithm = ParkingAlgorithm(connection)

    user_location = (random.randint(0, 9), random.randint(0, 9))
    destination_location = (random.randint(0, 9), random.randint(0, 9))
    requires_specialized_space = random.choice([None, 'handicap', 'ev_charging'])

    print("User Location:", user_location)
    print("Destination Location:", destination_location)
    print("Requires Specialized Space:", requires_specialized_space)

    algorithm.simulate(user_location, destination_location, requires_specialized_space)

    connection.close()
