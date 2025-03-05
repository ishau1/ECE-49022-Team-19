
import numpy as np
import math


#  Function used to create grayscale image of resistor with body of the resistor appearing as white
def colordeterm(red, green, blue):
    red = int(red)
    green = int(green)
    blue = int(blue)
    sum1 = red + green + blue


    if sum1 > 120*3:
        value = 0
        valueint8 = np.uint8(value)
        return valueint8
    elif ((red - blue) > 16 and (red - green) > 7) or ((blue - red) > 15) or blue > 4*red:
        value = 255
        valueint8 = np.uint8(value)
        return valueint8
    else:
        value = 0
        valueint8 = np.uint8(value)
        return valueint8


#  Function using RGB used to determine pixel color associated with resistor color chart
def color_determ_color_chart_return(red, green, blue):
    red = int(red)
    green = int(green)
    blue = int(blue)
    sum1 = red + green + blue
    if red > 3*green and red > 3*blue:  #Determines Red
        return 2
    elif (blue - red) > 25 and (blue - green) > 5 and sum1 >= 150:  #Determines Resistor Background Color Light Blue
        return 12
    elif sum1 < 40:  #Determines Black
        return 0
    elif red >= 4*green and red >= 4*blue and sum1 <= 50:  #Determines Brown
        return 1
    elif (red - blue) >= 40 and (red - green) >= 15:  #Determines Orange
        return 3
    elif (green - blue) >= 50 and (green - red) >= 10:  #Determines Yellow
        return 4
    elif (green - red) >= 10 and (green - blue) >= 10:  #Determines Green
        return 5
    elif green <= (blue - 15) and red <= (blue - 15) and (sum1 <= 70):  #Determines Purple
        return 7
    elif (blue - red) >= 50 and (blue - green) >= 40:  #Determines Blue
        return 6
    #  Determines Gray
    elif abs(red - blue) <= 15 and abs(red - green) <= 15 and abs(blue - green) <= 15 and sum1 <= 160:
        return 8
    else:  #Determines pixel color to be none of the above
        return 12


def color_determ_hsv(hue, saturation, value):
    if value <= 15:  #Determines if pixel is black
        return 0
    elif (hue <= 80) and (hue >= 76):  #Determines if pixel is yellow
        return 4
    elif (hue <= 5 or hue >= 176) and (value <= 15):  #Determines if pixel is purple
        return 7
    elif (hue <= 105) and (hue >= 100) and (saturation >= 170) and (value >= 70):  #Determines if pixel is orange
        return 3
    elif (hue <= 125) and (hue >= 115) and (value >= 20):  #Determines if pixel is red
        return 2
    elif (hue >= 4) and (hue <= 20) and (value <= 35):  #Determines if pixel is blue
        return 6
    else:  #Determines pixel to be none of the above
        return 12

#  Function to determine which bin the resistor is to be sent to
def bin_determ(band_array):
    if band_array[0] == 2 and band_array[1] == 2 or band_array[-1] == 2 and band_array[-2] == 2:  #Send to bin 3
        return 3
    elif band_array[0] == 3 and band_array[1] == 3 or band_array[-1] == 3 and band_array[-2] == 3:  #Send to bin 4
        return 4
    elif band_array[0] == 4 and band_array[1] == 7 or band_array[-1] == 4 and band_array[-2] == 7:  #Send to bin 5
        return 5
    elif band_array[0] == 5 and band_array[1] == 6 or band_array[-1] == 5 and band_array[-2] == 6:  #Send to bin 6
        return 6
    elif band_array[0] == 6 and band_array[1] == 8 or band_array[-1] == 6 and band_array[-2] == 8:  #Send to bin 7
        return 7
    elif band_array[0] == 8 and band_array[1] == 2 or band_array[-1] == 8 and band_array[-2] == 2:  #Send to bin 8
        return 8
    elif band_array[0] == 1 and band_array[1] == 5 or band_array[-1] == 1 and band_array[-2] == 5:  #Send to bin 2
        return 2
    elif band_array[0] == 1 and band_array[1] == 0 or band_array[-1] == 1 and band_array[-2] == 0:  #Send to bin 1
        return 1
    else:
        return 0  #Integer to let microprocessor know the no bin was determined


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
        print(new_coord_y1, x_coord + distance_new_pixel_var, new_pixel_color1, distance_var, 1, "V")
        print(new_coord_y2, x_coord - distance_new_pixel_var, new_pixel_color2, distance_var, 2, "V")
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
        print(y_coord + distance_new_pixel_var, new_coord_x1, new_pixel_color1, distance_var, 1, "H")
        print(y_coord - distance_new_pixel_var, new_coord_x2, new_pixel_color2, distance_var, 2, "H")
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

