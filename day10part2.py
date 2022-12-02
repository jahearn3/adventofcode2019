
import numpy as np 
import pandas as pd 

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
                asteroids.append(eval('(' + str(j) + ',' + str(i) + ')')) # eval converts the string to a tuple
    return asteroids

def get_slope(rise, run):
    if(run != 0):
        slope = rise / run
    else:
        slope = np.inf 
    return slope 

# need to add another variable paired with slopes just to say on what side the other asteroid is on, could be a positive/negative, True/False, spin up/spin down, etc.   
def get_side(slope, x1, x0, y1, y0):
    # define side as leading or trailing (in the asteroid's orbit, assuming the orbital direction is up)
    # leading = other_asteroid is in quadrants 1 or 2 compared to the current asteroid
    # trailing = other_asteroid is in quadrants 3 or 4 compared to the current_asteroid 
    # exception: if the slope is 0 (horizontal line), then we define:
    # leading = other_asteroid is between quadrants 2 and 3 (i.e., assume the center of mass is on the left)
    # trailing = other_asteroid is between quadrants 4 and 1
    side = 'leading' # will redefine as trailing if it is not in fact leading
    if(slope == 0):
        if(x1 > x0):
            side = 'trailing'
    elif(y1 > y0):
        side = 'trailing'
    return side 

def get_distance(y, x):
    return np.sqrt(x**2 + y**2)

def find_best_asteroid(asteroids):
    best = np.zeros(3) # will store the x,y coordinates and the number of asteroids observables from the best asteroid
    for asteroid in asteroids:
        slopes = []
        for other_asteroid in asteroids:
            if(asteroid != other_asteroid):
                slope = get_slope(other_asteroid[1] - asteroid[1], other_asteroid[0] - asteroid[0])
                side = get_side(slope, other_asteroid[0], asteroid[0], other_asteroid[1], asteroid[1])
                slopes.append((slope, side))

        count = len(set(slopes)) # counting unique slopes falls short because asteroids could have the same slope but be on opposite sides of the asteroid in question
       
        if(count > best[2]): # overwriting previous best if a better one is found 
            best[0] = int(asteroid[0])
            best[1] = int(asteroid[1])
            best[2] = int(count)
    return best 

def vaporize(df, vaporized, asteroid, vaporization_count):
    #print('Vaporizing the asteroid at (' + str(asteroid['x']) + ', ' + str(asteroid['y']) + ')')
    df = df.drop(asteroid.index) # removes the asteroid from df
    vaporized = pd.concat([vaporized, asteroid]) # adds the asteroid to the vaporized DataFrame 
    return df, vaporized, vaporization_count + 1

def loop_through_quadrant(q_asteroids, unique_slopes, df, vaporized, vaporization_count):
    for s in unique_slopes:
        asteroids_at_slope = q_asteroids[q_asteroids['slope'] == s]
        closest_at_slope = asteroids_at_slope[asteroids_at_slope['distance'] == asteroids_at_slope['distance'].min()]
        df, vaporized, vaporization_count = vaporize(df, vaporized, closest_at_slope, vaporization_count)
    return df, vaporized, vaporization_count

def vaporize_at_quadrant_border(asteroid_set, side, df, vaporized, vaporization_count):
    asteroid_subset = asteroid_set[asteroid_set['side'] == side]
    closest = asteroid_subset[asteroid_subset['distance'] == asteroid_subset['distance'].min()]
    df, vaporized, vaporization_count = vaporize(df, vaporized, closest, vaporization_count)
    return df, vaporized, vaporization_count

def vaporize_quadrant(asteroid_set, df, vaporized, vaporization_count):
    asteroid_subset = asteroid_set[asteroid_set['slope'] != 0] # this is necessary for only 2 quadrants
    unique_slopes = np.sort(asteroid_set['slope'].unique())
    df, vaporized, vaporization_count = loop_through_quadrant(asteroid_subset, unique_slopes, df, vaporized, vaporization_count)
    return df, vaporized, vaporization_count

def sweep360(best, df, vaporized, vaporization_count):
    verticals = df[df['slope'] == np.inf] 
    horizontals = df[df['slope'] == 0]
    leading_asteroids = df[df['side'] == 'leading']
    trailing_asteroids = df[df['side'] == 'trailing']

    print('12 o\'clock') # start with a slope of inf for leading asteroids
    df, vaporized, vaporization_count = vaporize_at_quadrant_border(verticals, 'leading', df, vaporized, vaporization_count)
    # proceed through quadrant 1 (leading)
    df, vaporized, vaporization_count = vaporize_quadrant(leading_asteroids[leading_asteroids['x'] > best[0]], df, vaporized, vaporization_count)
    print('3 o\'clock') # do slope = 0 for trailing
    df, vaporized, vaporization_count = vaporize_at_quadrant_border(horizontals, 'trailing', df, vaporized, vaporization_count)
    # proceed through quadrant 4 (trailing)
    df, vaporized, vaporization_count = vaporize_quadrant(trailing_asteroids[trailing_asteroids['x'] > best[0]], df, vaporized, vaporization_count)
    print('6 o\'clock') # do slope inf for trailing asteroids
    df, vaporized, vaporization_count = vaporize_at_quadrant_border(verticals, 'trailing', df, vaporized, vaporization_count)
    # proceed through quadrant 3 (trailing)
    df, vaporized, vaporization_count = vaporize_quadrant(trailing_asteroids[trailing_asteroids['x'] < best[0]], df, vaporized, vaporization_count)
    print('9 o\'clock') # do slope = 0 for leading
    df, vaporized, vaporization_count = vaporize_at_quadrant_border(horizontals, 'leading', df, vaporized, vaporization_count)
    # proceed through quadrant 2 (leading)
    df, vaporized, vaporization_count = vaporize_quadrant(leading_asteroids[leading_asteroids['x'] < best[0]], df, vaporized, vaporization_count)
    print('11:59:59.999') # then sweep is finished
    return df, vaporized, vaporization_count

def vaporize_asteroids(best, asteroids):
    # each time an asteroid is vaporized, replace the '#' with a '.' and overwrite field
    # or put them all in a DataFrame and then just drop them from the DataFrame 
    # DataFrame needs x, y, slope, side, distance from best (optional but convenient) 
    df = pd.DataFrame()
    N = len(asteroids)
    x = np.zeros(N)
    y = np.zeros(N)
    slopes = np.zeros(N)
    sides = []
    distances = np.zeros(N)
    for i in range(N):
        x[i] = asteroids[i][0]
        y[i] = asteroids[i][1]
        slopes[i] = get_slope(asteroids[i][1] - best[1], asteroids[i][0] - best[0]) # the best asteroid will show a slope of inf
        sides.append(get_side(slopes[i], asteroids[i][0], best[0], asteroids[i][1], best[1])) # the best asteroid will show a side of leading
        distances[i] = get_distance(asteroids[i][1] - best[1], asteroids[i][0] - best[0])
    df['x'] = x
    df['y'] = y 
    df['slope'] = slopes
    df['side'] = sides 
    df['distance'] = distances 
    #print(df.head())
    df = df[df['distance'] > 0] # removing the best from the df, (the one with a distance of 0) 

    vaporized = pd.DataFrame()
    vaporization_count = 0
    sweep_count = 0
    while(vaporization_count < 200):
        sweep_count += 1
        print('Sweep ' + str(sweep_count))
        df, vaporized, vaporization_count = sweep360(best, df, vaporized, vaporization_count)
        print(str(vaporization_count) + ' asteroids have now been vaporized')
    answer = vaporized.iloc[199]['x'] * 100 + vaporized.iloc[199]['y']
    return answer

for i in range(5,6):
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
        answer = vaporize_asteroids(best, asteroids)
        print('answer: ' + str(int(answer)) + ' (should be 802)')
print('Puzzle:')
field = load_field('input10.txt')
asteroids = identify_asteroids(field)
print(str(len(asteroids)) + ' asteroids identified')
best = find_best_asteroid(asteroids)
print('Best is ' + str(int(best[0])) + ',' + str(int(best[1])) + ' with ' + str(int(best[2])) + ' other asteroids detected')
# Answer was 326 other asteroids detected 
answer = vaporize_asteroids(best, asteroids)
print('answer: ' + str(int(answer)))
# Answer was 1623 