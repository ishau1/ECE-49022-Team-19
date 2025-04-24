import numpy as np
import math
import statistics



#  Function used to create grayscale image of resistor with body of the resistor appearing as white
def colordeterm(red, green, blue):
    red = int(red)  #Converts 8 bit red to integer
    green = int(green)  #Converts 8 bit green to integer
    blue = int(blue)  #Converts 8 bit blue to integer
    sum1 = red + green + blue  #Sums up the RGB values


    if sum1 > 200*3:  #Identifies white pixels
        value = 0  #Grayscale Value that the pixel will be changed to
        valueint8 = np.uint8(value)
        return valueint8  #Returns black pixel
    elif blue - red >= 60:  #Formula to Determine that the pixel is lightblue which is Resistor body color
        value = 255  #Grayscale Value that the pixel will be changed to
        valueint8 = np.uint8(value)
        return valueint8  #Returns white pixel
    else:
        value = 0  #Grayscale Value that the pixel will be changed to
        valueint8 = np.uint8(value)
        return valueint8  #Returns black pixel


#  Function using RGB used to determine pixel color associated with resistor color chart
def color_determ_color_chart_return(red, green, blue, gb_ratio):
    red = int(red)
    green = int(green)
    blue = int(blue)
    sum1 = red + green + blue
    if sum1 >= 650: # Determines White
        return 13
    elif red >= 120 and green >= 120 and blue >= 120 and sum1 >= 400:  # Determines Glare
        return 11
    elif (red - green) >= 25 and (red - blue) >= 25 and (red <= 160 and green <= 75) and abs(green - blue) <= 20 \
            and red >= 40:  #Determines Red
        return 2
    elif blue >= 160 and green >= 100 and (2*green > blue):  #Determines Resistor Background Color Light Blue
        return 12
    elif (blue - green > 50) and (green - red > 40) and gb_ratio > 1.7:
        return 12
    elif (blue - red > 120) and (green - red > 80) and gb_ratio < 1.25:
        return 12
    elif sum1 <= 50:
        if (red >= 5*green and red >= 5*blue) or (red - green >= 5 and red - blue >= 5):
            return 1
        elif green > blue and blue > red and (green - red >= 15):
            return 5
        elif (blue - green) >= 20 and (blue - red) >= 25 and blue >= 45:
            return 7
        else:
            return 0
    elif sum1 < 100 and abs(red - blue) <= 15 and abs(red - green) <= 15:  #Determines Black
        return 0
    elif sum1 < 100 and red >= 40 and red - green >= 0 and red - blue >= 0:  #Determines Brown
        return 1
    elif (red >= green + 20) and (blue + 20 <= red) and red <= 80:  #Determines Brown
        return 1
    elif red - green >= 15 and (green - blue >= 20) and (red - blue >= 40) and red >= 75:  #Determines Orange
        return 3
    elif (green - red) >= 25 and (green - blue) >= 70:  #Determines Yellow
        return 4
    elif green >= 3*red and green >= 2*blue and green >= 40 or (green - red >= 25
                                                                and green - blue >= 25 and green >= 40):
        # Determines Green
        return 5
    elif blue >= 4*red and green <= 60 and blue >= 105 and (red + green >= 10) and gb_ratio < 1.8:  #Determines Blue
        return 6
    elif blue >= 4*red and green <= 30 and blue >= 3*green and blue >= 40 and blue <= 100  and gb_ratio > 1.8:  #Determines Blue
        return 6
    elif green <= (blue - 20) and red <= (blue - 20) and abs(green - red) <= 25 and green <= 50:  #Determines Purple
        return 7
    elif green <= (blue - 80) and green > red and green <= 50 and gb_ratio > 2:
        return 7
    #  Determines Gray
    elif abs(red - blue) <= 25 and abs(red - green) <= 25 and abs(blue - green) <= 25 and sum1 >= 105 and green >= red:
        # Determines Gray
        return 8
    elif sum1 >= 75 and abs(red - blue) <= 15 and abs(red - green) <= 15 and abs(blue - green) <= 15 and green > red:
        # Determines Gray
        return 8
    elif (sum1 >= 150 and green > red and blue > red and abs(green - blue) <= 15 and abs(green - red) <= 50 and sum1 <= 300
          and abs(blue - red) <= 50 and red >= 45):
        # Determines Gray
        return 8
    elif (red <= 60 and green >= 50 and blue >= 65 and green <= 135 and blue <= 150 and ((green - red) >= 20)
          and ((blue - red) >= 35) and red >= 10 and (abs(blue - green) <= 25)):
        # Determines Gray
        return 8
    elif green >= 4*red and green >= blue and green >= 35 and (green - red >= 30):  # Determines Green
        return 5
    elif green > blue and blue > red and green <= 75 and green >= 20 and (green - red >= 15):
        return 5
    elif sum1 <= 75 and (red - 10 >= green) and (red - 10 >= blue):
        return 1
    elif red - 5 >= green and red - 5 >= blue and red >= 40 and blue >= 25 and green >= 25:
        return 1
    else:  #Determines pixel color to be none of the above
        return 11


#  Function to determine which bin the resistor is to be sent to
def bin_determ(band_array, ratio1):
    count5s = band_array.count(5)
    count3s = band_array.count(3)
    count8s = band_array.count(8)
    count6s = band_array.count(6)
    count7s = band_array.count(7)
    count2s = band_array.count(2)
    count1s = band_array.count(1)
    count0s = band_array.count(0)
    sum01s = count0s + count1s
    sum012s = sum01s + count2s
    sum23s = count2s + count3s
    sum67s = count6s + count7s
    if len(band_array) < 3 :  #Checks if array is empty
        return 7  #Integer to let microprocessor know the no bin was determined
    if band_array[0] == 6 or band_array[0] == 7 or band_array[-1] == 6 or band_array[-1] == 7:  # Send to bin 7
        return 14
    if (ratio1 <= 1.2 or ratio1 > 1.65) and count8s == 0:
        if count5s and ratio1 > 1.65:
            return 9
        elif count2s >= 3 and ratio1 > 2.1:
            return 10
        elif sum23s >= 2 and sum67s == 0 and count5s == 0:
            return 11
        else:
            return 8


    elif band_array[0] == 8 and band_array[1] == 2 or band_array[-1] == 8 and band_array[-2] == 2:  #Send to bin 8
        return 15
    elif count3s == 1 and count2s == 1 and sum012s >= 3:
        return 10
    elif band_array[0] == 6 and band_array[1] == 8 or band_array[-1] == 6 and band_array[-2] == 8:  #Send to bin 7
        return 14
    elif band_array[0] == 7 and band_array[1] == 8 or band_array[-1] == 7 and band_array[-2] == 8:  #Send to bin 7
        return 14
    elif band_array[0] == 5 and band_array[1] == 6 or band_array[-1] == 5 and band_array[-2] == 6:  #Send to bin 6
        return 13
    elif band_array[0] == 4 and band_array[1] == 7 or band_array[-1] == 4 and band_array[-2] == 7:  #Send to bin 5
        return 12
    elif band_array[0] == 4 and band_array[1] == 6 or band_array[-1] == 4 and band_array[-2] == 6:  #Send to bin 5
        return 12
    elif band_array[0] == 3 and band_array[1] == 3 or band_array[-1] == 3 and band_array[-2] == 3:  #Send to bin 4
        return 11
    elif band_array[0] == 2 and band_array[1] == 2 or band_array[-1] == 2 and band_array[-2] == 2:  #Send to bin 3
        return 10
    elif band_array[0] == 1 and band_array[1] == 5 or band_array[-1] == 1 and band_array[-2] == 5:
        return 9
    elif band_array[0] == 2 and band_array[1] == 5 or band_array[-1] == 2 and band_array[-2] == 5:  #Send to bin 2
        return 9
    elif band_array[0] == 1 and band_array[1] == 0 and band_array[2] == 0:
        return 8
    elif band_array[-1] == 1 and band_array[-2] == 0 and band_array[-3] == 0:
        return 8
    elif band_array[0] == 2 and band_array[1] == 0 and band_array[2] == 0:
        return 8
    elif band_array[-1] == 2 and band_array[-2] == 0 and band_array[-3] == 0:
        return 8
    elif sum01s >= 3:
        return 11
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


def pixel_glare_color_determ(x_coord, y_coord, slope, orientation, color_array, image_array, distance_var, height1, width1, color_orig, bg_ratio):
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
                    image_array[new_coord_y1][x_coord + distance_new_pixel_var][2],
                    bg_ratio)
            new_pixel_color2 = color_determ_color_chart_return(
                    image_array[new_coord_y2][x_coord - distance_new_pixel_var][0],
                    image_array[new_coord_y2][x_coord - distance_new_pixel_var][1],
                    image_array[new_coord_y2][x_coord - distance_new_pixel_var][2],
                    bg_ratio)
            image_array[new_coord_y1][x_coord + distance_new_pixel_var][0] = 255
        else:
            new_pixel_color1 = 13
            new_pixel_color2 = color_determ_color_chart_return(
                    image_array[new_coord_y2][x_coord - distance_new_pixel_var][0],
                    image_array[new_coord_y2][x_coord - distance_new_pixel_var][1],
                    image_array[new_coord_y2][x_coord - distance_new_pixel_var][2],
                    bg_ratio)
            image_array[new_coord_y1][x_coord][0] = 255
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
                    image_array[y_coord + distance_new_pixel_var][new_coord_x1][2],
                    bg_ratio)
            new_pixel_color2 = color_determ_color_chart_return(
                    image_array[y_coord - distance_new_pixel_var][new_coord_x2][0],
                    image_array[y_coord - distance_new_pixel_var][new_coord_x2][1],
                    image_array[y_coord - distance_new_pixel_var][new_coord_x2][2],
                    bg_ratio)
            image_array[y_coord + distance_new_pixel_var][new_coord_x1][0] = 255
        else:
            new_pixel_color1 = 13
            new_pixel_color2 = color_determ_color_chart_return(
                    image_array[y_coord - distance_new_pixel_var][new_coord_x2][0],
                    image_array[y_coord - distance_new_pixel_var][new_coord_x2][1],
                    image_array[y_coord - distance_new_pixel_var][new_coord_x2][2],
                    bg_ratio)
            image_array[y_coord][new_coord_x1][0] = 255
        image_array[y_coord - distance_new_pixel_var][new_coord_x2][0] = 255
        #print(y_coord + distance_new_pixel_var, new_coord_x1, new_pixel_color1, distance_var, 1, "H")
        #print(y_coord - distance_new_pixel_var, new_coord_x2, new_pixel_color2, distance_var, 2, "H")
    pixel_color_array = [color_orig, new_pixel_color1, new_pixel_color2]
    count0s = pixel_color_array.count(0)
    count1s = pixel_color_array.count(1)
    count2s = pixel_color_array.count(2)
    sum01s = count0s + count1s
    sum12s = count1s + count2s
    mode1 = statistics.mode(pixel_color_array)
    if len(set(pixel_color_array)) == 1 and mode1 != 11:
        color_array[-1] = color_orig
    elif pixel_color_array.count(mode1) == 2 and mode1 != 11:
        color_array[-1] = mode1
    elif sum01s == 2 and color_orig != 0 and color_orig != 1:
        pixel_glare_color_determ(x_coord, y_coord, slope, orientation, color_array, image_array, distance_var + 4, height1, width1, 0, bg_ratio)
    elif sum12s == 2:
        color_array[-1] = 2
        #pixel_glare_color_determ(x_coord, y_coord, slope, orientation, color_array, image_array, distance_var + 4, height1, width1, 1)
    else:
        pixel_glare_color_determ(x_coord, y_coord, slope, orientation, color_array, image_array, distance_var + 4, height1, width1, color_orig, bg_ratio)
    return None

#  Function that determines the x and y coordinates of the 4 vertices that define location of the body of the Resistor
def line_bisection_coords1(color_array2, pixel_var, orientation_var, height1, width1):
    index1 = 0  #Itteration variable
    threshold1 = pixel_var*255*2.5  #Arbitrary threshold voltage
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
        nonzero_array_top = np.nonzero(color_array2[row_top])[0]
        nonzero_array_bottom = np.nonzero(color_array2[row_bottom])[0]
        if len(nonzero_array_top) <= 1 or len(nonzero_array_bottom) <= 1:
            top_left_x = 0
            top_right_x = 0
            bottom_left_x = 0
            bottom_right_x = 0
        else:
            top_left_x = int(nonzero_array_top[0])
            top_right_x = int(nonzero_array_top[-1])
            bottom_left_x = int(nonzero_array_bottom[0])
            bottom_right_x = int(nonzero_array_bottom[-1])
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
        nonzero_array_left = np.nonzero(color_array2[:, col_left])[0]
        nonzero_array_right = np.nonzero(color_array2[:, col_right])[0]
        if len(nonzero_array_left) <= 1 or len(nonzero_array_right) <= 1:
            top_left_y = 0
            top_right_y = 0
            bottom_left_y = 0
            bottom_right_y = 0
        else:
            top_left_y = int(nonzero_array_left[0])
            top_right_y = int(nonzero_array_right[0])
            bottom_left_y = int(nonzero_array_left[-1])
            bottom_right_y = int(nonzero_array_right[-1])

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
    jump_number = 8
    length1 = len(long_array)  #Determines the length of the array
    while index1 < (length1 - 4):  #Iterates through all color values of array except final 4
        if long_array[index1] != long_array[index1 + 1]:  #Checks for change in pixel value
            array1 = long_array[index1 + 1:index1 + 5]  #Creates an array of the next 4 color values in the array
            median1 = statistics.median(array1)  #Determines the median of the new array
            sum1 = array1.count(median1)  #Determines the number of times the median value of the new array occurs
            count2s = array1.count(2)
            count1s = array1.count(1)
            count0s = array1.count(0)
            count8s = array1.count(8)
            sum1and0 = count0s + count1s
            sum1and2 = count1s + count2s
            if count8s == 4:
                short_array.append(long_array[index1 + 1])
                if index1 <= (length1 - jump_number) and not (long_array[index1 + 1] == 12 or
                                                     long_array[index1 + 1] == 11 or long_array[index1 + 1] == 13):
                    # Checks if index value is less than 10 from max value
                    index1 += jump_number  #Jumps 10 pixel in order to leap pass pixel band which it is currently in
            elif sum1 >= 3 and median1 == long_array[index1 + 1] and median1 != 8:  #Determines if the change in pixels should result in
                # new pixel being added to the short_array
                short_array.append(long_array[index1 + 1])  #Adds integer to short_array
                if index1 <= (length1 - jump_number) and not (long_array[index1 + 1] == 12 or
                                                     long_array[index1 + 1] == 11 or long_array[index1 + 1] == 13):
                    # Checks if index value is less than 10 from max value
                    index1 += jump_number  #Jumps 10 pixel in order to leap pass pixel band which it is currently in
            elif sum1and0 >= 3:
                if count1s < count0s:
                    short_array.append(0)
                else:
                    short_array.append(1)
                if index1 <= (length1 - jump_number):
                    index1 += jump_number  #Jumps 10 pixel in order to leap pass pixel band which it is currently in
            elif sum1and2 >= 3:
                short_array.append(2)
                if index1 <= (length1 - jump_number):
                    index1 += jump_number

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
#  Function that determines the colors associated with that pixel using an RGB function
def color_array_line_plotter(slope1, y_int1, x_coord1, y_coord1, x_coord2, y_coord2, orientation3, color_array1,
                             image_array1, color_array2, bg_ratio):
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
                image_array1[starter_index1][starter_index2][2],
                bg_ratio))

            #if color_array1[-1] == 11 or color_array1[-1] == 8 or color_array1[-1] == 2 or color_array1[-1] == 1 or color_array1[-1] == 6:
            pixel_glare_color_determ(starter_index2, starter_index1, slope1, orientation3, color_array1,
                                              image_array1, 8, dimensions1[0], dimensions1[1], color_array1[-1], bg_ratio)

            # Function that adds the pixels color determined by RGB to an array
            image_array1[starter_index1][starter_index2][1] = 255  #Assigns the pixel in the line green value
            if starter_index1 == y_coord1:
                image_array1[starter_index1][starter_index2][0] = 255


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
                image_array1[starter_index2][starter_index1][2],
                bg_ratio))

            #if color_array1[-1] == 11 or color_array1[-1] == 8 or color_array1[-1] == 2 or color_array1[-1] == 1 or color_array1[-1] == 6:
            pixel_glare_color_determ(starter_index1, starter_index2, slope1, orientation3, color_array1,
                                              image_array1, 8, dimensions1[0], dimensions1[1], color_array1[-1], bg_ratio)

            # Function that adds the pixels color determined by RGB to an array
            image_array1[starter_index2][starter_index1][1] = 255  #Assigns the pixel in the line green value
            if starter_index1 == x_coord1:
                image_array1[starter_index2][starter_index1][0] = 255
            starter_index1 += 1  #Increases increment by 1
    return None


#  Function that determines the slope and y-intercept of the line that bisects the body of the Resistor
def slope_determ(x_coord1, y_coord1, x_coord2, y_coord2):
    if x_coord1 == x_coord2:  #Checks if x coordinates are identical as slope would be infinity in that case

        return 0, x_coord1  #Returns 0 because slope will be 0 when iterating across y-axis values
    slope1 = (y_coord2 - y_coord1)/(x_coord2 - x_coord1)
    if abs(slope1) > 1.0:  #Checks if slope is greater than 1 so it can have its inverse be the slope
        slope1 = 1/slope1
    if abs(x_coord2 - x_coord1) > abs(y_coord2 - y_coord1):  #Checks if Resistor is more horizontal or vertical
        b = -slope1*x_coord1 + y_coord1  #Determines y-intercept is Resistor is more horizontal
    else:
        b = -slope1*y_coord1 + x_coord1  #Determines y-intercept is Resistor is more vertical
    return slope1, b


#  Function that creates the grayscale image of the Resistor where the body of the resistor appears as white
def color_array_filler(dimensions1, image_array1, color_array1, x_array1, y_array1):
    index1 = 0  #Itteration variable
    while index1 < dimensions1[0]:  #Iterates through the height of the image
        index2 = 0  #Itteration variable
        while index2 < dimensions1[1]:  #Iterates through the width of the image
            color_array1[index1][index2] = colordeterm(image_array1[index1][index2][0],
                                                            image_array1[index1][index2][1],
                                                            image_array1[index1][index2][2])
            if color_array1[index1][index2]:
                x_array1.append(index2)
                y_array1.append(index1)

           # Fills in 2D grayscale matrix which will be used to identify body of the Resistor
            index2 += 1  #Increases increment by 1
        index1 += 1  #Increases increment by 1
    return None

def critical_points_determ(orientation1, coords, final_slope):
    if abs(final_slope) < 0.07:
        var1 = 1
        var2 = 1
    elif final_slope >= 0.07 and final_slope < 0.15:
        var1 = 1.5
        var2 = 1
    elif final_slope >= 0.15 and final_slope < 0.25:
        var1 = 2
        var2 = 1
    elif final_slope >= 0.25 and final_slope < 0.4:
        var1 = 3
        var2 = 1
    elif final_slope >= 0.4 and final_slope < 0.7:
        var1 = 5
        var2 = 1
    elif final_slope >= 0.7:
        var1 = 7
        var2 = 1
    elif final_slope <= -0.07 and final_slope > -0.15:
        var1 = 1
        var2 = 1.5
    elif final_slope <= -0.15 and final_slope > -0.25:
        var1 = 1
        var2 = 2
    elif final_slope <= -0.25 and final_slope > -0.4:
        var1 = 1
        var2 = 3
    elif final_slope <= -0.4 and final_slope > -0.7:
        var1 = 1
        var2 = 5
    else:
        var1 = 1
        var2 = 7
    sum1 = var1 + var2
    if orientation1:  # True if body of resistor is orientated in a more vertical direction
        x1 = int((var1*coords[0] + var2*coords[2]) / sum1)  # Calculates left x value that will be used to determine bisecting line
        y1 = int((var2*coords[1] + var1*coords[3]) / sum1)  # Calculates left y value that will be used to determine bisecting line
        x2 = int((var1*coords[4] + var2*coords[6]) / sum1)  # Calculates right x value that will be used to determine bisecting line
        y2 = int((var2*coords[5] + var1*coords[7]) / sum1)  # Calculates right y value that will be used to determine bisecting line
    else:
        x1 = int((var1*coords[0] + var2*coords[6]) / sum1)  # Calculates left x value that will be used to determine bisecting line
        y1 = int((var1*coords[1] + var2*coords[7]) / sum1)  # Calculates left y value that will be used to determine bisecting line
        x2 = int((var2*coords[2] + var1*coords[4]) / sum1)  # Calculates right x value that will be used to determine bisecting line
        y2 = int((var2*coords[3] + var1*coords[5]) / sum1)  # Calculates right y value that will be used to determine bisecting line

    return x1, y1, x2, y2

def median_blue_determ(image_array, x_values, y_values):
    length1 = len(x_values)
    index1 = 0
    blue_values = []
    green_values = []
    while index1 < length1:
        blue_value_temp = image_array[y_values[index1]][x_values[index1]][2]
        green_value_temp = image_array[y_values[index1]][x_values[index1]][1]
        blue_values.append(blue_value_temp)
        green_values.append(green_value_temp)
        index1 += 1

    median_blue = np.median(blue_values)
    median_green = np.median(green_values)


    return median_blue, median_green

def array_to_band_integer(array1):
    filter_array = [x for x in array1 if x not in (11, 12, 13)]
    length1 = len(filter_array)
    count0s = filter_array.count(0)
    count1s = filter_array.count(1)
    count2s = filter_array.count(2)
    count3s = filter_array.count(3)
    count4s = filter_array.count(4)
    count5s = filter_array.count(5)
    count6s = filter_array.count(6)
    count7s = filter_array.count(7)
    sum012s = count0s + count1s + count2s
    sum23s = count2s + count3s
    sum13s = count1s + count3s
    sum07s = count0s + count7s
    sum45s = count4s + count5s
    median1 = statistics.median(filter_array)
    if math.ceil(median1) == math.floor(median1):
        median1 = int(median1)
    mode1 = statistics.mode(filter_array)
    countmode1 = filter_array.count(mode1)
    ratio1 = countmode1/length1



    if median1 == 8 and mode1 == 8 and ratio1 >= 0.75 and length1 >= 5:
        return 8
    else:
        filter_array1 = [x for x in filter_array if x != 8]

    if not filter_array1:
        return -1

    length1 = len(filter_array1)
    median1 = statistics.median(filter_array1)
    if math.ceil(median1) == math.floor(median1):
        median1 = int(median1)
    mode1 = int(statistics.mode(filter_array1))
    ratio1 = mode1/length1
    ratio012 = sum012s/length1
    ratio45 = sum45s/length1
    ratio5 = count5s/length1
    ratio07 = sum07s/length1
    ratio23 = sum23s/length1
    ratio13 = sum13s/length1

    if ratio012 >= 0.5 and count3s < 2:
        if count2s >= count1s and count2s >= 2:
            return 2
        if length1 >= 5:
            if ratio5 >= 0.75:
                return 5
            trimmed_array = filter_array1[1:-1]
            temp1 = int(statistics.median(trimmed_array))
            return temp1
        if count2s >= count1s and (mode1 == 2 or median1 == 2):
            return 2
        elif count1s >= count0s and count1s >= count2s:
            return 1
        else:
            return 0
    elif ratio45 >= 0.7 and length1 >= 5:
        trimmed_array = filter_array1[1:-1]
        temp1 = int(statistics.median(trimmed_array))
        return temp1
    elif ratio07 >= 0.8 and count7s >= count0s:
        return 7
    elif (ratio23 > 0.75 or ratio13 > 0.75) and count3s >= 2:
        return 3
    elif median1 == mode1:
        return median1
    elif length1 % 2 == 0 and isinstance(median1, int):
        return median1
    else:
        if isinstance(median1, float):
            return mode1
        else:
            return median1


def band_integer_determ1(long_array, short_array):
    index1 = 0  #Itteration variable
    length1 = len(long_array)  #Determines the length of the array
    while index1 < (length1 - 4):  #Iterates through all color values of array except final 4
        temp_array = [long_array[index1],long_array[index1 + 1], long_array[index1 + 2], long_array[index1 + 3]] #Checks for change in pixel value
        count = len([x for x in temp_array if x not in (12, 13)])
        if count >= 3:
            index2 = 1
            #if (index1 + index2 + 3) < (length1 - 1):
            while (index1 + 3 + index2) < (length1 - 1) and long_array[index1 + 2 + index2] not in (12, 13) or long_array[index1 + 3 + index2] not in (12, 13) and index2 <= 11:
                temp_array.append(long_array[index1 + 3 + index2])
                index2 += 1

            index1 = index1 + 2 + index2

            temp1 = array_to_band_integer(temp_array)
            if temp1 != -1:
                short_array.append(temp1)

        index1 = index1 + 1

    return None  #Currently outdated, does not affect main functions output

def orientation_determ2(slopeA, slopeB):
    if abs(slopeA) < abs(slopeB):
        orientation2 = False
        slope_final = slopeA
    else:
        orientation2 = True
        slope_final = slopeB

    return orientation2, slope_final
