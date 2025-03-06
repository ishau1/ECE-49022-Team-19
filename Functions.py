import numpy as np
import math
import statistics


#  Function used to create grayscale image of resistor with body of the resistor appearing as white
def colordeterm(red, green, blue):
    red = int(red)  #Converts 8 bit red to integer
    green = int(green)  #Converts 8 bit green to integer
    blue = int(blue)  #Converts 8 bit blue to integer
    sum1 = red + green + blue  #Sums up the RGB values


    if sum1 > 150*3:  #Identifies white pixels
        value = 0  #Grayscale Value that the pixel will be changed to
        valueint8 = np.uint8(value)
        return valueint8  #Returns black pixel
    elif blue - red >= 40:  #Formula to Determine that the pixel is lightblue which is Resistor body color
        value = 255  #Grayscale Value that the pixel will be changed to
        valueint8 = np.uint8(value)
        return valueint8  #Returns white pixel
    else:
        value = 0  #Grayscale Value that the pixel will be changed to
        valueint8 = np.uint8(value)
        return valueint8  #Returns black pixel


#  Function using RGB used to determine pixel color associated with resistor color chart
def color_determ_color_chart_return(red, green, blue):
    red = int(red)
    green = int(green)
    blue = int(blue)
    sum1 = red + green + blue
    if sum1 >= 650:
        return 13
    elif sum1 >= 450:
        return 11
    elif red >= 90 and green >= 90 and blue >= 90 and sum1 >= 320:
        return 11
    elif (red - green) >= 25 and (red - blue) >= 25 and (red <= 160 and green <= 75) and abs(green - blue) <= 20 and red >= 40:  #Determines Red
        return 2
    elif blue >= 160 and green >= 100:  #Determines Resistor Background Color Light Blue
        return 12
    elif sum1 <= 25:
        if red >= 5*green and red >= 5*blue:
            return 1
        else:
            return 0
    elif sum1 < 180 and abs(red - blue) <= 15 and abs(red - green) <= 15:  #Determines Black
        return 0
    elif sum1 < 190 and red >= 40 and red - green >= 0 and red - blue >= 0:  #Determines Brown
        return 1
    elif (red >= green + 20) and (blue + 20 <= red) and red <= 80:  #Determines Brown
        return 1
    elif red - green >= 15 and (green - blue >= 20) and (red - blue >= 40) and red >= 75:  #Determines Orange
        return 3
    elif (green - red) >= 25 and (green - blue) >= 80:  #Determines Yellow
        return 4
    elif green >= 3*red and green >= 2*blue and green >= 40 or (green - red >= 25 and green - blue >= 25 and green >= 40):  #Determines Green
        return 5
    elif blue >= 4*red and green <= 40 and blue >= 80 and blue <= 150 and blue + red > 10:  #Determines Blue
        return 6
    elif green <= (blue - 20) and red <= (blue - 20) and abs(green - red) <= 25:  #Determines Purple
        return 7


    #  Determines Gray
    elif abs(red - blue) <= 25 and abs(red - green) <= 25 and abs(blue - green) <= 25 and sum1 >= 125:
        return 8
    else:  #Determines pixel color to be none of the above
        return 12


def color_determ_hsv(hue, saturation, value):
    if value <= 35:  #Determines if pixel is black
        return 0
    elif ((hue <= 66) and (hue >= 55)) and (saturation <= 60 and value >= 80) and value <= 120:
        return 8
    elif (hue <= 66) and (hue >= 55):  #Determines if pixel is yellow
        return 5
    elif (hue <= 80) and (hue >= 67):  #Determines if pixel is yellow
        return 4
    elif hue <= 11 or hue >= 176:  #Determines if pixel is purple
        return 7
    elif (hue <= 115) and (hue >= 105) and (value >= 150):  #Determines if pixel is orange
        return 3
    elif (hue <= 130) and (hue >= 116) and (value >= 80) and (saturation >= 90):  #Determines if pixel is red
        return 2
    elif (hue >= 8) and (hue <= 15):  #Determines if pixel is blue
        return 6
    elif (hue >= 100) and (hue <= 130) and (value <= 90):  #Determines if pixel is red
        return 1
    elif (hue >= 95) and (hue <= 105) and (saturation <= 160 and value >= 115) and (value >= 115 and value <= 145):
        # Determines if pixel is Gold
        return 10
    else:  #Determines pixel to be none of the above
        return 12


#  Function to determine which bin the resistor is to be sent to
def bin_determ(band_array):
    if len(band_array) < 3 :  #Checks if array is empty
        return 7  #Integer to let microprocessor know the no bin was determined
    elif band_array[0] == 2 and band_array[1] == 2 or band_array[-1] == 2 and band_array[-2] == 2:  #Send to bin 3
        return 10
    elif band_array[0] == 3 and band_array[1] == 3 or band_array[-1] == 3 and band_array[-2] == 3:  #Send to bin 4
        return 11
    elif band_array[0] == 4 and band_array[1] == 7 or band_array[-1] == 4 and band_array[-2] == 7:  #Send to bin 5
        return 12
    elif band_array[0] == 5 and band_array[1] == 6 or band_array[-1] == 5 and band_array[-2] == 6:  #Send to bin 6
        return 13
    elif band_array[0] == 6 and band_array[1] == 8 or band_array[-1] == 6 and band_array[-2] == 8:  #Send to bin 7
        return 14
    elif band_array[0] == 8 and band_array[1] == 2 or band_array[-1] == 8 and band_array[-2] == 2:  #Send to bin 8
        return 15
    elif band_array[0] == 1 and band_array[1] == 5 or band_array[-1] == 1 and band_array[-2] == 5:  #Send to bin 2
        return 9
    elif (band_array[0] == 1 and band_array[1] == 0 and band_array[2] == 0) or (band_array[-1] == 1 and band_array[-2] == 0 and band_array[-3] == 0):
        return 8
    else:
        return 7  #Integer to let microprocessor know the no bin was determined


#  Old function to determine the coordinates. Was replaced by line_bisection_coords1
def line_bisection_coords(color_array1, pixel_var):  #Returns the x and y values of the 4 coordinates used to define the

    # body of the resistor
    length1, width1 = color_array1.shape  # length1 is the number of elements for height
    # width1 is number of elements in the x-axis
    index1 = 0  # Index Variable
    top_left_x = 0  # X Index value of top left coordinate
    top_left_y = 0  # Y Index value of top left coordinate
    top_right_x = 0  # X Index value of top right coordinate
    top_right_y = 0  # Y Index value of top right coordinate
    bottom_left_x = 0  # X Index value of bottom left coordinate
    bottom_left_y = 0  # Y Index value of bottom left coordinate
    bottom_right_x = 0  # X Index value of bottom right coordinate
    bottom_right_y = 0  # Y Index value of bottom right coordinate

    threshold1 = pixel_var * 255  # Arbitrarily defined threshold
    while index1 < width1:
        if color_array1[:, index1].sum() > threshold1:  # Checks if row contains threshold number of white pixels
            top_left_x = index1  # Identifies top left x index
            top_left_y = index_finder(color_array1[:, index1], True)  # Identfies top left y index
            index1 = width1  # End while loop
        else:
            index1 += 1  # Increases increment by 1
    index1 = 0
    while index1 < length1:
        if color_array1[index1].sum() > threshold1:
            top_right_y = index1
            top_right_x = index_finder(color_array1[index1], False)
            index1 = length1
        else:
            index1 += 1  # Increases increment by 1
    index1 = 0
    while index1 < width1:
        if color_array1[:, width1 - index1 - 1].sum() > threshold1:
            bottom_right_x = width1 - index1 - 1
            bottom_right_y = index_finder(color_array1[:, width1 - index1 - 1], False)
            index1 = width1
        else:
            index1 += 1  # Increases increment by 1

    index1 = 0
    while index1 < length1:
        if color_array1[length1 - index1 - 1].sum() > threshold1:
            bottom_left_y = length1 - index1 - 1
            bottom_left_x = index_finder(color_array1[length1 - index1 - 1], True)
            index1 = length1
        else:
            index1 += 1  # Increases increment by 1

    array1 = [top_left_x, top_left_y, top_right_x, top_right_y, bottom_right_x, bottom_right_y,
              bottom_left_x, bottom_left_y]
    return array1


#  Function that would determine the index of the first or last nonzero element of an array
def index_finder(array1, direction_determiner):
    index1 = 0
    length1 = len(array1)
    if direction_determiner:  # Checks if Direction Determiner boolean variable is True
        while index1 < length1:
            if array1[index1] > 0:
                return index1
            else:
                index1 += 1  # Increases increment by 1
    else:
        while index1 < length1:
            if array1[length1 - index1 - 1] > 0:
                return length1 - index1 - 1
            else:
                index1 += 1  # Increases increment by 1
    return 0


#  Function that determines the distance between two points given their x and y coordinates
def dist_determ(x_coord1, y_coord1, x_coord2, y_coord2):
    return math.sqrt((x_coord1 - x_coord2)**2 + (y_coord1-y_coord2)**2)


def pixel_glare_color_determ(x_coord, y_coord, slope, orientation, color_array, image_array, distance_var, height1, width1):
    distance_new_pixel_var = distance_var
    if slope != 0:
        new_slope = -slope
    else:
        new_slope = slope
    if orientation:  # Resistor is more Vertical
        new_coord_y1 = int(round(distance_new_pixel_var * new_slope + y_coord))
        new_coord_y2 = int(round(-distance_new_pixel_var * new_slope + y_coord))
        if new_coord_y1 < height1 and (x_coord + distance_new_pixel_var) < width1:
            new_pixel_color1 = color_determ_color_chart_return(
                    image_array[new_coord_y1][x_coord + distance_new_pixel_var][0],
                    image_array[new_coord_y1][x_coord + distance_new_pixel_var][1],
                    image_array[new_coord_y1][x_coord + distance_new_pixel_var][2])
            new_pixel_color2 = color_determ_color_chart_return(
                    image_array[new_coord_y2][x_coord - distance_new_pixel_var][0],
                    image_array[new_coord_y2][x_coord - distance_new_pixel_var][1],
                    image_array[new_coord_y2][x_coord - distance_new_pixel_var][2])
        else:
            new_pixel_color1 = 11
            new_pixel_color2 = color_determ_color_chart_return(
                    image_array[new_coord_y2][x_coord - distance_new_pixel_var][0],
                    image_array[new_coord_y2][x_coord - distance_new_pixel_var][1],
                    image_array[new_coord_y2][x_coord - distance_new_pixel_var][2])
        image_array[new_coord_y1][x_coord + distance_new_pixel_var][0] = 255
        image_array[new_coord_y2][x_coord - distance_new_pixel_var][0] = 255
        #print(new_coord_y1, x_coord + distance_new_pixel_var, new_pixel_color1, distance_var, 1, "V")
        #print(new_coord_y2, x_coord - distance_new_pixel_var, new_pixel_color2, distance_var, 2, "V")
    else: # Resistor is more Horizontal
        new_coord_x1 = int(round(distance_new_pixel_var * new_slope + x_coord))
        new_coord_x2 = int(round(-distance_new_pixel_var * new_slope + x_coord))
        if new_coord_x1 < width1 and (y_coord + distance_new_pixel_var) < height1:
            new_pixel_color1 = color_determ_color_chart_return(
                    image_array[y_coord + distance_new_pixel_var][new_coord_x1][0],
                    image_array[y_coord + distance_new_pixel_var][new_coord_x1][1],
                    image_array[y_coord + distance_new_pixel_var][new_coord_x1][2])
            new_pixel_color2 = color_determ_color_chart_return(
                    image_array[y_coord - distance_new_pixel_var][new_coord_x2][0],
                    image_array[y_coord - distance_new_pixel_var][new_coord_x2][1],
                    image_array[y_coord - distance_new_pixel_var][new_coord_x2][2])
        else:
            new_pixel_color1 = 11
            new_pixel_color2 = color_determ_color_chart_return(
                    image_array[y_coord - distance_new_pixel_var][new_coord_x2][0],
                    image_array[y_coord - distance_new_pixel_var][new_coord_x2][1],
                    image_array[y_coord - distance_new_pixel_var][new_coord_x2][2])
        image_array[y_coord + distance_new_pixel_var][new_coord_x1][0] = 255
        image_array[y_coord - distance_new_pixel_var][new_coord_x2][0] = 255
        #print(y_coord + distance_new_pixel_var, new_coord_x1, new_pixel_color1, distance_var, 1, "H")
        #print(y_coord - distance_new_pixel_var, new_coord_x2, new_pixel_color2, distance_var, 2, "H")
    if new_pixel_color1 == new_pixel_color2 and new_pixel_color1 != 11:
        color_array[-1] = new_pixel_color1
    elif new_pixel_color1 == 11 and new_pixel_color2 == 11:
        pixel_glare_color_determ(x_coord, y_coord, slope, orientation, color_array, image_array, distance_var + 2, height1, width1)
    elif new_pixel_color1 == 11 and new_pixel_color2 != 11:
        color_array[-1] = new_pixel_color2
    elif new_pixel_color1 != 11 and new_pixel_color2 == 11:
        color_array[-1] = new_pixel_color1
    elif new_pixel_color1 == 12 and new_pixel_color2 != 12:
        color_array[-1] = new_pixel_color2
    elif new_pixel_color1 != 12 and new_pixel_color2 == 12:
        color_array[-1] = new_pixel_color1
    else:
        color_array[-1] = new_pixel_color2
    return None

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
            color_array1.append(color_determ_color_chart_return(
                image_array1[starter_index1][starter_index2][0],
                image_array1[starter_index1][starter_index2][1],
                image_array1[starter_index1][starter_index2][2]))

            if color_array1[-1] == 11:
                pixel_glare_color_determ(starter_index2, starter_index1, slope1, orientation3, color_array1,
                                              image_array1, 6, dimensions1[0], dimensions1[1])

            # Function that adds the pixels color determined by RGB to an array
            image_array1[starter_index1][starter_index2][1] = 255  #Assigns the pixel in the line green value
            hsv_color_array.append(color_determ_hsv(int(hsv_array1[starter_index1][starter_index2][0]),
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
            color_array1.append(color_determ_color_chart_return(
                image_array1[starter_index2][starter_index1][0],
                image_array1[starter_index2][starter_index1][1],
                image_array1[starter_index2][starter_index1][2]))

            if color_array1[-1] == 11:
                pixel_glare_color_determ(starter_index1, starter_index2, slope1, orientation3, color_array1,
                                              image_array1, 4, dimensions1[0], dimensions1[1])

            # Function that adds the pixels color determined by RGB to an array
            image_array1[starter_index2][starter_index1][1] = 255  #Assigns the pixel in the line green value
            hsv_color_array.append(color_determ_hsv(int(hsv_array1[starter_index2][starter_index1][0]),
                                                         int(hsv_array1[starter_index2][starter_index1][1]),
                                                         int(hsv_array1[starter_index2][starter_index1][2])))
            # Function that adds the pixels color determined by HSV to an array
            hsv_array1[starter_index2][starter_index1][1] = 0  #Assigns the pixel in the line 0 saturation value
            starter_index1 += 1  #Increases increment by 1
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


#  Function that creates the grayscale image of the Resistor where the body of the resistor appears as white
def color_array_filler(dimensions1, image_array1, color_array1):
    index1 = 0  #Itteration variable
    while index1 < dimensions1[0]:  #Iterates through the height of the image
        index2 = 0  #Itteration variable
        while index2 < dimensions1[1]:  #Iterates through the width of the image
            color_array1[index1][index2] = colordeterm(image_array1[index1][index2][0],
                                                            image_array1[index1][index2][1],
                                                            image_array1[index1][index2][2])
           # Fills in 2D grayscale matrix which will be used to identify body of the Resistor
            index2 += 1  #Increases increment by 1
        index1 += 1  #Increases increment by 1
    return None

