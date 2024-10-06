import csv
import numpy as np
import matplotlib.pyplot as plt
import time  # Import the time module

def load_data(filename, columns):
    data = np.genfromtxt(filename, delimiter=',', skip_header=1, usecols=columns)
    return data.reshape(-1, 1)

price = load_data('BTC.csv', [4])

# Start timing the calculation
start_time = time.time()  # Record the start time

# Calculate returns using NumPy for faster performance
returns = np.diff(price[:, 0]) / price[:-1, 0]

threshold = float(input("Enter threshold in decimals: "))

# Create threshold movement array
threshold_movement = np.where(returns > threshold, 1, np.where(returns < -threshold, -1, 0))

def transition_probabilities(movement):
    rise = movement > 0
    fall = movement <= 0
    
    total_rise = np.sum(rise[:-1])
    total_fall = np.sum(fall[:-1])

    total_rise_to_rise = np.sum(rise[:-1] & rise[1:])
    total_rise_to_fall = np.sum(rise[:-1] & fall[1:])
    total_fall_to_rise = np.sum(fall[:-1] & rise[1:])
    total_fall_to_fall = np.sum(fall[:-1] & fall[1:])

    prob_rise_given_rise = total_rise_to_rise / total_rise if total_rise else 0
    prob_fall_given_rise = total_rise_to_fall / total_rise if total_rise else 0
    prob_rise_given_fall = total_fall_to_rise / total_fall if total_fall else 0
    prob_fall_given_fall = total_fall_to_fall / total_fall if total_fall else 0

    return np.array([prob_rise_given_rise, prob_fall_given_rise, prob_rise_given_fall, prob_fall_given_fall])

initial_transition_probs = transition_probabilities(threshold_movement)

num_iterations = int(input("Enter the number of days: "))
initial_price = float(input("Enter the initial price: "))
num_simulations = int(input("Enter the number of simulations: "))

all_simulated_prices = np.zeros((num_simulations, num_iterations + 1))
all_simulated_prices[:, 0] = initial_price

for sim in range(num_simulations):
    for i in range(num_iterations):
        if np.random.rand() < initial_transition_probs[0]:
            today_return = np.random.normal(loc=np.mean(returns), scale=np.std(returns))
        else:
            today_return = np.random.normal(loc=-np.mean(returns), scale=np.std(returns))

        new_price = all_simulated_prices[sim, i] * (1 + today_return)
        all_simulated_prices[sim, i + 1] = new_price

        last_movement = 1 if today_return > 0 else -1
        threshold_movement = np.append(threshold_movement, last_movement)
        initial_transition_probs = transition_probabilities(threshold_movement)

final_prices = all_simulated_prices[:, -1]
average_final_price = np.mean(final_prices)

# End timing the calculation
end_time = time.time()  # Record the end time
elapsed_time = end_time - start_time  # Calculate elapsed time

print(f"\nAverage final price after {num_simulations} simulations: {average_final_price:.4f}")
print(f"Elapsed time: {elapsed_time:.4f} seconds")  # Print elapsed time

plt.figure(figsize=(12, 6))
plt.plot(all_simulated_prices.T, label='Simulation')
plt.title('Monte Carlo Simulation of Price')
plt.xlabel('Days')
plt.ylabel('Price')
plt.show()
