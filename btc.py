import csv
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont


def load_data(filename, columns):
    """
    Loads data from a btc.csv file and puts into columns.
    """

    mylist = []
    with open(filename, 'r') as file:  # Open the file in read mode
        data = csv.reader(file, delimiter=',')  # Create a CSV reader object
        next(data)  # Skip the header row
        for row in data:
            column = [float(row[i]) for i in columns]  # Convert each element to float
            mylist.append(column)
    return mylist


def calculate_probabilities(threshold):
    """
    Calculates transition probabilities for Bitcoin price movements based on a threshold.
    """

    price = load_data('BTC.csv', [4])  # Load closing price data from the fourth column

    # Calculate daily returns
    returns = []
    for i in range(1, len(price)):
        returns.append((price[i][0] / price[i-1][0]) - 1)

    # Categorize price movements based on the threshold
    threshold_movement = [
        1 if return_value > threshold else -1 if return_value < -threshold else 0
        for return_value in returns
    ]

    # Separate price movements into positive and negative groups
    positive_next_day_movement = []
    negative_next_day_movement = []
    for i in range(1, len(threshold_movement)):
        if threshold_movement[i-1] == 1:
            positive_next_day_movement.append(returns[i])
        elif threshold_movement[i-1] == -1:
            negative_next_day_movement.append(returns[i])

    # Calculate probabilities for positive and negative change groups
    (
        prob_rise_given_rise_pos,
        prob_fall_given_rise_pos,
        prob_rise_given_fall_pos,
        prob_fall_given_fall_pos,
        rise_to_fall_pos,
        rise_to_rise_pos,
        fall_to_rise_pos,
        fall_to_fall_pos,
        total_rise_pos,
        total_fall_pos
    ) = transition_probabilities(positive_next_day_movement)

    (
        prob_rise_given_rise_neg,
        prob_fall_given_rise_neg,
        prob_rise_given_fall_neg,
        prob_fall_given_fall_neg,
        rise_to_fall_neg,
        rise_to_rise_neg,
        fall_to_rise_neg,
        fall_to_fall_neg,
        total_rise_neg,
        total_fall_neg
    ) = transition_probabilities(negative_next_day_movement)

    # Display the calculated results in a GUI window
    show_results(threshold, prob_rise_given_rise_pos, prob_fall_given_rise_pos,
                 rise_to_rise_pos, rise_to_fall_pos, total_rise_pos,
                 prob_rise_given_fall_neg, prob_fall_given_fall_neg,
                 fall_to_rise_neg, fall_to_fall_neg, total_fall_neg)


def transition_probabilities(movement):
    """
    Calculates transition probabilities from price movements.


    movement (list) list of price change values.
    """

    total_rise_to_rise = sum(1 for i in range(1, len(movement)) if movement[i-1] > 0 and movement[i] > 0)
    total_rise_to_fall = sum(1 for i in range(1, len(
