import random
import math


def generate_exponential_random_variables(lmbda, num_variables):
    exponential_random_variables = []

    # Generate num_variables exponential random variables
    for _ in range(num_variables):
        # Generate a uniform random variable between 0 and 1
        uniform_random_variable = random.uniform(0, 1)

        # Calculate the exponential random variable using the inverse transform method
        exponential_random_variable = -(1 / lmbda) * math.log(1 - uniform_random_variable)

        # Add the exponential random variable to the list
        exponential_random_variables.append(exponential_random_variable)

    return exponential_random_variables


# Generate 1000 exponential random variables with λ=75
random_variables = generate_exponential_random_variables(75, 1000)

# Calculate the mean of the generated random variables
mean = sum(random_variables) / len(random_variables)

# Calculate the variance of the generated random variables using the unbiased formula
variance = sum((x - mean) ** 2 for x in random_variables) / (len(random_variables) - 1)

# Print the calculated mean and variance
print(f"Mean: {mean}")
print(f"Variance: {variance}")
