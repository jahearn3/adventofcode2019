
import numpy as np 

# Monitoring Station

def load_field(filename):
    with open(filename) as f:
        lines = f.readlines()
    return lines

def identify_asteroids(field):
    asteroids = []
    for i in range(len(field)):
        for j in range(len(field[i])):
            if(field[i][j] == '#'):
                asteroids.append((j,i)) # (x,y)
                #asteroids.append(eval('(' + str(j) + ',' + str(i) + ')')) # eval converts the string to a tuple
                #asteroids.append(zip(j,i)) # appends the x and y coordinates to the list of asteroids
    return asteroids

def find_best_asteroid(asteroids):
    best = np.zeros(3) # will store the x,y coordinates and the number of asteroids observable from the best asteroid
    for asteroid in asteroids:
        slopes = []
        for other_asteroid in asteroids:
            if(asteroid != other_asteroid):
                rise = other_asteroid[1] - asteroid[1] 
                run = other_asteroid[0] - asteroid[0]
                if(run != 0):
                    slope = rise / run
                    #slopes.append(rise / run)
                else:
                    slope = np.inf 
                    #slopes.append(np.inf)
                # define side as leading or trailing (in the asteroid's orbit, assuming the orbital direction is in the positive y direction)
                # leading = other_asteroid is in quadrants 1 or 2 compared to the current asteroid
                # trailing = other_asteroid is in quadrants 3 or 4 compared to the current_asteroid 
                # exception: if the slope is 0 (horizontal line), then we define:
                # leading = other_asteroid is between quadrants 2 and 3 (i.e., assume the center of mass is on the left)
                # trailing = other_asteroid is between quadrants 4 and 1
                side = 'leading' # will redefine as trailing if it is not in fact leading
                if(slope == 0):
                    if(other_asteroid[0] > asteroid[0]):
                        side = 'trailing'
                elif(other_asteroid[1] > asteroid[1]):
                    side = 'trailing'
                slopes.append((slope, side))
        #TODO need to add another variable paired with slopes just to say on what side the other asteroid is on, could be a positive/negative, True/False, spin up/spin down, etc. 
        #print('Slopes: ' + str(len(slopes)))
        #print(slopes)
        count = len(set(slopes)) # counting unique slopes falls short because asteroids could have the same slope but be on opposite sides of the asteroid in question
        # add to the count if for the same slope two asteroids are on opposite sides of the asteroid in question
        #count_add = 0
        #TODO The following will not solve it either because there could be more than one asteroid on either side of the asteroid in question, so it could overcount the asteroids
        # for second_asteroid in asteroids:
        #     for third_asteroid in asteroids:
        #         if((asteroid != second_asteroid) and (asteroid != third_asteroid) and (second_asteroid != third_asteroid)):
        #             if((second_asteroid[1] - asteroid[1]) / (second_asteroid[0] - asteroid[0]) == (third_asteroid[1] - asteroid[1]) / (third_asteroid[0] - asteroid[0])): # if the slope between ast and ast2 equals the slope between ast and ast3
        #                 if(second_asteroid[0] <= asteroid[0] <= third_asteroid[0]) or (second_asteroid[0] >= asteroid[0] >= third_asteroid[0]): # comparing x coordinates
        #                     if(second_asteroid[1] <= asteroid[1] <= third_asteroid[1]) or (second_asteroid[1] >= asteroid[1] >= third_asteroid[1]): # comparing y coordinates
        #                         count_add += 1
        #                         print('Adding 1 for the asteroid at ' + str(asteroid) + '... ' )
        #                         print('...because ' + str(second_asteroid) + ' and ' + str(third_asteroid) + ' have a slope of ' + str((second_asteroid[1] - asteroid[1]) / (second_asteroid[0] - asteroid[0])))
        #TODO I think i and j in slopes do not correspond to i and j in asteroids, so I'm getting garbage output 
        # for i in range(len(slopes)):
        #     for j in range(len(slopes)):
        #         if(i != j) and (slopes[i] == slopes[j]):
        #             if(asteroids[i][0] <= asteroid[0] <= asteroids[j][0]) or (asteroids[i][0] >= asteroid[0] >= asteroids[j][0]): # comparing x coordinates
        #                 if(asteroids[i][1] <= asteroid[1] <= asteroids[j][1] or (asteroids[i][1] >= asteroid[1] >= asteroids[j][1])): # comparing y coordinates
        #                     count_add += 1
        #                     print('Adding 1 for the asteroid at ' + str(asteroid) + '... ' )
        #                     print('...because ' + str(asteroids[i]) + ' and ' + str(asteroids[j]) + ' have a slope of ' + str(slopes[i]))

        #count_add /= 2 # removes the double counting
        #count += count_add
        #print(str(count) + ' unique slopes')
        if(count > best[2]): # overwriting previous best if a better one is found 
            best[0] = int(asteroid[0])
            best[1] = int(asteroid[1])
            best[2] = int(count)
    return best 

for i in range(1,6):
    print('Example ' + str(i) + ':')
    field = load_field('day10example' + str(i) + '.txt')
    asteroids = identify_asteroids(field)
    print(str(len(asteroids)) + ' asteroids identified')
    best = find_best_asteroid(asteroids)
    print('Best is ' + str(int(best[0])) + ',' + str(int(best[1])) + ' with ' + str(int(best[2])) + ' other asteroids detected')
    if(i == 1):
        print('Should be 3,4 with 8 other asteroids detected')
    elif(i == 2):
        print('Should be 5,8 with 33 other asteroids detected')
    elif(i == 3):
        print('Should be 1,2 with 35 other asteroids detected')
    elif(i == 4):
        print('Should be 6,3 with 41 other asteroids detected')
    elif(i == 5):
        print('Should be 11,13 with 210 other asteroids detected')

print('Puzzle:')
field = load_field('input10.txt')
asteroids = identify_asteroids(field)
print(str(len(asteroids)) + ' asteroids identified')
best = find_best_asteroid(asteroids)
print('Best is ' + str(int(best[0])) + ',' + str(int(best[1])) + ' with ' + str(int(best[2])) + ' other asteroids detected')
# Answer was 326 other asteroids detected 