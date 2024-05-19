import random


# Function to calculate normalized value using Z-Score Normalization
def z_score_normalisation(value, mean, std_dev):
    return (value - mean) / std_dev


# Function to calculate overall score for a car park
def calculate_score(car_park, weights, means, std_dev):
    # Assuming the car_park dictionary contains values for each criterion
    # Modify this based on your actual data structure

    # Calculate normalized values for each criterion using Z-Score Normalization
    normalised_time_to_destination = z_score_normalisation(car_park['time_to_destination'],
                                                           means['time_to_destination'],
                                                           std_dev['time_to_destination'])
    normalised_time_to_carpark = z_score_normalisation(car_park['time_to_carpark'], means['time_to_carpark'],
                                                        std_dev['time_to_carpark'])
    normalised_time_from_carpark = z_score_normalisation(car_park['time_from_carpark'], means['time_from_carpark'],
                                                          std_dev['time_from_carpark'])
    normalised_traffic_density = z_score_normalisation(car_park['traffic_density'], means['traffic_density'],
                                                       std_dev['traffic_density'])
    normalised_carpark_availability = z_score_normalisation(car_park['carpark_availability'],
                                                            means['carpark_availability'],
                                                            std_dev['carpark_availability'])

    # Calculate overall score using the provided weights
    score = (weights['time_to_destination'] * normalised_time_to_destination) + \
            (weights['time_to_carpark'] * normalised_time_to_carpark) + \
            (weights['time_from_carpark'] * normalised_time_from_carpark) + \
            (weights['traffic_density'] * normalised_traffic_density) + \
            (weights['carpark_availability'] * normalised_carpark_availability)

    return score


# Function to generate a sample set of car parks
def generate_sample_car_parks(num_car_parks):
    sample_car_parks = []
    for _ in range(num_car_parks):
        car_park = {
            'time_to_destination': random.uniform(5, 30),
            'time_to_carpark': random.uniform(2, 15),
            'time_from_carpark': random.uniform(2, 15),
            'traffic_density': random.uniform(0.1, 1),
            'carpark_availability': random.uniform(0.1, 1),
        }
        sample_car_parks.append(car_park)
    return sample_car_parks


# Main function
def main():
    # User preferences and weights
    user_weights = {
        'time_to_destination': 0.2,
        'time_to_carpark': 0.15,
        'time_from_carpark': 0.15,
        'traffic_density': 0.3,
        'carpark_availability': 0.2
    }

    # Generate a sample set of car parks
    num_car_parks = 5
    sample_car_parks = generate_sample_car_parks(num_car_parks)

    # Extract mean and standard deviation for each criterion
    means = {criterion: sum(cp[criterion] for cp in sample_car_parks) / num_car_parks for criterion in
             user_weights.keys()}
    std_devs = {
        criterion: (sum((cp[criterion] - means[criterion]) ** 2 for cp in sample_car_parks) / num_car_parks) ** 0.5 for
        criterion in user_weights.keys()}

    # Calculate scores for each car park
    car_park_scores = []
    for index, car_park in enumerate(sample_car_parks, start=1):
        score = calculate_score(car_park, user_weights, means, std_devs)
        car_park_scores.append((index, score))

    # Rank car parks based on scores
    ranked_car_parks = sorted(car_park_scores, key=lambda x: x[1], reverse=True)

    # Display ranked car parks
    print("Ranked Car Parks:")
    for rank, (index, score) in enumerate(ranked_car_parks, start=1):
        print(f"{rank}. Car Park {index} - Score: {score:.2f}")


if __name__ == "__main__":
    main()
