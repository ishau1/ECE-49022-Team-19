import copy
import math
import time
import cv2
import Functions as Fun1

# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


#  Function that creates the grayscale image of the Resistor where the body of the resistor appears as white
def color_array_filler(dimensions1, image_array1, color_array1):
    index1 = 0  #Itteration variable
    while index1 < dimensions1[0]:
        index2 = 0
        while index2 < dimensions1[1]:
            color_array1[index1][index2] = Fun1.colordeterm(image_array1[index1][index2][0],
                                                            image_array1[index1][index2][1],
                                                            image_array1[index1][index2][2])
            index2 += 1  #Increases increment by 1
        index1 += 1  #Increases increment by 1
    return None


#  Function that determines the slope and y-intercept of the line that bisects the body of the Resistor
def slope_determ(x_coord1, y_coord1, x_coord2, y_coord2):
    if x_coord1 == x_coord2:
        return 1
    slope1 = (y_coord2 - y_coord1)/(x_coord2 - x_coord1)
    if abs(slope1) > 1.0:
        slope1 = 1/slope1
    if abs(x_coord2 - x_coord1) > abs(y_coord2 - y_coord1):
        b = -slope1*x_coord1 + y_coord1
    else:
        b = -slope1*y_coord1 + x_coord1
    return slope1, b


#  Function that determines the pixels in the line that bisects the body of the resistor
#  Function that determines the colors associated with that pixel using an RGB function as well as an HSV function
def color_array_line_plotter(slope1, y_int1, x_coord1, y_coord1, x_coord2, y_coord2, orientation3, color_array1,
                             image_array1, color_array2, hsv_array1, hsv_color_array):
    if orientation3:
        starter_index1 = y_coord1
        while starter_index1 < y_coord2:
            starter_index2 = int(slope1*starter_index1 + y_int1)
            color_array2[starter_index1][starter_index2] = 128
            color_array1.append(Fun1.color_determ_color_chart_return(
                image_array1[starter_index1][starter_index2][0],
                image_array1[starter_index1][starter_index2][1],
                image_array1[starter_index1][starter_index2][2]))
            image_array1[starter_index1][starter_index2][3] = 0
            hsv_color_array.append(Fun1.color_determ_hsv(int(hsv_array1[starter_index1][starter_index2][0]),
                                                         int(hsv_array1[starter_index1][starter_index2][1]),
                                                         int(hsv_array1[starter_index1][starter_index2][2])))
            hsv_array1[starter_index1][starter_index2][1] = 0
            starter_index1 += 1  #Increases increment by 1
    else:
        starter_index1 = x_coord1
        while starter_index1 < x_coord2:
            starter_index2 = int(slope1*starter_index1 + y_int1)
            color_array2[starter_index2][starter_index1] = 128
            color_array1.append(Fun1.color_determ_color_chart_return(
                image_array1[starter_index2][starter_index1][0],
                image_array1[starter_index2][starter_index1][1],
                image_array1[starter_index2][starter_index1][2]))
            image_array1[starter_index2][starter_index1][3] = 0
            hsv_color_array.append(Fun1.color_determ_hsv(int(hsv_array1[starter_index2][starter_index1][0]),
                                                         int(hsv_array1[starter_index2][starter_index1][1]),
                                                         int(hsv_array1[starter_index2][starter_index1][2])))
            hsv_array1[starter_index2][starter_index1][1] = 0
            starter_index1 += 1  #Increases increment by 1
    return None


#  Function that determines the individual integers correlated with each band
#  Function also determines whether the integers are in reverse order or not
def band_integer_determ(long_array, short_array):
    index1 = 0
    index2 = 0
    num_pix_start = 0
    num_pix_end = 0
    length1 = len(long_array)
    while index1 < (length1 - 3):
        if long_array[index1] != long_array[index1 + 1]:
            if index1 < length1 - 2:
                if long_array[index1 + 1] == long_array[index1 + 2] and \
                        long_array[index1 + 1] == long_array[index1 + 3] and \
                        long_array[index1 + 1] != long_array[index1 - 2]:
                    short_array.append(long_array[index1 + 1])
        index1 += 1  #Increases increment by 1


    # print(long_array)
    element_to_remove = 12
    while element_to_remove in short_array:
        short_array.remove(element_to_remove)


    while index2 < length1 - 2:
        if long_array[index2] != element_to_remove and long_array[index2 + 1] != element_to_remove \
                and long_array[index2 + 2] != element_to_remove:
            index2 = length1
        else:
            num_pix_start += 1
            index2 += 1  #Increases increment by 1
    while index2 > 2:
        if long_array[index2 - 1] != element_to_remove and long_array[index2 - 2] != element_to_remove \
                and long_array[index2 - 3] != element_to_remove:
            index2 = 0
        else:
            num_pix_end += 1
            index2 -= 1  #Decreases increment by 1

    # print(num_pix_start, num_pix_end)

    if num_pix_start > num_pix_end:
        return True  #Returns True if Color Bands Array is in reverse order
    else:
        return False  #Returns False if Color Band Array is in correct order


#  Function that determines if the body of the resistor is in a more horizontal or vertical direction
def orientation_determ(grayscale_array, length1, width1, pixel1):
    index1 = 0
    threshold1 = pixel1*255
    right = 0
    left = 0
    top = 0
    bottom = 0
    while index1 < length1:
        if grayscale_array[index1].sum() >= threshold1:
            top = index1
            index1 = length1
        else:
            index1 += 1  #Increases increment by 1
    index1 = 0
    while index1 < length1:
        if grayscale_array[length1 - index1 - 1].sum() >= threshold1:
            bottom = length1 - index1 - 1
            index1 = length1
        else:
            index1 += 1  #Increases increment by 1
    index1 = 0
    while index1 < width1:
        if grayscale_array[:, index1].sum() >= threshold1:
            left = index1
            index1 = width1
        else:
            index1 += 1  #Increases increment by 1
    index1 = 0
    while index1 < width1:
        if grayscale_array[:, width1 - index1 - 1].sum() >= threshold1:
            right = width1 - index1 - 1
            index1 = width1
        else:
            index1 += 1  #Increases increment by 1

    # print(right, left, top, bottom)
    if (right - left) > (bottom - top):  #returns False if resistor is more horizontal or flat
        return False
    else:
        return True    #Return True when body of the resistor is standing vertical or tall


#  Function that determines the x and y coordinates of the 4 vertices that define location of the body of the Resistor
def line_bisection_coords1(color_array2, pixel_var, orientation_var, height1, width1):
    index1 = 0
    threshold1 = pixel_var*255*3
    row_top = 0
    row_bottom = 0
    col_left = 0
    col_right = 0
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
    image = Image.open('R47.png')  #Assigns png image to a variable
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

    pixel_value_var = 5  #Helper variable that varies based on number of pixels in the body of the resistor

    orientation1 = orientation_determ(color_array, dimensions[0], dimensions[1], pixel_value_var)
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

    print(color_array_color_chart_hsv)
    print(color_array_color_chart)


    orientation_band = band_integer_determ(color_array_color_chart, color_array_color_chart_bands_only)
    # Function that determines the orientation of the color band.
    # Returns True if color_array_color_chart_bands_only array is in reverse order
    if orientation_band:  #Checks if the orientation band boolean variable is true
        color_array_color_chart_bands_only = color_array_color_chart_bands_only[::-1]
        # Reverse the order of the integers in color_array_color_chart_bands_only array


    print(color_array_color_chart_bands_only)  #Prints the array of the integers associated with each color band


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

    bin_number = Fun1.bin_determ(color_array_color_chart_bands_only)

    print(resistance_value)  #Prints the resistance value of the resistor
    print("The bin number is", bin_number)


    end_time = time.time()  #End time variable

    print(end_time - start_time)  #Displays time taken for program to run
    plt.imshow(image_array, cmap='gray')

    plt.show()
