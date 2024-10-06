import csv
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont

def load_data(filename, columns):
    mylist = []
    with open(filename) as file:
        data = csv.reader(file, delimiter=',')
        next(data)
        for row in data:
            column = [float(row[i]) for i in columns]
            mylist.append(column)
    return mylist

def calculate_probabilities(threshold):
    price = load_data('BTC.csv', [4])

    returns = []
    for i in range(1, len(price)):
        returns.append((price[i][0] / price[i-1][0]) - 1)

    threshold_movement = [
        1 if return_value > threshold else -1 if return_value < -threshold else 0
        for return_value in returns
    ]

    positive_next_day_movement = []
    negative_next_day_movement = []
    for i in range(1, len(threshold_movement)):
        if threshold_movement[i-1] == 1:
            positive_next_day_movement.append(returns[i])
        elif threshold_movement[i-1] == -1:
            negative_next_day_movement.append(returns[i])

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

    show_results(threshold, prob_rise_given_rise_pos, prob_fall_given_rise_pos,
                 rise_to_rise_pos, rise_to_fall_pos, total_rise_pos,
                 prob_rise_given_fall_neg, prob_fall_given_fall_neg,
                 fall_to_rise_neg, fall_to_fall_neg, total_fall_neg)

def transition_probabilities(movement):
    total_rise_to_rise = sum(1 for i in range(1, len(movement)) if movement[i-1] > 0 and movement[i] > 0)
    total_rise_to_fall = sum(1 for i in range(1, len(movement)) if movement[i-1] > 0 and movement[i] <= 0)
    total_fall_to_rise = sum(1 for i in range(1, len(movement)) if movement[i-1] <= 0 and movement[i] > 0)
    total_fall_to_fall = sum(1 for i in range(1, len(movement)) if movement[i-1] <= 0 and movement[i] <= 0)

    total_rise = sum(1 for i in range(len(movement)) if movement[i-1] > 0)
    total_fall = sum(1 for i in range(len(movement)) if movement[i-1] <= 0)

    prob_rise_given_rise = total_rise_to_rise / total_rise if total_rise else 0
    prob_fall_given_rise = total_rise_to_fall / total_rise if total_rise else 0

    prob_rise_given_fall = total_fall_to_rise / total_fall if total_fall else 0
    prob_fall_given_fall = total_fall_to_fall / total_fall if total_fall else 0

    return (
        prob_rise_given_rise,
        prob_fall_given_rise,
        prob_rise_given_fall,
        prob_fall_given_fall,
        total_rise_to_fall,
        total_rise_to_rise,
        total_fall_to_rise,
        total_fall_to_fall,
        total_rise,
        total_fall
    )

def show_results(threshold, prob_rise_given_rise_pos, prob_fall_given_rise_pos,
                 rise_to_rise_pos, rise_to_fall_pos, total_rise_pos,
                 prob_rise_given_fall_neg, prob_fall_given_fall_neg,
                 fall_to_rise_neg, fall_to_fall_neg, total_fall_neg):

    results_window = tk.Toplevel()
    results_window.title("Transition Probabilities")

    results_window.geometry("600x400")
    results_window.update_idletasks()

    screen_width = results_window.winfo_screenwidth()
    screen_height = results_window.winfo_screenheight()

    x = (screen_width // 2) - (results_window.winfo_width() // 2)
    y = (screen_height // 2) - (results_window.winfo_height() // 2)

    results_window.geometry(f"+{x}+{y}")

    custom_font = tkFont.Font(family="Arial", size=12)

    text = tk.Text(results_window, wrap='word', font=custom_font)
    text.pack(expand=True, fill='both')

    output = []
    output.append(f"Transition Probabilities given a {threshold * 100:.2f}% change:\n")
    
    output.append(f"After a rise greater than {threshold * 100:.2f}%:")
    output.append(f"P(Rise|Rise): {prob_rise_given_rise_pos:.4f}")
    output.append(f"P(Fall|Rise): {prob_fall_given_rise_pos:.4f}")
    output.append(f"Total Rise to Rise: {rise_to_rise_pos}")
    output.append(f"Total Rise to Fall: {rise_to_fall_pos}")
    output.append(f"Total Rise: {total_rise_pos}\n")
    
    output.append(f"After a fall greater than {threshold * 100:.2f}%:")
    output.append(f"P(Rise|Fall): {prob_rise_given_fall_neg:.4f}")
    output.append(f"P(Fall|Fall): {prob_fall_given_fall_neg:.4f}")
    output.append(f"Total Fall to Rise: {fall_to_rise_neg}")
    output.append(f"Total Fall to Fall: {fall_to_fall_neg}")
    output.append(f"Total Fall: {total_fall_neg}\n")
    
    transition_matrix = [
        [prob_rise_given_rise_pos, prob_fall_given_rise_pos],
        [prob_rise_given_fall_neg, prob_fall_given_fall_neg]
    ]
    
    output.append(f"Transition Matrix given a {threshold * 100:.2f}% change:")
    output.append("           Rise       Fall")
    output.append(f"Rise   |  {transition_matrix[0][0]:.4f}    {transition_matrix[0][1]:.4f}")
    output.append(f"Fall     |  {transition_matrix[1][0]:.4f}    {transition_matrix[1][1]:.4f}")

    for line in output:
        text.insert(tk.END, line + "\n")

    results_window.mainloop()

def start_gui():
    gui = tk.Tk()
    gui.title("Input Threshold")

    gui.geometry("400x150")
    gui.update_idletasks()

    screen_width = gui.winfo_screenwidth()
    screen_height = gui.winfo_screenheight()

    x = (screen_width // 2) - (gui.winfo_width() // 2)
    y = (screen_height // 2) - (gui.winfo_height() // 2)

    gui.geometry(f"+{x}+{y}")

    custom_font = tkFont.Font(family="Helvetica", size=12)

    tk.Label(gui, text="Enter threshold in decimals:", font=custom_font).pack(pady=10)

    threshold_entry = tk.Entry(gui, font=custom_font)
    threshold_entry.pack(pady=5)

    def submit_threshold():
        try:
            threshold = float(threshold_entry.get())
            calculate_probabilities(threshold)
            gui.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    tk.Button(gui, text="Submit", command=submit_threshold, font=custom_font).pack(pady=10)

    gui.mainloop()

start_gui()