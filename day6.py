#import numpy as np 

# Universal Orbit Map

def load_data():
    lines = []
    with open('input6.txt') as f:
        for line in f.readlines():
            lines.append(line.strip('\n'))
    return lines

def add_element(dict, key, value):
    if key not in dict:
        dict[key] = []
    dict[key].append(value)
    #return dict 

def build_orbit_tree(orbit_list): 
    orbit_tree = {}
    for line in orbit_list:
        data = line.split(')')
        parent = data[0]
        child  = data[1]
        add_element(orbit_tree, parent, child)
    return orbit_tree # dictionary tree-like structure 

def find_parent(k, orbit_tree, dist_to_root):
    #print('k: ' + k)
    for key, value in orbit_tree.items():
        #print('key: ' + key)
        #print('value: ' + value)
        for v in value:
            #print('v: ' + v)
            if(v == k):
                print(v + ' orbits ' + key)
                if(key == 'COM'):
                    return dist_to_root + 1
                else:
                    return find_parent(key, orbit_tree, dist_to_root + 1)
    #print('dist_to_root from ' + k + ': ' + str(dist_to_root))
    return dist_to_root 

def get_dist_to_root(k, orbit_tree):
    dist_to_root = 0 
    # count the number of levels to get to the root 
    # recursively get the parent of k 
    dist_to_root = find_parent(k, orbit_tree, dist_to_root)
    return dist_to_root  

def count_orbits(orbit_tree):
    n_orbits = 0
    for k,v in orbit_tree.items():
        n_orbits += len(v) # direct orbits
        n_orbits += (len(v) * get_dist_to_root(k, orbit_tree)) # indirect orbits
    return n_orbits
#orbit_count_checksums # total number of direct orbits and indirect orbits

def calculate_orbits(orbit_list):
    orbit_tree = build_orbit_tree(orbit_list)
    #print(orbit_tree)
    n = count_orbits(orbit_tree)
    return n 
    
print('Example: ')
orbit_list = ['COM)B','B)C','C)D','D)E','E)F','B)G','G)H','D)I','E)J','J)K','K)L']
n = calculate_orbits(orbit_list)
print(str(n) + ' orbits (should be 42)')

print('Puzzle: ')
orbit_list = load_data()
n = calculate_orbits(orbit_list)
print(str(n) + ' orbits')
# 154386 was the correct answer

# Part 2: Orbital Transfers between YOU and SAN (Santa) 

def list_to_root(k, v, orbit_tree):
    lst = [v, k] 
    keep_going = True
    while(keep_going):
        for key, value in orbit_tree.items():
            for val in value:
                if(val == k):
                    lst.append(key)
                    k = key 
                    if(k == 'COM'):
                        keep_going = False
                        break 
    return lst 

def count_transfers(orbit_tree, start='YOU', end='SAN'):
    k_transfers = 0
    list_from_start_to_root = []
    list_from_end_to_root = []
    for k,v in orbit_tree.items():
        for val in v:
            if(val == start):
                list_from_start_to_root = list_to_root(k, val, orbit_tree)
            if(val == end):
                list_from_end_to_root = list_to_root(k, val, orbit_tree)
    # find common orbited body closest to YOU/SAN (minimum, or for loop)
    for i in range(len(list_from_start_to_root)):
        for j in range(len(list_from_end_to_root)):
            if(list_from_start_to_root[i] == list_from_end_to_root[j]):
                # add difference of indices in lists
                k_transfers = i + j - 2
                return k_transfers
    print(list_from_start_to_root)
    print(list_from_end_to_root)
    return k_transfers 

def orbital_transfers(orbit_list):
    orbit_tree = build_orbit_tree(orbit_list)
    k = count_transfers(orbit_tree)
    return k 

print('Example: ')
orbit_list = ['COM)B','B)C','C)D','D)E','E)F','B)G','G)H','D)I','E)J','J)K','K)L','K)YOU','I)SAN']
k = orbital_transfers(orbit_list)
print(str(k) + ' transfers (should be 4)')

print('Puzzle: ')
orbit_list = load_data()
k = orbital_transfers(orbit_list)
print(str(k) + ' transfers')
# 346 was the correct answer




