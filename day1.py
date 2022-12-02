import numpy as np 

def calculate_fuel(mass):
    return int(mass / 3) - 2

def calculate_fuel2(mass):
    fuel = int(mass / 3) - 2
    if(fuel < 0):
        fuel = 0
    print(fuel)
    return fuel 

def calculate_fuel_including_fuel(masses):
    tot_fuel = []
    for mass in masses:
        total_fuel = 0
        needs_fuel = True 
        m = mass
        print('mass: ' + str(mass))
        while(needs_fuel):
            fuel = calculate_fuel2(m)
            total_fuel += fuel 
            if(fuel == 0):
                needs_fuel = False
                print('All fueled up!')
                print('Total fuel: ' + str(total_fuel))
                tot_fuel.append(total_fuel)
            m = fuel 
    print(np.sum(tot_fuel))

print('Example: ')
masses = [12, 14, 1969, 100756]

for mass in masses:
    fuel = calculate_fuel(mass)
    print(mass, fuel)

print('Puzzle: ')
data = np.loadtxt('input1.txt')
module_masses = data[:]

total_fuel = 0
for m in module_masses:
    fuel = calculate_fuel(m)
    total_fuel += fuel
print(total_fuel)

print('Example: ')
example_masses = [14, 1969, 100756]
total_fuel = calculate_fuel_including_fuel(example_masses)

print('Puzzle: ')
data = np.loadtxt('input1.txt')
module_masses = data[:]
total_fuel = calculate_fuel_including_fuel(module_masses)