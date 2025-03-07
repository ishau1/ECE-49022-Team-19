import copy
import time
import cv2
import Functions as Fun1

# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start_time = time.time()  #Identifies the start time
    image = Image.open('R_test10.jpg')  #Assigns png image to a variable
    image_array = np.array(image)   #Takes png and converts it to a 3D number array
    image_array_copy = copy.deepcopy(image_array)  #Creates an identical matrix of image_array
    dimensions = image_array.shape  #Obtains dimensions of array, 1st number is length, 2nd number is width
    hsv_image = cv2.cvtColor(image_array_copy, cv2.COLOR_BGR2HSV)



    # 3rd is depth
    color_array = np.zeros((dimensions[0], dimensions[1]))  #Creates an array of zeros with same length and width as the
    # 3D array of the png
    print(dimensions)  #Prints the dimensions of the 3D number array

    Fun1.color_array_filler(dimensions, image_array, color_array)  #Runs function that blacks out all pixels except for
    # except for pixel in the body of the resistor

    pixel_value_var = 10  #Helper variable that varies based on number of pixels in the body of the resistor

    orientation1 = Fun1.orientation_determ(color_array, dimensions[1], dimensions[0], pixel_value_var)
    # Returns True if resistor is more Vertical, Returns False if resistor is more horizontal
    coords2 = Fun1.line_bisection_coords1(color_array, pixel_value_var, orientation1, dimensions[0], dimensions[1])
    # Array containing 8 values representing the x and y of the 4 vertices of the body of the resistor

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

    # print(x1, y1, x2, y2)  #Prints coordinates for bisecting line
    slope, y_int = Fun1.slope_determ(x1, y1, x2, y2)  #Funtion that determines the slope, y_int, and orientation
    image_array[coords2[1]][coords2[0]][0] = 255  #Function that assigns top left vertice pixel color to be red
    image_array[coords2[3]][coords2[2]][0] = 255  #Function that assigns top right vertice pixel color to be red
    image_array[coords2[5]][coords2[4]][0] = 255  #Function that assigns bottom right vertice pixel color to be red
    image_array[coords2[7]][coords2[6]][0] = 255  #Function that assigns bottom left vertice pixel color to be red

    color_array_color_chart = []  #Array that will contain the colors of every pixel along the bisecting line
    color_array_color_chart_hsv = []
    color_array_color_chart_bands_only = []  #Array that will only contain the integer values associated
    # with each individual color band
    Fun1.color_array_line_plotter(slope, y_int, x1, y1, x2, y2, orientation1,
                             color_array_color_chart, image_array, color_array, hsv_image, color_array_color_chart_hsv)
    # Function that plots bisecting line in gray on the color array

    matrix_colors = np.vstack((color_array_color_chart_hsv, color_array_color_chart))  #Combines my two arrays with
    # With colors based on the resistor color chart. Top is HSV and bottom is RGB
    print(matrix_colors)

    orientation_band = Fun1.band_integer_determ(color_array_color_chart, color_array_color_chart_bands_only)
    # Function that determines the orientation of the color band.
    # Returns True if color_array_color_chart_bands_only array is in reverse order
    if orientation_band:  #Checks if the orientation band boolean variable is true
        color_array_color_chart_bands_only = color_array_color_chart_bands_only[::-1]
        # Reverse the order of the integers in color_array_color_chart_bands_only array


    print(color_array_color_chart_bands_only)  #Prints the array of the integers associated with each color band

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

    print(end_time - start_time)  #Displays time taken for program to run
    plt.imshow(image_array, cmap='gray')
    #plt.imshow(hsv_image, cmap='gray')
    #plt.imshow(color_array, cmap='gray')

    plt.show()

    bin_number = Fun1.bin_determ(color_array_color_chart_bands_only)
    print("The bin number is", bin_number)

    #plt.imshow(color_array, cmap='gray')
    #plt.show()
