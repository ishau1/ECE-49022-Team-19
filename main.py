import copy
import math
import Functions

# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def line_bisection_coords(color_array1, pixel_var):  #Returns the x and y values of the 4 coordinates used to define the
        # body of the resistor
    length1, width1 = color_array1.shape  #length1 is the number of elements for height
    index1 = 0
    top_left_x = 0
    top_left_y = 0
    top_right_x = 0
    top_right_y = 0
    bottom_left_x = 0
    bottom_left_y = 0
    bottom_right_x = 0
    bottom_right_y = 0

    threshold1 = pixel_var*255
    while index1 < width1:
        if color_array1[:, index1].sum() > threshold1:
            top_left_x = index1
            top_left_y = index_finder(color_array1[:, index1], True)
            index1 = width1
        else:
            index1 += 1
    index1 = 0
    while index1 < length1:
        if color_array1[index1].sum() > threshold1:
            top_right_y = index1
            top_right_x = index_finder(color_array1[index1], False)
            index1 = length1
        else:
            index1 += 1
    index1 = 0
    while index1 < width1:
        if color_array1[:, width1 - index1 - 1].sum() > threshold1:
            bottom_right_x = width1 - index1 - 1
            bottom_right_y = index_finder(color_array1[:, width1 - index1 - 1], False)
            index1 = width1
        else:
            index1 += 1


    index1 = 0
    while index1 < length1:
        if color_array1[length1 - index1 - 1].sum() > threshold1:
            bottom_left_y = length1 - index1 - 1
            bottom_left_x = index_finder(color_array1[length1 - index1 - 1], True)
            index1 = length1
        else:
            index1 += 1


    array1 = [top_left_x, top_left_y, top_right_x, top_right_y, bottom_right_x, bottom_right_y,
              bottom_left_x, bottom_left_y]
    return array1


def index_finder(array1, direction_determiner):
    index1 = 0
    length1 = len(array1)
    if direction_determiner:  #Checks if Direction Determiner boolean variable is True
        while index1 < length1:
            if array1[index1] > 0:
                return index1
            else:
                index1 += 1
    else:
        while index1 < length1:
            if array1[length1 - index1 - 1] > 0:
                return length1 - index1 - 1
            else:
                index1 += 1
    return 0


def dist_determ(x_coord1, y_coord1, x_coord2, y_coord2):
    return math.sqrt((x_coord1 - x_coord2)**2 + (y_coord1-y_coord2)**2)


def color_array_filler(dimensions1, image_array1, color_array1):
    index1 = 0  #Itteration variable
    while index1 < dimensions1[0]:
        index2 = 0
        while index2 < dimensions1[1]:
            color_array1[index1][index2] = Functions.colordeterm(image_array1[index1][index2][0],
                                                                 image_array1[index1][index2][1],
                                                                 image_array1[index1][index2][2])
            index2 += 1
        index1 += 1
    return None


def slope_determ(x_coord1, y_coord1, x_coord2, y_coord2):
    if x_coord1 == x_coord2:
        return 1
    slope1 = (y_coord2 - y_coord1)/(x_coord2 - x_coord1)
    if abs(slope1) > 1.0:
        slope1 = 1/slope1
    if abs(x_coord2 - x_coord1) > abs(y_coord2 - y_coord1):
        orientation2 = False
        b = -slope1*x_coord1 + y_coord1
    else:
        orientation2 = True
        b = -slope1*y_coord1 + x_coord1
    return slope1, b, orientation2


def color_array_line_plotter(slope1, y_int1, x_coord1, y_coord1, x_coord2, y_coord2, orientation3, color_array1,
                             image_array1, color_array2):
    if orientation3:
        starter_index1 = y_coord1
        while starter_index1 < y_coord2:
            starter_index2 = int(slope1*starter_index1 + y_int1)
            color_array2[starter_index1][starter_index2] = 128
            color_array1.append(Functions.color_determ_color_chart_return(
                image_array1[starter_index1][starter_index2][0],
                image_array1[starter_index1][starter_index2][1],
                image_array1[starter_index1][starter_index2][2]))
            image_array1[starter_index1][starter_index2][1] = 255
            starter_index1 += 1
    else:
        starter_index1 = x_coord1
        while starter_index1 < x_coord2:
            starter_index2 = int(slope1*starter_index1 + y_int1)
            color_array2[starter_index2][starter_index1] = 128
            color_array1.append(Functions.color_determ_color_chart_return(
                image_array1[starter_index2][starter_index1][0],
                image_array1[starter_index2][starter_index1][1],
                image_array1[starter_index2][starter_index1][2]))
            image_array1[starter_index2][starter_index1][1] = 255
            starter_index1 += 1
    return None


def band_integer_determ(long_array, short_array):
    index1 = 0
    index2 = 0
    num_pix_start = 0
    num_pix_end = 0
    length1 = len(long_array)
    while index1 < (length1 - 1):
        if long_array[index1] != long_array[index1 + 1]:
            if index1 < length1 - 2:
                if long_array[index1 + 1] == long_array[index1 + 2] and \
                        long_array[index1 + 1] == long_array[index1 + 3] and \
                        long_array[index1 + 1] != long_array[index1 - 1]:
                    short_array.append(long_array[index1 + 1])
        index1 += 1


    print(long_array)
    element_to_remove = 12
    while element_to_remove in short_array:
        short_array.remove(element_to_remove)


    while index2 < length1 - 2:
        if long_array[index2] != element_to_remove and long_array[index2 + 1] != element_to_remove \
                and long_array[index2 + 2] != element_to_remove:
            index2 = length1
        else:
            num_pix_start += 1
            index2 += 1
    while index2 > 2:
        if long_array[index2 - 1] != element_to_remove and long_array[index2 - 2] != element_to_remove \
                and long_array[index2 - 2] != element_to_remove:
            index2 = 0
        else:
            num_pix_end += 1
            index2 -= 1

    if num_pix_start > num_pix_end:
        return True  #Returns True if Color Bands Array is in reverse order
    else:
        return False  #Returns False if Color Band Array is in correct order


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
            index1 += 1
    index1 = 0
    while index1 < length1:
        if grayscale_array[length1 - index1 - 1].sum() >= threshold1:
            bottom = length1 - index1 - 1
            index1 = length1
        else:
            index1 += 1
    index1 = 0
    while index1 < width1:
        if grayscale_array[:, index1].sum() >= threshold1:
            left = index1
            index1 = width1
        else:
            index1 += 1
    index1 = 0
    while index1 < width1:
        if grayscale_array[:, width1 - index1 - 1].sum() >= threshold1:
            right = width1 - index1 - 1
            index1 = width1
        else:
            index1 += 1

    print(right, left, top, bottom)
    if (right - left) > (bottom - top):  #returns False if resistor is more horizontal or flat
        return False
    else:
        return True    #Return True when body of the resistor is standing vertical or tall


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
                index1 += 1
        index1 = 0
        while index1 < height1:
            if color_array2[height1 - index1 - 1].sum() >= threshold1:
                row_bottom = height1 - index1 - 1
                index1 = height1
            else:
                index1 += 1
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
                index1 += 1
        index1 = 0
        while index1 < width1:
            if color_array2[:, width1 - index1 - 1].sum() >= threshold1:
                col_right = width1 - index1 - 1
                index1 = width1
            else:
                index1 += 1
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
    image = Image.open('ImageResistor.png')  #Assigns png image to a variable
    image1 = Image.open('Resistor_47.png')  #Assigns png image to a variable
    image_array = np.array(image)   #Takes png and converts it to a 3D number array
    image1_array = np.array(image1)
    image_array_copy = copy.deepcopy(image_array)
    dimensions = image_array.shape  #Obtains dimensions of array, 1st number is length, 2nd number is width
    # 3rd is depth
    color_array = np.zeros((dimensions[0], dimensions[1]))  #Creates an array of zeros with same length and width as the
    # 3D array of the png
    print(dimensions)

    color_array_filler(dimensions, image_array, color_array)


    pixel_value_var = 5
    """
    coords1 = line_bisection_coords(color_array, pixel_value_var)

    image_array[coords1[1]][coords1[0]][0] = 255
    image_array[coords1[3]][coords1[2]][0] = 255
    image_array[coords1[5]][coords1[4]][0] = 255
    image_array[coords1[7]][coords1[6]][0] = 255"""

    orientation1 = orientation_determ(color_array, dimensions[0], dimensions[1], pixel_value_var)
    coords2 = line_bisection_coords1(color_array, pixel_value_var, orientation1, dimensions[0], dimensions[1])

    if orientation1:
        x1 = int((coords2[0] + coords2[2])/2)
        y1 = int((coords2[1] + coords2[3])/2)
        x2 = int((coords2[4] + coords2[6])/2)
        y2 = int((coords2[5] + coords2[7])/2)
    else:
        x1 = int((coords2[0] + coords2[6])/2)
        y1 = int((coords2[1] + coords2[7])/2)
        x2 = int((coords2[2] + coords2[4])/2)
        y2 = int((coords2[3] + coords2[5])/2)

    print(x1, y1, x2, y2)
    slope, y_int, orientation = slope_determ(x1, y1, x2, y2)
    image_array[coords2[1]][coords2[0]][0] = 255
    image_array[coords2[3]][coords2[2]][0] = 255
    image_array[coords2[5]][coords2[4]][0] = 255
    image_array[coords2[7]][coords2[6]][0] = 255

    color_array_color_chart = []
    color_array_color_chart_bands_only = []
    color_array_line_plotter(slope, y_int, x1, y1, x2, y2, orientation,
                             color_array_color_chart, image_array, color_array)




    orientation_band = band_integer_determ(color_array_color_chart, color_array_color_chart_bands_only)
    if orientation_band:
        color_array_color_chart_bands_only = color_array_color_chart_bands_only[::-1]


    print(color_array_color_chart_bands_only)


    if len(color_array_color_chart_bands_only) > 3:
        resistance_value = (color_array_color_chart_bands_only[0]*100 + color_array_color_chart_bands_only[1]*10
                            + color_array_color_chart_bands_only[2]) * 10**color_array_color_chart_bands_only[-1]
    elif len(color_array_color_chart_bands_only) == 3:
        resistance_value = (color_array_color_chart_bands_only[0]*10 + color_array_color_chart_bands_only[1]) \
                           * 10**color_array_color_chart_bands_only[-1]
    else:
        resistance_value = False
    print(resistance_value)

    plt.imshow(color_array, cmap='gray', vmin=0, vmax=255)
    plt.imshow(image_array_copy, cmap='gray')
    plt.show()
