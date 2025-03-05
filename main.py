import copy
import time
import cv2
import Functions as Fun1
import statistics

# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


#  Function that creates the grayscale image of the Resistor where the body of the resistor appears as white
def color_array_filler(dimensions1, image_array1, color_array1):
    index1 = 0  #Itteration variable
    while index1 < dimensions1[0]:  #Iterates through the height of the image
        index2 = 0  #Itteration variable
        while index2 < dimensions1[1]:  #Iterates through the width of the image
            color_array1[index1][index2] = Fun1.colordeterm(image_array1[index1][index2][0],
                                                            image_array1[index1][index2][1],
                                                            image_array1[index1][index2][2])
           # Fills in 2D grayscale matrix which will be used to identify body of the Resistor
            index2 += 1  #Increases increment by 1
        index1 += 1  #Increases increment by 1
    return None


#  Function that determines the slope and y-intercept of the line that bisects the body of the Resistor
def slope_determ(x_coord1, y_coord1, x_coord2, y_coord2):
    if x_coord1 == x_coord2:  #Checks if x coordinates are identical as slope would be infinity in that case
        return 0  #Returns 0 because slope will be 0 when iterating across y-axis values
    slope1 = (y_coord2 - y_coord1)/(x_coord2 - x_coord1)
    if abs(slope1) > 1.0:  #Checks if slope is greater than 1 so it can have its inverse be the slope
        slope1 = 1/slope1
    if abs(x_coord2 - x_coord1) > abs(y_coord2 - y_coord1):  #Checks if Resistor is more horizontal or vertical
        b = -slope1*x_coord1 + y_coord1  #Determines y-intercept is Resistor is more horizontal
    else:
        b = -slope1*y_coord1 + x_coord1  #Determines y-intercept is Resistor is more vertical
    return slope1, b


#  Function that determines the pixels in the line that bisects the body of the resistor
#  Function that determines the colors associated with that pixel using an RGB function as well as an HSV function
def color_array_line_plotter(slope1, y_int1, x_coord1, y_coord1, x_coord2, y_coord2, orientation3, color_array1,
                             image_array1, color_array2, hsv_array1, hsv_color_array):
    dimensions1 = image_array1.shape
    if orientation3:  #Orientation value that determines the Resistor to be more Vertical
        starter_index1 = y_coord1  #The y-axis value (row) of the first pixel in the line that bisects Resistor
        while starter_index1 < y_coord2:  #Will run through all y-axis values until it reaches end of line of pixels
            starter_index2 = int(slope1*starter_index1 + y_int1)
            # The x-axis value (column) of the first pixel in the line that bisects Resistor
            color_array2[starter_index1][starter_index2] = 128
            # Assigns the pixel in the line gray value
            color_array1.append(Fun1.color_determ_color_chart_return(
                image_array1[starter_index1][starter_index2][0],
                image_array1[starter_index1][starter_index2][1],
                image_array1[starter_index1][starter_index2][2]))

            if color_array1[-1] == 11:
                Fun1.pixel_glare_color_determ(starter_index2, starter_index1, slope1, orientation3, color_array1,
                                              image_array1, 6, dimensions1[0], dimensions1[1])

            # Function that adds the pixels color determined by RGB to an array
            image_array1[starter_index1][starter_index2][1] = 255  #Assigns the pixel in the line green value
            hsv_color_array.append(Fun1.color_determ_hsv(int(hsv_array1[starter_index1][starter_index2][0]),
                                                         int(hsv_array1[starter_index1][starter_index2][1]),
                                                         int(hsv_array1[starter_index1][starter_index2][2])))
            # Function that adds the pixels color determined by HSV to an array
            hsv_array1[starter_index1][starter_index2][1] = 0  #Assigns the pixel in the line 0 saturation value
            starter_index1 += 1  #Increases increment by 1
    else:  #Orientation value determined the Resistor to be more Horizontal
        starter_index1 = x_coord1  #The x-axis value (column) of the first pixel in the line that bisects Resistor
        while starter_index1 < x_coord2:
            starter_index2 = int(slope1*starter_index1 + y_int1)
            # The y-axis value (row) of the first pixel in the line that bisects Resistor
            color_array2[starter_index2][starter_index1] = 128
            # Assigns the pixel in the line gray value
            color_array1.append(Fun1.color_determ_color_chart_return(
                image_array1[starter_index2][starter_index1][0],
                image_array1[starter_index2][starter_index1][1],
                image_array1[starter_index2][starter_index1][2]))

            if color_array1[-1] == 11:
                Fun1.pixel_glare_color_determ(starter_index1, starter_index2, slope1, orientation3, color_array1,
                                              image_array1, 4, dimensions1[0], dimensions1[1])

            # Function that adds the pixels color determined by RGB to an array
            image_array1[starter_index2][starter_index1][1] = 255  #Assigns the pixel in the line green value
            hsv_color_array.append(Fun1.color_determ_hsv(int(hsv_array1[starter_index2][starter_index1][0]),
                                                         int(hsv_array1[starter_index2][starter_index1][1]),
                                                         int(hsv_array1[starter_index2][starter_index1][2])))
            # Function that adds the pixels color determined by HSV to an array
            hsv_array1[starter_index2][starter_index1][1] = 0  #Assigns the pixel in the line 0 saturation value
            starter_index1 += 1  #Increases increment by 1
    return None


#  Function that determines the individual integers correlated with each band
#  Function also determines whether the integers are in reverse order or not
def band_integer_determ(long_array, short_array):
    index1 = 0  #Itteration variable
    length1 = len(long_array)  #Determines the length of the array
    while index1 < (length1 - 4):  #Iterates through all color values of array except final 4
        if long_array[index1] != long_array[index1 + 1]:  #Checks for change in pixel value
            array1 = long_array[index1 + 1:index1 + 5]  #Creates an array of the next 4 color values in the array
            median1 = statistics.median(array1)  #Determines the median of the new array
            sum1 = array1.count(median1)  #Determines the number of times the median value of the new array occurs
            if sum1 >= 3 and median1 == long_array[index1 + 1]:  #Determines if the change in pixels should result in
                # new pixel being added to the short_array
                short_array.append(long_array[index1 + 1])  #Adds integer to short_array
                if index1 <= (length1 - 11) and not (long_array[index1 + 1] == 12 or
                                                     long_array[index1 + 1] == 11 or long_array[index1 + 1] == 13):
                    # Checks if index value is less than 10 from max value
                    index1 += 10  #Jumps 10 pixel in order to leap pass pixel band which it is currently in
        index1 += 1  #Increases increment by 1

    # print(long_array)
    element_to_remove = 12  #Element that represents light blue pixels
    while element_to_remove in short_array:  #Function that removes all light blue pixels from array
        short_array.remove(element_to_remove)

    element_to_remove = 11  #Element that represents light blue pixels
    while element_to_remove in short_array:  #Function that removes all light blue pixels from array
        short_array.remove(element_to_remove)

    element_to_remove = 13  #Element that represents light blue pixels
    while element_to_remove in short_array:  #Function that removes all light blue pixels from array
        short_array.remove(element_to_remove)

    return True  #Currently outdated, does not affect main functions output


#  Function that determines if the body of the resistor is in a more horizontal or vertical direction
def orientation_determ(grayscale_array, width1, length1, pixel1):
    index1 = 0  #Itteration variable
    threshold1 = pixel1*255  #Arbitrarily defined threshold for number of pixels
    right = 0  #right most pixel index
    left = 0  #left most pixel index
    top = 0  #top most pixel index
    bottom = 0  #bottom most pixel index
    while index1 < length1:  #While loop that will iterate through all y-axis (row) values
        if grayscale_array[index1].sum() >= threshold1:  #Checks if sum of row of pixels exceeds threshold
            top = index1  #Assigns index to the first row from the top that exceeds threshold
            index1 = length1  #Assigns index1 to end value to end while loop
        else:
            index1 += 1  #Increases increment by 1
    index1 = 0  #Returns Iteration variable to 0
    while index1 < length1:  #While loop that will iterate through all y-axis (row) values
        if grayscale_array[length1 - index1 - 1].sum() >= threshold1:  #Checks if sum of row of pixels exceeds threshold
            bottom = length1 - index1 - 1  #Assigns index to the first row from the bottom that exceeds threshold
            index1 = length1  #Assigns index1 to end value to end while loop
        else:
            index1 += 1  #Increases increment by 1
    index1 = 0  #Returns Iteration variable to 0
    while index1 < width1:  #While loop that will iterate through all x-axis (column) values
        if grayscale_array[:, index1].sum() >= threshold1:  #Checks if sum of column of pixels exceeds threshold
            left = index1  #Assigns index to the first column from the left that exceeds threshold
            index1 = width1  #Assigns index1 to end value to end while loop
        else:
            index1 += 1  #Increases increment by 1
    index1 = 0
    while index1 < width1:  #While loop that will iterate through all x-axis (column) values
        if grayscale_array[:, width1 - index1 - 1].sum() >= threshold1:
            # Checks if sum of row of pixels exceeds threshold
            right = width1 - index1 - 1  #Assigns index to the first column from the right that exceeds threshold
            index1 = width1  #Assigns index1 to end value to end while loop
        else:
            index1 += 1  #Increases increment by 1

    # print(right, left, top, bottom)
    if (right - left) > (bottom - top):  #returns False if resistor is more horizontal or flat
        return False
    else:
        return True    #Return True when body of the resistor is standing vertical or tall


#  Function that determines the x and y coordinates of the 4 vertices that define location of the body of the Resistor
def line_bisection_coords1(color_array2, pixel_var, orientation_var, height1, width1):
    index1 = 0  #Itteration variable
    threshold1 = pixel_var*255*3  #Arbitrary threshold voltage
    row_top = 0  #Top y-axis index value
    row_bottom = 0  #Bottom y-axis index value
    col_left = 0 #Left most x-axis index value
    col_right = 0 #Right most x-axis index value
    if orientation_var:  #Checks if orientation_var is True
        while index1 < height1:
            if color_array2[index1].sum() >= threshold1:
                row_top = index1
                index1 = height1
            else:
                index1 += 1  #Increases increment by 1
        index1 = 0
        while index1 < height1:
            if color_array2[height1 - index1 - 1].sum() >= threshold1:
                row_bottom = height1 - index1 - 1
                index1 = height1
            else:
                index1 += 1  #Increases increment by 1
        top_left_y = row_top
        top_right_y = row_top
        bottom_left_y = row_bottom
        bottom_right_y = row_bottom
        nonzero_indices_top = np.nonzero(color_array2[row_top])[0]
        nonzero_indices_bottom = np.nonzero(color_array2[row_bottom])[0]
        top_left_x = int(nonzero_indices_top[0])
        top_right_x = int(nonzero_indices_top[-1])
        bottom_left_x = int(nonzero_indices_bottom[0])
        bottom_right_x = int(nonzero_indices_bottom[-1])
    else:
        while index1 < width1:
            if color_array2[:, index1].sum() >= threshold1:
                col_left = index1
                index1 = width1
            else:
                index1 += 1  #Increases increment by 1
        index1 = 0
        while index1 < width1:
            if color_array2[:, width1 - index1 - 1].sum() >= threshold1:
                col_right = width1 - index1 - 1
                index1 = width1
            else:
                index1 += 1  #Increases increment by 1
        top_left_x = col_left
        top_right_x = col_right
        bottom_left_x = col_left
        bottom_right_x = col_right
        nonzero_indices_left = np.nonzero(color_array2[:, col_left])[0]
        nonzero_indices_right = np.nonzero(color_array2[:, col_right])[0]
        top_left_y = int(nonzero_indices_left[0])
        top_right_y = int(nonzero_indices_right[0])
        bottom_left_y = int(nonzero_indices_left[-1])
        bottom_right_y = int(nonzero_indices_right[-1])

    array1 = [top_left_x, top_left_y, top_right_x, top_right_y, bottom_right_x, bottom_right_y, bottom_left_x,
              bottom_left_y]

    return array1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start_time = time.time()  #Identifies the start time
    image = Image.open('R_test11.jpg')  #Assigns png image to a variable
    image_array = np.array(image)   #Takes png and converts it to a 3D number array
    image_array_copy = copy.deepcopy(image_array)  #Creates an identical matrix of image_array
    dimensions = image_array.shape  #Obtains dimensions of array, 1st number is length, 2nd number is width
    hsv_image = cv2.cvtColor(image_array_copy, cv2.COLOR_BGR2HSV)



    # 3rd is depth
    color_array = np.zeros((dimensions[0], dimensions[1]))  #Creates an array of zeros with same length and width as the
    # 3D array of the png
    print(dimensions)  #Prints the dimensions of the 3D number array

    color_array_filler(dimensions, image_array, color_array)  #Runs function that blacks out all pixels except for
    # except for pixel in the body of the resistor

    pixel_value_var = 10  #Helper variable that varies based on number of pixels in the body of the resistor

    orientation1 = orientation_determ(color_array, dimensions[1], dimensions[0], pixel_value_var)
    # Returns True if resistor is more Vertical, Returns False if resistor is more horizontal
    coords2 = line_bisection_coords1(color_array, pixel_value_var, orientation1, dimensions[0], dimensions[1])
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
    slope, y_int = slope_determ(x1, y1, x2, y2)  #Funtion that determines the slope, y_int, and orientation
    image_array[coords2[1]][coords2[0]][0] = 255  #Function that assigns top left vertice pixel color to be red
    image_array[coords2[3]][coords2[2]][0] = 255  #Function that assigns top right vertice pixel color to be red
    image_array[coords2[5]][coords2[4]][0] = 255  #Function that assigns bottom right vertice pixel color to be red
    image_array[coords2[7]][coords2[6]][0] = 255  #Function that assigns bottom left vertice pixel color to be red

    color_array_color_chart = []  #Array that will contain the colors of every pixel along the bisecting line
    color_array_color_chart_hsv = []
    color_array_color_chart_bands_only = []  #Array that will only contain the integer values associated
    # with each individual color band
    color_array_line_plotter(slope, y_int, x1, y1, x2, y2, orientation1,
                             color_array_color_chart, image_array, color_array, hsv_image, color_array_color_chart_hsv)
    # Function that plots bisecting line in gray on the color array

    matrix_colors = np.vstack((color_array_color_chart_hsv, color_array_color_chart))  #Combines my two arrays with
    # With colors based on the resistor color chart. Top is HSV and bottom is RGB
    print(matrix_colors)

    orientation_band = band_integer_determ(color_array_color_chart, color_array_color_chart_bands_only)
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
