# Space Image Format

import numpy as np 

def load_image_data():
    with open('input8.txt') as f:
        line = f.readlines()
    return line[0]

def process_image(image_data, pixels_wide, pixels_tall):
    # split the image data into a matrix
    #print(pixels_wide, pixels_tall)
    #print(len(image_data))
    #print(type(image_data))
    #print(image_data)
    image_list = []
    for i in range(len(image_data)):
        image_list.append(image_data[i])

    n_layers = int(len(image_data) / (pixels_wide * pixels_tall))
    #print(n_layers)
    processed_image = np.reshape(image_list, (n_layers, pixels_tall, pixels_wide))
    # processed_image = np.zeros((n_layers, pixels_tall, pixels_wide))
    # for i in range(len(image_data)):
    #     for j in range(n_layers):
    #         for k in range(pixels_tall):
    #             for l in range(pixels_wide):
    #                 processed_image[j][k][l] = image_data[i] # this did not work because it replaced every digit with the last digit in image_data
    return processed_image

def print_output(processed_image):
    print('Output: ')
    # print(processed_image)
    # print(processed_image.shape)
    # print(len(processed_image))
    # print(len(processed_image[0]))
    # print(len(processed_image[0][0]))
    for i in range(len(processed_image)):
        for j in range(len(processed_image[i])):
            row = ''
            for k in range(len(processed_image[i][j])):
                row = row + processed_image[i][j][k]
            if(j == 0):
                print('Layer ' + str(i+1) + ': ' + row)
            else:
                print('\t ' + row)
    print('Output should be: ')
    print('Layer 1: 123\n\t 456\n')
    print('Layer 2: 789\n\t 012')

def find_layer_with_fewest_0_digits(processed_image):
    # loop through the processed image and identify the layer with the minimum amount of zeros
    n_zeros = []
    for i in range(len(processed_image)): # loop over each layer
        zeros_count = 0
        for j in range(len(processed_image[i])): # loop over each row
            for k in range(len(processed_image[i][j])): # loop over each digit
                digit = processed_image[i][j][k]
                if(digit == '0'):
                    zeros_count += 1
        n_zeros.append(zeros_count)
    #print(n_zeros)
    zerosparselayer = processed_image[np.argmin(n_zeros)]    
    return zerosparselayer

def mult_1_digits_by_2_digits(zerosparselayer):
    # multiply the number of 1 digits by the number of 2 digits
    ones_count = 0
    twos_count = 0
    for i in range(len(zerosparselayer)): # looping over each row
        for j in range(len(zerosparselayer[i])): # looping over each digit
            digit = zerosparselayer[i][j]
            if(digit == '1'):
                ones_count += 1
            elif(digit == '2'):
                twos_count += 1 
    return ones_count * twos_count

print('Example: ')
pixels_wide = 3
pixels_tall = 2
image_data = '123456789012'
processed_image = process_image(image_data, pixels_wide, pixels_tall)
#print_output(processed_image)

print('Puzzle: ')
pixels_wide = 25
pixels_tall = 6
image_data = load_image_data()
processed_image = process_image(image_data, pixels_wide, pixels_tall)
zerosparselayer = find_layer_with_fewest_0_digits(processed_image)
answer = mult_1_digits_by_2_digits(zerosparselayer)
print(answer)
# 1703 was the correct answer

# Part 2
def stack_layers(processed_image):
    stacked_image = np.zeros((processed_image.shape[1], processed_image.shape[2]))
    #TODO start with last layer and go towards the front, replacing if not transparent
    stacked_image = processed_image[-1] # starts with last layer 
    for i in range(len(processed_image) - 1, 0, -1): # looping through layers in reverse order
        for j in range(len(processed_image[i])): # looping through rows
            for k in range(len(processed_image[i][j])):
                digit = processed_image[i][j][k]
                # replace it if it isn't transparent
                if(digit != 2):
                    stacked_image[j][k] = digit 
    return stacked_image

def print_image(image):
    print('Image: ')
    for i in range(len(image)): # looping through each row
        row = ''
        for j in range(len(image[i])): # looping through each digit
            digit = image[i][j]
            if(digit == '2'):
                row = row + ' '
            else:
                row = row + digit
            #row = row + image[i][j]
        print(row)

stacked_image = stack_layers(processed_image)
print_image(stacked_image)