import copy
import time
import cv2
import Functions as Fun1

# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress


# Press the green button in the gutter to run the script.
def fun1(path_image):
    start_time = time.time()  #Identifies the start time
    image = Image.open(path_image)  #Assigns png image to a variable
    image_array = np.array(image)   #Takes png and converts it to a 3D number array
    image_array_copy = copy.deepcopy(image_array)  #Creates an identical matrix of image_array
    dimensions = image_array.shape  #Obtains dimensions of array, 1st number is length, 2nd number is width



    # 3rd is depth
    color_array = np.zeros((dimensions[0], dimensions[1]))  #Creates an array of zeros with same length and width as the
    # 3D array of the png
    #print(dimensions)  #Prints the dimensions of the 3D number array
    x_values = []
    y_values = []
    Fun1.color_array_filler(dimensions, image_array, color_array, x_values, y_values)  #Runs function that blacks out all pixels except for
    result = linregress(x_values, y_values)
    result1 = linregress(y_values, x_values)
    slope = result.slope
    slope1 = result1.slope


    if abs(slope) < abs(slope1):
        orientation2 = False
        slope_final = slope
    else:
        orientation2 = True
        slope_final = slope1

    # except for pixel in the body of the resistor

    pixel_value_var = 10  #Helper variable that varies based on number of pixels in the body of the resistor

    orientation1 = Fun1.orientation_determ(color_array, dimensions[1], dimensions[0], pixel_value_var)
    # Returns True if resistor is more Vertical, Returns False if resistor is more horizontal
    coords2 = Fun1.line_bisection_coords1(color_array, pixel_value_var, orientation1, dimensions[0], dimensions[1])
    # Array containing 8 values representing the x and y of the 4 vertices of the body of the resistor
    """"
    if orientation1:  #True if body of resistor is orientated in a more vertical direction
        x1 = int((coords2[0] + coords2[2])/2)  #Calculates left x value that will be used to determine bisecting line
        y1 = int((coords2[1] + coords2[3])/2)  #Calculates left y value that will be used to determine bisecting line
        x2 = int((coords2[4] + coords2[6])/2)  #Calculates right x value that will be used to determine bisecting line
        y2 = int((coords2[5] + coords2[7])/2)  #Calculates right y value that will be used to determine bisecting line
    else:
        x1 = int((coords2[0] + coords2[6])/2)  #Calculates left x value that will be used to determine bisecting line
        y1 = int((coords2[1] + coords2[7])/2)  #Calculates left y value that will be used to determine bisecting line
        x2 = int((coords2[2] + coords2[4])/2)  #Calculates right x value that will be used to determine bisecting line
        y2 = int((coords2[3] + coords2[5])/2)  #Calculates right y value that will be used to determine bisecting line
    """

    x1, y1, x2, y2 = Fun1.critical_points_determ(orientation2, coords2, slope_final)
    #print(x1, y1, x2, y2)  #Prints coordinates for bisecting line
    #print(orientation2)
    slope, y_int = Fun1.slope_determ(x1, y1, x2, y2)  #Funtion that determines the slope, y_int, and orientation
    image_array[coords2[1]][coords2[0]][0] = 255  #Function that assigns top left vertice pixel color to be red
    image_array[coords2[3]][coords2[2]][0] = 255  #Function that assigns top right vertice pixel color to be red
    image_array[coords2[5]][coords2[4]][0] = 255  #Function that assigns bottom right vertice pixel color to be red
    image_array[coords2[7]][coords2[6]][0] = 255  #Function that assigns bottom left vertice pixel color to be red

    color_array_color_chart = []  #Array that will contain the colors of every pixel along the bisecting line
    color_array_color_chart_bands_only = []  #Array that will only contain the integer values associated
    # with each individual color band
    Fun1.color_array_line_plotter(slope, y_int, x1, y1, x2, y2, orientation1,
                             color_array_color_chart, image_array, color_array)
    # Function that plots bisecting line in gray on the color array

    # With colors based on the resistor color chart. Top is HSV and bottom is RGB
    #for i in range(0, len(color_array_color_chart), 25):
    #    print(color_array_color_chart[i:i + 25])
    orientation_band = Fun1.band_integer_determ(color_array_color_chart, color_array_color_chart_bands_only)
    # Function that determines the orientation of the color band.
    # Returns True if color_array_color_chart_bands_only array is in reverse order
    if orientation_band:  #Checks if the orientation band boolean variable is true
        color_array_color_chart_bands_only = color_array_color_chart_bands_only[::-1]
        # Reverse the order of the integers in color_array_color_chart_bands_only array


    #print(color_array_color_chart_bands_only)  #Prints the array of the integers associated with each color band


    """
    if len(color_array_color_chart_bands_only) > 3:  #Checks if resistor is 5 band or greater
        resistance_value = (color_array_color_chart_bands_only[0]*100 + color_array_color_chart_bands_only[1]*10
                            + color_array_color_chart_bands_only[2]) * 10**color_array_color_chart_bands_only[-1]
        # Calculates resistance value of 5 band resistor
    elif len(color_array_color_chart_bands_only) == 3:  #Checks if resistor is 4 band
        resistance_value = (color_array_color_chart_bands_only[0]*10 + color_array_color_chart_bands_only[1]) \
                           * 10**color_array_color_chart_bands_only[-1]
        # Calculates resistance value of 4 band resistor
    else:
        resistance_value = False  #Returns false in case of poor determination of color bands
    print(resistance_value)  #Prints the resistance value of the resistor
    """

    end_time = time.time()  #End time variable
    total_time = end_time - start_time
    #print("The total completion time is", total_time, "seconds")  #Displays time taken for program to run

    bin_number = Fun1.bin_determ(color_array_color_chart_bands_only)
    #print("The bin number is", bin_number)







    return(bin_number, total_time)

