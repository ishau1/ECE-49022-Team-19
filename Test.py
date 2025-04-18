import numpy as np
import math
import statistics
from scipy.stats import linregress
import main_function

if __name__ == '__main__':
    # Number of elements you want
    n = 53

    # Creating the array of strings
    array_path = [f"Demo_Resistors/R_Demo{i}.jpg" for i in range(1, n + 1)]

    bin_numbers = [9, 9, 13, 12, 9, 9, 9, 8, 8, 10, 10, 10, 14, 12, 9, 12, 12, 13, 15, 13, 9, 15, 9, 11, 13, 9, 8, 9, 9, 8, 10, 8, 15, 9, 12, 10, 13, 8, 8, 8, 10, 9, 10, 11, 15, 11, 11, 11, 11, 9, 14, 11, 10]

    time_values = []

    number_bin_correct = 0
    number_time_in_range = 0
    number_ratio_in_range = 0
    total_iterations = 0
    temp_binary = 0

    index1 = 0
    while index1 < n:
        bin_num_temp, time_temp, ratio1 = main_function.fun1(array_path[index1])
        if bin_num_temp == bin_numbers[index1]:
            number_bin_correct += 1
        else:
            print(index1 + 1)
        if time_temp < 3:
            number_time_in_range += 1
        time_values.append(time_temp)

        total_iterations += 1
        index1 += 1

    print(number_bin_correct/total_iterations)
    print(number_time_in_range/total_iterations)
    print(number_ratio_in_range/total_iterations)
    print(statistics.median(time_values))
    print(statistics.mean(time_values))



