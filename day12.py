# The N-Body Problem
import numpy as np 

def load_data(filename):
    lines = []
    with open(filename) as f:
        for line in f.readlines():
            lines.append(line.strip('<>\n'))
    return lines

def initialize_positions(lines):
    x = []
    y = []
    z = []
    for line in lines:
        split_line = line.split(',')
        x.append(int(split_line[0][2:]))
        y.append(int(split_line[1][3:]))
        z.append(int(split_line[2][3:]))
    return (x, y, z)

def initialize_arrays(initial_positions, timesteps):
    # N timesteps, 3 coordinates, 4 moons
    positions  = np.zeros((timesteps, 3, 4)) 
    velocities = np.zeros((timesteps, 3, 4)) 
    positions[0] = initial_positions
    return positions, velocities 

def apply_gravity(positions_t, velocities_prev):
    # updates the velocity
    velocities_t = np.zeros((3, 4))
    for m in range(4):
        for k in range(3):
            velocities_t[k][m] = velocities_prev[k][m]
        for j in range(4):
            if(m != j):
                for i in range(3):
                    if(  positions_t[i][m] < positions_t[i][j]):
                        velocities_t[i][m] += 1 
                    elif(positions_t[i][m] > positions_t[i][j]):
                        velocities_t[i][m] -= 1
    return velocities_t

def apply_velocity(positions_prev, velocities_t):
    # updates the position
    positions_t = np.zeros((3, 4))
    for m in range(4):
        for i in range(3):
            positions_t[i][m] = positions_prev[i][m] + velocities_t[i][m]
    return positions_t

def print_status(pos, vel, t):
    print(f'After {t} timesteps: ')
    for i in range(4):
        print(f'pos=<x={int(pos[0][i])}, y={int(pos[1][i])}, z={int(pos[2][i])}>, vel=<x={int(vel[0][i])}, y={int(vel[1][i])}, z={int(vel[2][i])}>')

def simulate(positions, velocities, timesteps):
    total_energy = 0
    print_status(positions[0], velocities[0], 0)
    for t in range(1, timesteps):
        velocities[t] = apply_gravity(positions[t-1], velocities[t-1])
        positions[t] = apply_velocity(positions[t-1], velocities[t])
        if(t % int(timesteps / 10) == 0):
            print_status(positions[t], velocities[t], t)
    # calculate energy only at the end    
    for m in range(4):
        pot = abs( positions[-1][0][m]) + abs( positions[-1][1][m]) + abs( positions[-1][2][m]) 
        kin = abs(velocities[-1][0][m]) + abs(velocities[-1][1][m]) + abs(velocities[-1][2][m]) 
        energy = pot * kin
        total_energy += energy
    return int(total_energy) 

# timesteps = 10 + 1
# print('Example 1: ')
# lines = load_data('day12example1.txt')
# initial_positions = initialize_positions(lines)
# positions, velocities = initialize_arrays(initial_positions, timesteps)
# print(positions[0])
# answer = simulate(positions, velocities, timesteps)
# print(f'Sum of total energy: {answer} (should be 179)')

# timesteps = 100 + 1
# print('Example 2: ')
# lines = load_data('day12example2.txt')
# initial_positions = initialize_positions(lines)
# positions, velocities = initialize_arrays(initial_positions, timesteps)
# answer = simulate(positions, velocities, timesteps)
# print(f'Sum of total energy: {answer} (should be 1940)')

# timesteps = 1000 + 1
print('Puzzle: ')
lines = load_data('input12.txt')
initial_positions = initialize_positions(lines)
# positions, velocities = initialize_arrays(initial_positions, timesteps)
# answer = simulate(positions, velocities, timesteps)
# print(f'Sum of total energy: {answer}')
# answer was 10664

# Part 2...
# x, y, z are completely independent, so we can simulate them one at a time 
# x repeats with a certain frequency
# y repeats with a different frequency
# z repeats with a different frequency 
# find the least common multiple

def apply_grav(positions_t, velocities_prev):
    # updates the velocity
    velocities_t = np.zeros(4)
    for m in range(4):
        velocities_t[m] = velocities_prev[m]
        for j in range(4):
            if(m != j):
                if(  positions_t[m] < positions_t[j]):
                    velocities_t[m] += 1 
                elif(positions_t[m] > positions_t[j]):
                    velocities_t[m] -= 1
    return velocities_t

def apply_velo(positions_prev, velocities_t):
    # updates the position
    positions_t = np.zeros(4)
    for m in range(4):
        positions_t[m] = positions_prev[m] + velocities_t[m]
    return positions_t

reps = np.zeros(3)
for i in range(3): # loop through x, y, and z directions
    # initialize parameters
    repeated = False
    pos = [initial_positions[i]]
    vel = [[0, 0, 0, 0]] 
    # first timestep outside the while loop to avoid comparing an empty set
    vel.append(apply_grav(pos[0], vel[0]))
    pos.append(apply_velo(pos[0], vel[1]))
    t = 1 # counting the number of timesteps
    log_idx = 10
    while(repeated == False):
        # advance to next timestep
        t += 1
        # calculate and record new position and velocity
        new_vel = apply_grav(pos[t-1], vel[t-1])
        vel.append(new_vel)
        new_pos = apply_velo(pos[t-1], vel[t])
        pos.append(new_pos)
        
        # compare new position and velocity to previous timesteps
        for k in range(t):
            if((new_pos == pos[k]).all() and (new_vel == vel[k]).all()):
                repeated = True
                print(f'{i}: repeated state after {t} steps!')
                reps[i] = t
            elif(t == log_idx):
                print(f'still searching after {t} steps...')
                log_idx *= 10 

# 186028, 56344, 231614 

def lcm(lst): # https://theprogrammingexpert.com/python-least-common-multiple/
    lcm_temp = max(lst)
    while(True):
        if all(lcm_temp % x == 0 for x in lst):
            break
        lcm_temp = lcm_temp + 1
    return lcm_temp

result_lcm = lcm([186028, 56344, 231614])
# 303459551979256 given by Wolfram Alpha

#result_lcm = np.lcm.reduce(reps) # numpy.core._exceptions.UFuncTypeError: ufunc 'lcm' did not contain a loop with signature matching types (None, <class 'numpy.dtype[float64]'>) -> None
print(f'Steps to reach a state that matches a previous state: {result_lcm}')