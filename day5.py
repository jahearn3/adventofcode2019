import numpy as np 

# Sunny with a Chance of Asteroids

def load_intcode():
    with open('input5.txt') as f:
        line = f.readlines()
    data = line[0].split(',')
    intcode = []
    for element in data:
        intcode.append(int(element))
    return intcode 

def get_value(mode, intcode, i, j):
    if(mode == 0): # position mode
        value = intcode[intcode[i+j+1]]
    elif(mode == 1): # immediate mode
        value = intcode[i+j+1]
    else:
        print('Mode not supported. ')
        value = 0
    return value

def run_code(intcode, input):
    keep_going = True 
    i = 0
    while(keep_going):
        #print(i)
        opcodestring = str(int(intcode[i]))
        parameter_modes = np.zeros(3)
        while(len(opcodestring) < 5):
            opcodestring = '0' + opcodestring 
        #print(opcodestring)
        opcode = int(opcodestring[3:])
        parameter_modes[0] = int(opcodestring[2])
        parameter_modes[1] = int(opcodestring[1])
        parameter_modes[2] = int(opcodestring[0])
        if(opcode == 99):
            print("Program halted by opcode 99")
            keep_going = False
            break
        elif((opcode == 1) or (opcode == 2)):
            num = np.zeros(3)
            for j in range(3):
                num[j] = get_value(parameter_modes[j], intcode, i, j)
            if(opcode == 1):
                num[2] = num[0] + num[1]
            elif(opcode == 2):
                num[2] = num[0] * num[1]
            if(parameter_modes[2] == 0): # position mode
                intcode[intcode[i+3]] = num[2]
            i += 4
        elif((opcode == 3) or (opcode == 4)):  
            if(opcode == 3):
                for j in range(3):
                    if(parameter_modes[j] == 0): # position mode
                        intcode[intcode[i+1]] = input 
                    if(parameter_modes[j] == 1): # immediate mode
                        intcode[i+1] = input
            elif(opcode == 4):
                for j in range(3):
                    if(parameter_modes[j] == 0): # position mode
                        print('output: ' + str(int(intcode[intcode[i+1]])))
                    if(parameter_modes[j] == 1): # immediate mode
                        print('output: ' + str(int(intcode[i+1])))
            i += 2
        elif(5 <= opcode <= 8):
            num = np.zeros(2)
            for j in range(2):
                if(parameter_modes[j] == 0): # position mode
                    num[j] = intcode[intcode[i+j+1]]
                elif(parameter_modes[j] == 1): # immediate mode
                    num[j] = intcode[i+j+1]
            if(opcode == 5):
                if(num[0] != 0):
                    i = num[1]
                    
                print('opcode 5')
                keep_going = False
                #if(intcode[i+1] != 0):
                    #i = intcode[i+2]
            elif(opcode == 6):
                #if(intcode[i+1] == 0):
                    #i = intcode[i+2]
                if(num[0] == 0):
                    i = num[1]
                print('opcode 6')
                keep_going = False
                    
            elif(opcode == 7):
                #if(intcode[i+1] < intcode[i+2]):
                    #intcode[intcode[i+3]] = 1
                if(num[0] < num[1]):
                    intcode[intcode[i+3]] = 1
                else:
                    intcode[intcode[i+3]] = 0
                i += 4
            elif(opcode == 8):
                #if(intcode[i+1] == intcode[i+2]):
                if(num[0] == num[1]):
                    intcode[intcode[i+3]] = 1
                else:
                    intcode[intcode[i+3]] = 0
                i += 4
        
        else:
            print("Something went wrong!")
            keep_going = False 
            break 



print('Part 1')
intcode = load_intcode()
input = int(1)
run_code(intcode, input)
# Part 1 answer was 12428642 

print('Part 2')
input = int(5)
run_code(intcode, input)