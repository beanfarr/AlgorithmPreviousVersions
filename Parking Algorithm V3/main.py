import numpy as np
from scipy.optimize import linear_sum_assignment

# Function to calculate normalized value using Z-Score Normalization
def z_score_normalization(value, mean, std_dev):
    return (value - mean) / std_dev

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
    normalised_carpark_availability = z_score_normalization(car_park['carpark_availability'], means['carpark_availability'], std_devs['carpark_availability'])

    # Calculate overall score using the provided weights
    score = (weights['time_to_destination'] * normalised_time_to_destination) + \
            (weights['traffic_density'] * normalised_traffic_density) + \
            (weights['carpark_availability'] * normalised_carpark_availability)

    return score

# Function to generate a sample set of car parks
def generate_sample_car_parks():
    car_parks = [
        {
            'name': 'Alpha',
            'time_to_carpark': 10,
            'time_from_carpark': 5,
            'traffic_density': 0.7,
            'carpark_availability': 0.8,
            'parking_matrix': np.array([True, False, False, False])  # One full parking space
        },
        {
            'name': 'Bravo',
            'time_to_carpark': 8,
            'time_from_carpark': 6,
            'traffic_density': 0.5,
            'carpark_availability': 0.9,
            'parking_matrix': np.array([True, True, True, True])  # One full parking space
        },
        {
            'name': 'Charlie',
            'time_to_carpark': 12,
            'time_from_carpark': 7,
            'traffic_density': 0.6,
            'carpark_availability': 0.7,
            'parking_matrix': np.array([True, True, True, True])  # One full parking space
        },
        {
            'name': 'Delta',
            'time_to_carpark': 9,
            'time_from_carpark': 4,
            'traffic_density': 0.8,
            'carpark_availability': 0.6,
            'parking_matrix': np.array([False, False, False, True])  # One full parking space
        },
        {
            'name': 'Echo',
            'time_to_carpark': 11,
            'time_from_carpark': 6,
            'traffic_density': 0.4,
            'carpark_availability': 0.5,
            'parking_matrix': np.array([True, True, True, True])  # One full parking space
        }
    ]

    return car_parks

# Function to generate a sample parking matrix (Boolean: True - occupied, False - available)
def generate_parking_matrix(num_parking_spaces, occupancy_prob=0.5):
    parking_matrix = np.random.choice([False, True], size=(num_parking_spaces,), p=[1 - occupancy_prob, occupancy_prob])
    return parking_matrix

# Function to solve the assignment problem
def solve_assignment_problem(cost_matrix):
    _, occupancy_matrix = linear_sum_assignment(cost_matrix)
    return occupancy_matrix

# Main function
def main():
    # User preferences and weights
    user_weights = {
        'time_to_destination': 0.2,
        'traffic_density': 0.3,
        'carpark_availability': 0.5
    }

    # Generate a sample set of car parks
    sample_car_parks = generate_sample_car_parks()

    # Extract mean and standard deviation for each criterion
    criteria = ['time_to_carpark', 'time_from_carpark', 'traffic_density', 'carpark_availability']
    means = {criterion: np.mean([cp[criterion] for cp in sample_car_parks if 'parking_matrix' in cp]) for criterion in criteria}
    std_devs = {criterion: np.std([cp[criterion] for cp in sample_car_parks if 'parking_matrix' in cp]) for criterion in criteria}

    # Check and print full car parks
    full_car_parks = [car_park['name'] for car_park in sample_car_parks if 'parking_matrix' in car_park and np.all(car_park['parking_matrix'])]
    if full_car_parks:
        print(f"\nFull Car Parks: {', '.join(full_car_parks)}")
    else:
        print("\nNo Full Car Parks")

    # Exclude full car parks
    non_full_car_parks = [cp for cp in sample_car_parks if 'parking_matrix' in cp and not np.all(cp['parking_matrix'])]

    # Print the generated parking matrix
    print("\nGenerated Parking Matrix:")
    for car_park in sample_car_parks:
        print(f"{car_park['name']} - Parking Matrix: {car_park.get('parking_matrix', 'N/A')}")

    # Create a cost matrix (negation of the parking matrix to convert the minimization problem to maximization)
    cost_matrix = -np.array([[calculate_score(cp, user_weights, means, std_devs) for cp in non_full_car_parks] for _ in range(len(non_full_car_parks))])

    # Solve the assignment problem to determine the optimal occupancy matrix
    occupancy_matrix = linear_sum_assignment(cost_matrix)

    # Calculate scores for each car park
    car_park_scores = []
    for car_park in non_full_car_parks:
        score = calculate_score(car_park, user_weights, means, std_devs)
        car_park_scores.append((car_park['name'], score))

    # Rank car parks based on scores
    ranked_car_parks = sorted(car_park_scores, key=lambda x: x[1], reverse=True)

    # Display ranked car parks
    print("\nRanked Car Parks:")
    for rank, (name, score) in enumerate(ranked_car_parks, start=1):
        print(f"{rank}. {name} - Score: {score:.2f}")

if __name__ == "__main__":
    main()
