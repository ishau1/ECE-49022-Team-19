import numpy as np
import math
import statistics
from scipy.stats import linregress
import main_function

if __name__ == '__main__':
    # Number of elements you want
    n = 25

    # Creating the array of strings
    array_path = [f"R_Demo{i}.jpg" for i in range(1, n + 1)]

    bin_numbers = [9, 9, 13, 12, 8, 9, 9, 8, 8, 10, 10, 10, 14, 12, 9, 12, 12, 13, 15, 13, 9, 15, 9, 11, 13]

    number_bin_correct = 0
    number_time_in_range = 0
    total_iterations = 0

    index1 = 10
    while index1 < n:
        bin_num_temp, time_temp = main_function.fun1(array_path[index1])
        if bin_num_temp == bin_numbers[index1]:
            number_bin_correct += 1
        if time_temp <= 3:
            number_time_in_range += 1
        total_iterations += 1
        index1 += 1

    print(number_bin_correct/total_iterations)
    print(number_time_in_range/total_iterations)


