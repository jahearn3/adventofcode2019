# Secure Container

input_start = 264360
input_stop  = 746325

possible_password_count = 0

for i in range(input_start, input_stop + 1):
    j = str(i)
    if((j[0] == j[1]) or (j[1] == j[2]) or (j[2] == j[3]) or (j[3] == j[4]) or (j[4] == j[5])): # 2 adjacent digit criterion
        if((int(j[0]) <= int(j[1])) and (int(j[1]) <= int(j[2])) and (int(j[2]) <= int(j[3])) and (int(j[3]) <= int(j[4])) and (int(j[4]) <= int(j[5]))): # monotonic increase criterion
            #possible_password_count += 1 # uncomment for part 1 count
            repeats = 0
            repeated_numbers = []
            for k in range(1, len(j)):
                if(j[k-1] == j[k]):
                    repeats += 1
                    repeated_numbers.append(j[k])
            if(repeats == 1):
                possible_password_count += 1
            elif(repeats == 2):
                if(repeated_numbers[0] != repeated_numbers[1]):
                    possible_password_count += 1
            elif(repeats == 3): 
                if((repeated_numbers[0] != repeated_numbers[1]) or (repeated_numbers[1] != repeated_numbers[2])):
                    possible_password_count += 1
            elif(repeats == 4): 
                if((repeated_numbers[0] != repeated_numbers[1]) or (repeated_numbers[1] != repeated_numbers[2]) or (repeated_numbers[2] != repeated_numbers[3])):
                    if((repeated_numbers[0] == repeated_numbers[1]) and (repeated_numbers[1] != repeated_numbers[2]) and (repeated_numbers[2] == repeated_numbers[3])):
                        pass
                    else:
                        possible_password_count += 1
print(possible_password_count)

# 945 for part 1

# part 2
# 365 is too low
# 419 is too low
# 617 is correct 
# 635 is too high