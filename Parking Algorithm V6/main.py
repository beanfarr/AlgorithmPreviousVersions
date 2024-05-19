import random 

class CarPark:
    def __init__(self, id, name, location, parking_spaces, handicap_spaces, ev_charging_spaces):
        self.id = id
        self.name = name
        self.location = location
        self.parking_spaces = parking_spaces  # Manually defined parking spaces matrix
        self.handicap_spaces = handicap_spaces  # Number of handicap spaces
        self.ev_charging_spaces = ev_charging_spaces  # Number of electric vehicle charging spaces

    def has_available_space(self):
        return any(space == 1 for space in self.parking_spaces)

    def has_available_specialized_space(self, space_type):
        if space_type == 'handicap':
            return self.handicap_spaces > 0
        elif space_type == 'ev_charging':
            return self.ev_charging_spaces > 0
        else:
            return False

    def display_parking_spaces(self):
        print(f"Parking spaces for {self.name}:")
        for space in self.parking_spaces:
            print(space, end=" ")
        print()

    def display_specialized_spaces(self):
        print(f"Specialized spaces for {self.name}:")
        print(f"Handicap Spaces: {self.handicap_spaces}")
        print(f"EV Charging Spaces: {self.ev_charging_spaces}")


class ParkingAlgorithm:
    def __init__(self, car_parks):
        self.car_parks = car_parks
        self.matrix_size = 10
        self.time_intervals = {
            'low': 5,
            'medium': 10,
            'high': 15
        }
        self.traffic_density = random.choice(['low', 'medium', 'high'])
        self.walk_time = 15  # Walking time between car park and destination is fixed to 15 minutes

    def calculate_time(self, start_location, end_location, traffic_density):
        x1, y1 = start_location
        x2, y2 = end_location
        time_interval = self.time_intervals[traffic_density]
        return abs(x2 - x1) * time_interval + abs(y2 - y1) * time_interval

    def generate_matrix(self, user_location, destination_location):
        matrix = [['-' for _ in range(self.matrix_size)] for _ in range(self.matrix_size)]
        for i, car_park in enumerate(self.car_parks, start=1):
            x, y = car_park.location
            matrix[x][y] = str(i)  # representing car park with numbers
        ux, uy = user_location
        dx, dy = destination_location
        matrix[ux][uy] = 'U'  # representing user
        matrix[dx][dy] = 'D'  # representing destination
        return matrix

    def find_optimal_car_park(self, user_location, destination_location, requires_specialized_space=None):
        time_to_carpark = {}  # Dictionary to store the time to reach each car park
        for car_park in self.car_parks:
            if car_park.has_available_space():
                if requires_specialized_space:
                    if not car_park.has_available_specialized_space(requires_specialized_space):
                        continue  # Skip this car park if required specialized space is not available
                drive_time = self.calculate_time(user_location, car_park.location, self.traffic_density)
                walk_time = self.calculate_time(car_park.location, destination_location,
                                                'low')  # Walking time is unaffected by traffic density
                total_time = drive_time + walk_time
                time_to_carpark[car_park] = total_time

        # Sort the car parks based on total time and filter out full car parks
        sorted_carparks = sorted(time_to_carpark.items(), key=lambda x: x[1])
        available_carparks = [car_park for car_park, time in sorted_carparks if car_park.has_available_space()]

        return available_carparks

    def simulate(self, user_location, destination_location, requires_specialized_space=None):
        # Step 4: Calculate optimal car park
        car_parks = self.find_optimal_car_park(user_location, destination_location, requires_specialized_space)

        # Step 5: Send output
        if car_parks:
            print("List of car parks in order of best option:")
            for i, car_park in enumerate(car_parks, start=1):
                print(f"{i}. {car_park.name}")
                car_park.display_specialized_spaces()  # Display specialized spaces availability
                car_park.display_parking_spaces()  # Display regular parking spaces availability
        else:
            print("No available parking spaces.")


if __name__ == "__main__":
    # Manually defining parking space matrices and specialized spaces for each car park
    car_parks_data = [
        {"id": 1, "name": "Car Park A", "location": (2, 3), "parking_spaces": [1, 1, 1, 0], "handicap_spaces": 2,
         "ev_charging_spaces": 1},
        {"id": 2, "name": "Car Park B", "location": (5, 7), "parking_spaces": [1, 1, 0, 0], "handicap_spaces": 1,
         "ev_charging_spaces": 0},
        {"id": 3, "name": "Car Park C", "location": (8, 1), "parking_spaces": [1, 1, 1, 1], "handicap_spaces": 0,
         "ev_charging_spaces": 2},
        # Add more car park data as needed
    ]

    car_parks = [CarPark(cp["id"], cp["name"], cp["location"], cp["parking_spaces"], cp["handicap_spaces"],
                         cp["ev_charging_spaces"]) for cp in car_parks_data]

    algorithm = ParkingAlgorithm(car_parks)

    # Simulate the algorithm
    user_location = (random.randint(0, 9), random.randint(0, 9))
    destination_location = (random.randint(0, 9), random.randint(0, 9))
    requires_specialized_space = random.choice(
        [None, 'handicap', 'ev_charging'])  # Randomly select if user requires specialized space

    print("User Location:", user_location)
    print("Destination Location:", destination_location)
    print("Requires Specialized Space:", requires_specialized_space)

    algorithm.simulate(user_location, destination_location, requires_specialized_space)

    # Generate and display the matrix
    print("\nMatrix:")
    matrix = algorithm.generate_matrix(user_location, destination_location)
    for row in matrix:
        print(" ".join(row))
