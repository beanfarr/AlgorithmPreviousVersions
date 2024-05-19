import random
import numpy as np
from scipy.optimize import linear_sum_assignment
from tabulate import tabulate

# Function to calculate time between two positions
def calculate_time(position1, position2):
    time_to_move = 5  # 5 minutes to move between elements
    return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1]) * time_to_move

# Function to generate a sample set of car parks with positions
def generate_sample_car_parks(user_position=None, destination_position=None):
    user_weights = {
        'time_to_destination': 0.8,
        'traffic_density': 0.0,
        'handicapped_space': 0.0,
        'family_space': 0.0,
        'ev_charging_space': 0.0
    }

    car_park_positions = {
        'Alpha': (2, 3),
        'Bravo': (5, 7),
        'Charlie': (8, 1),
        'Delta': (4, 9),
        'Echo': (1, 6)
    }

    # If user_position and destination_position are not provided, randomize them
    if user_position is None:
        user_position = random.choice(list(set(car_park_positions.values())))
    if destination_position is None:
        destination_position = random.choice(list(set(car_park_positions.values()) - {user_position}))

    car_parks = [
        {
            'name': 'Alpha',
            'time_to_carpark': calculate_time(user_position, car_park_positions['Alpha']),
            'time_from_carpark': calculate_time(car_park_positions['Alpha'], destination_position),
            'traffic_density': 0.0,
            'parking_matrix': np.array([1, 0, 0, 0]),  # One full parking space
            'handicapped_space': 0,
            'family_space': 1,
            'ev_charging_space': 1,
            'position': car_park_positions['Alpha']
        },
        {
            'name': 'Bravo',
            'time_to_carpark': calculate_time(user_position, car_park_positions['Bravo']),
            'time_from_carpark': calculate_time(car_park_positions['Bravo'], destination_position),
            'traffic_density': 0.0,
            'parking_matrix': np.array([1, 0, 0, 1]),  # One full parking space
            'handicapped_space': 1,
            'family_space': 0,
            'ev_charging_space': 1,
            'position': car_park_positions['Bravo']
        },
        {
            'name': 'Charlie',
            'time_to_carpark': calculate_time(user_position, car_park_positions['Charlie']),
            'time_from_carpark': calculate_time(car_park_positions['Charlie'], destination_position),
            'traffic_density': 0.0,
            'parking_matrix': np.array([1, 1, 1, 1]),  # One full parking space
            'handicapped_space': 1,
            'family_space': 1,
            'ev_charging_space': 0,
            'position': car_park_positions['Charlie']
        },
        {
            'name': 'Delta',
            'time_to_carpark': calculate_time(user_position, car_park_positions['Delta']),
            'time_from_carpark': calculate_time(car_park_positions['Delta'], destination_position),
            'traffic_density': 0.0,
            'parking_matrix': np.array([0, 0, 0, 1]),  # One full parking space
            'handicapped_space': 0,
            'family_space': 0,
            'ev_charging_space': 1,
            'position': car_park_positions['Delta']
        },
        {
            'name': 'Echo',
            'time_to_carpark': calculate_time(user_position, car_park_positions['Echo']),
            'time_from_carpark': calculate_time(car_park_positions['Echo'], destination_position),
            'traffic_density': 0.0,
            'parking_matrix': np.array([1, 1, 0, 1]),  # One full parking space
            'handicapped_space': 1,
            'family_space': 1,
            'ev_charging_space': 1,
            'position': car_park_positions['Echo']
        }
    ]

    return car_parks, car_park_positions, user_weights

# Function to generate a sample parking matrix (binary: 0 - available, 1 - occupied)
def generate_parking_matrix(num_parking_spaces, occupancy_prob=0.5):
    parking_matrix = np.random.choice([0, 1], size=(num_parking_spaces,), p=[1 - occupancy_prob, occupancy_prob])
    return parking_matrix

# Function to solve the assignment problem
def solve_assignment_problem(cost_matrix):
    _, occupancy_matrix = linear_sum_assignment(cost_matrix)
    return occupancy_matrix

# Function to recommend parking based on user and destination positions
def recommend_parking(user_position, car_park_positions, ranked_car_parks, full_car_parks):
    # Extract indices of non-full car parks
    non_full_indices = [idx for idx, (car_park, _) in enumerate(ranked_car_parks) if car_park['name'] not in full_car_parks]

    # Sort non-full car parks based on their distance to the user position
    non_full_car_parks_sorted = sorted(non_full_indices, key=lambda idx: calculate_time(ranked_car_parks[idx][0]['position'], user_position))

    # Choose the first non-full car park as the recommended one
    recommended_index = non_full_car_parks_sorted[0] if non_full_car_parks_sorted else None

    # Get the recommended car park position along with the name
    recommended_car_park_info = ranked_car_parks[recommended_index] if recommended_index is not None else None

    return recommended_car_park_info, recommended_index, non_full_indices


# Function to calculate normalized value using Z-Score Normalization
def z_score_normalization(value, mean, std_dev):
    if std_dev == 0 or np.isnan(mean) or np.isnan(std_dev):
        return 0  # Return 0 for invalid cases
    try:
        result = (value - mean) / std_dev
        if not np.isfinite(result):
            print(f"Invalid result in z_score_normalization: {result}")
            print(f"value: {value}, mean: {mean}, std_dev: {std_dev}")
            return 0  # Return 0 if the result is NaN or inf
        return result
    except Exception as e:
        print(f"Error in z_score_normalization: {e}")
        return 0  # Return 0 in case of any exception

# Function to calculate overall score for a car park
def calculate_score(car_park, weights, means, std_devs):
    # Assuming the car_park dictionary contains values for each criterion
    # Modify this based on your actual data structure

    # Calculate normalized values for each criterion using Z-Score Normalization
    normalised_time_to_carpark = z_score_normalization(car_park['time_to_carpark'], means['time_to_carpark'], std_devs['time_to_carpark'])
    normalised_time_from_carpark = z_score_normalization(car_park['time_from_carpark'], means['time_from_carpark'], std_devs['time_from_carpark'])

    # Sum of time_to_carpark and time_from_carpark as time_to_destination
    normalised_time_to_destination = normalised_time_to_carpark + normalised_time_from_carpark

    normalised_traffic_density = z_score_normalization(car_park['traffic_density'], means['traffic_density'], std_devs['traffic_density'])

    # Additional spaces
    normalised_handicapped_space = z_score_normalization(car_park['handicapped_space'], means['handicapped_space'], std_devs['handicapped_space'])
    normalised_family_space = z_score_normalization(car_park['family_space'], means['family_space'], std_devs['family_space'])
    normalised_ev_charging_space = z_score_normalization(car_park['ev_charging_space'], means['ev_charging_space'], std_devs['ev_charging_space'])

    # Calculate overall score using the provided weights
    score = (weights['time_to_destination'] * normalised_time_to_destination) + \
            (weights['traffic_density'] * normalised_traffic_density) + \
            (weights['handicapped_space'] * normalised_handicapped_space) + \
            (weights['family_space'] * normalised_family_space) + \
            (weights['ev_charging_space'] * normalised_ev_charging_space)

    return score

# Main function
def main():
    # Generate a sample set of car parks
    result = generate_sample_car_parks(user_position=None, destination_position=None)
    sample_car_parks, car_park_positions, user_weights = result[0], result[1], result[2]

    # Randomize user and destination positions excluding car park locations
    available_positions = set([(x, y) for x in range(11) for y in range(11)]) - set(car_park_positions.values())
    user_position = random.choice(list(available_positions))
    destination_position = random.choice(list(available_positions - {user_position}))

    print(f"User Position: {user_position}")
    print(f"Destination Position: {destination_position}")

    # Check and print full car parks
    full_car_parks = [car_park['name'] for car_park in sample_car_parks if 'parking_matrix' in car_park and np.all(car_park['parking_matrix'] == 1)]
    if full_car_parks:
        print(f"\nFull Car Parks: {', '.join(full_car_parks)}")
    else:
        print("\nNo Full Car Parks")

    # Exclude full car parks
    non_full_car_parks = [cp for cp in sample_car_parks if 'parking_matrix' in cp and not np.all(cp['parking_matrix'] == 1)]

    # Print the generated parking matrix and special spaces
    print("\nGenerated Parking Matrix:")
    for car_park in sample_car_parks:
        print(f"{car_park['name']} - Parking Matrix: {car_park.get('parking_matrix', 'N/A')}")
        print(f"  Handicapped Space: {car_park['handicapped_space']}")
        print(f"  Family Space: {car_park['family_space']}")
        print(f"  EV Charging Space: {car_park['ev_charging_space']}")
        print(f"  Position: {car_park['position']}")

    # Print the Location Matrix in a grid using tabulate
    print("\nLocation Matrix:")
    location_matrix = np.zeros((11, 11), dtype=str)
    location_matrix[user_position] = 'U'  # User
    location_matrix[destination_position] = 'X'  # Destination
    for car_park in car_park_positions:
        location_matrix[car_park_positions[car_park]] = car_park[0]  # First letter of car park name

    headers = [''] + [f'Col {i+1}' for i in range(11)]
    table = tabulate(location_matrix, headers, showindex=[f'Row {i+1}' for i in range(11)], tablefmt='grid')
    print(table)

    # Extract mean and standard deviation for each criterion
    criteria = ['time_to_carpark', 'time_from_carpark', 'traffic_density', 'handicapped_space', 'family_space', 'ev_charging_space']
    means = {criterion: np.mean([cp[criterion] for cp in sample_car_parks if 'parking_matrix' in cp]) for criterion in criteria}
    std_devs = {criterion: np.std([cp[criterion] for cp in sample_car_parks if 'parking_matrix' in cp]) for criterion in criteria}

    # Create a cost matrix (negation of the parking matrix to convert the minimization problem to maximization)
    cost_matrix = -np.array([[calculate_score(cp, user_weights, means, std_devs) for cp in non_full_car_parks] for _ in range(len(non_full_car_parks))])

    # Solve the assignment problem to determine the optimal occupancy matrix
    occupancy_matrix = solve_assignment_problem(cost_matrix)

    # Rank car parks based on scores
    car_park_scores = []
    for car_park in non_full_car_parks:
        score = calculate_score(car_park, user_weights, means, std_devs)
        car_park_scores.append((car_park, score))

    # Rank car parks based on scores
    ranked_car_parks = sorted(car_park_scores, key=lambda x: x[1], reverse=True)

    # Display ranked car parks
    print("\nRanked Car Parks:")
    for rank, (name, score) in enumerate(ranked_car_parks, start=1):
        print(f"{rank}. {name['name']} - Score: {score:.2f}")

    # Integrate the recommendation algorithm
    car_park_positions = [car_park['position'] for car_park in sample_car_parks]
    full_car_parks = [car_park['name'] for car_park in sample_car_parks if
                          'parking_matrix' in car_park and np.all(car_park['parking_matrix'] == 1)]
    # Call recommend_parking with full_car_parks and user_position
    recommended_car_park_info, recommended_index, non_full_indices = recommend_parking(user_position, car_park_positions, ranked_car_parks, full_car_parks)
    if recommended_car_park_info is not None:
        recommended_car_park_name = recommended_car_park_info[0]['name']
        recommended_car_park_position = recommended_car_park_info[0]['position']
        print("\nRecommended Car Park Position:")
        print(f"{recommended_car_park_name} - Position: {recommended_car_park_position}")
    else:
        print("\nNo recommended car parks.")

if __name__ == "__main__":
    main()