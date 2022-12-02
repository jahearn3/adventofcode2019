import numpy as np 
import time 
# Manhattan distance from the central port to the closest intersection

def load_wires():
    with open('input3.txt') as f:
        line = f.readlines()
    wire1 = line[0].split(',')
    wire2 = line[1].split(',')
    return wire1, wire2 

def find_distance_to_closest_intersection(wire1, wire2):
    # set up flux coordinate arrays
    flux1x = []
    flux1y = []
    flux2x = []
    flux2y = []

    origin_x = 0
    origin_y = 0

    wires  = [wire1, wire2]
    fluxes_x = [flux1x, flux2x]
    fluxes_y = [flux1y, flux2y]
    # lay out wires
    for i in range(len(wires)):
        wire = wires[i]
        flux_x = fluxes_x[i]
        flux_y = fluxes_y[i]
        # starting point
        current_x = origin_x 
        current_y = origin_y
        for instruction in wire:
            direction = instruction[0]
            magnitude = int(instruction[1:])
            for i in range(magnitude):
                if(direction == 'R'):   # go to the right
                    current_x += 1
                elif(direction == 'L'): # go to the left
                    current_x -= 1
                elif(direction == 'U'): # go up
                    current_y += 1
                elif(direction == 'D'): # go down
                    current_y -= 1
                else:
                    print('Unknown direction: ' + direction)
                    break
                #flux[current_x][current_y] = 1
                flux_x.append(current_x)
                flux_y.append(current_y)
            #print('Current location: (' + str(current_x) + ', ' + str(current_y) + ')')
 
     # set up arrays for manhattan distance and step count at intersections
    intersections = []
    steps = [] 
    for i in range(len(flux1x)):
        for j in range(len(flux2x)):
            if((flux1x[i] == flux2x[j]) and (flux1y[i] == flux2y[j])):
                # add up coordinates of intersections
                manhattan_distance = np.absolute(flux1x[i]) + np.absolute(flux1y[i])
                if(manhattan_distance != 0):
                    intersections.append(manhattan_distance) 
                    print('Intersection: ' + str(manhattan_distance))
                    steps.append(i+j+2) # indices count how many steps, add 1+1=2 for step from origin
                    print('Steps to intersection: ' + str(i+j+2))
                
    # return the minimum of the Manhattan distances of intersections as the answer
    answer = np.amin(intersections)
    steps_min = np.amin(steps)
    return answer, steps_min 


print('Example 1:')
wire1 = ['R75','D30','R83','U83','L12','D49','R71','U7','L72']
wire2 = ['U62','R66','U55','R34','D71','R55','D58','R83']
answer, steps_min = find_distance_to_closest_intersection(wire1, wire2)
print('Manhattan distance: ' + str(answer) + ' (should be 159)')
print('Minimum steps to intersection: ' + str(steps_min) + ' (should be 610)')

print('Example 2:')
wire1 = ['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51']
wire2 = ['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7']
answer, steps_min = find_distance_to_closest_intersection(wire1, wire2)
print('Manhattan distance: ' + str(answer) + ' (should be 135)')
print('Minimum steps to intersection: ' + str(steps_min) + ' (should be 410)')


print('Puzzle: ')
start = time.time()
wire1, wire2 = load_wires()
answer, steps_min = find_distance_to_closest_intersection(wire1, wire2)
print('Manhattan distance: ' + str(answer))
print('Minimum steps to intersection: ' + str(steps_min))
stop = time.time()
print('It took ' + str((stop-start)/60) + ' minutes to execute the puzzle code.') # last time it took 23.55 minutes 

