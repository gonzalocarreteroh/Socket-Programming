import numpy as np

def generate_exponential_random_variables(lmbda, num_variables):
    uniform_random_variables = np.random.uniform(0, 1, num_variables)
    exponential_random_variables = -(1 / lmbda) * np.log(1 - uniform_random_variables)

    return exponential_random_variables

# Generate 1000 exponential random variables with λ=75
random_variables = generate_exponential_random_variables(75, 1000)

# Calculate mean and variance
mean = np.mean(random_variables)
variance = np.var(random_variables)

print(f"Mean: {mean}")
print(f"Variance: {variance}")
