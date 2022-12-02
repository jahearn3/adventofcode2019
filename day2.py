from audioop import add
from cProfile import run
import numpy as np 

def load_intcode():
    with open('input2.txt') as f:
        line = f.readlines()
    data = line[0].split(',')
    intcode = []
    for element in data:
        intcode.append(int(element))
    return intcode 

def run_code(intcode, noun, verb): 
    intcode[1] = noun
    intcode[2] = verb
    for i in range(0, len(intcode), 4):
        #print('i = ' + str(i))
        opcode = intcode[i]
        #print('opcode = ' + str(opcode))

        if(opcode == 1):
            #add
            #print('Adding')
            idx1 = intcode[i+1]
            idx2 = intcode[i+2]
            idx3 = intcode[i+3]
            intcode[idx3] = intcode[idx1] + intcode[idx2]
        elif(opcode == 2):
            # multiply
            #print('Multiplying')
            idx1 = intcode[i+1]
            idx2 = intcode[i+2]
            idx3 = intcode[i+3]
            intcode[idx3] = intcode[idx1] * intcode[idx2]
        elif(opcode == 99):
            #print("Program halted by opcode 99")
            break
        else:
            print("Something went wrong!")
            break 
    return intcode

def find_noun_and_verb(desired_output, i_range=99, j_range=99, answer=0):
    for i in range(i_range):
        for j in range(j_range):
            intcode = load_intcode()
            noun = i
            verb = j 
            intcode = run_code(intcode, noun, verb)
            if(intcode[0] == desired_output):
                answer = 100 * noun + verb 
                print('Answer found: ' + str(answer))
    return answer

print('Part 1')
intcode = load_intcode()
noun = 12
verb = 2
intcode = run_code(intcode, noun, verb)
print(intcode[0])

print('Part 2')
desired_output = 19690720
answer = find_noun_and_verb(desired_output)