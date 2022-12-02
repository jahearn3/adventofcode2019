# Amplication Circuit

def load_intcode():
    with open('input7.txt') as f:
        line = f.readlines()
    data = line[0].split(',')
    intcode = []
    for element in data:
        intcode.append(int(element))
    return intcode 



intcode = load_intcode()