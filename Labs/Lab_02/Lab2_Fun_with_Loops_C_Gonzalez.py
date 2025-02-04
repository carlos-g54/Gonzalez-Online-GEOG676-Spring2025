

# Define the list of numbers
part1 = [1,2,4,8,16,32,64,128,256,512,1024,2048,4096]

# Initialize the result to 1 
result = 1

# Iterate through each number in the list
for number in part1:
    result *= number  # Multiply the result by the current number

# Print the final result
print("The product of all numbers in the list is:", result)


part2 = [-1, 23, 483, 8573, -13847, -381569, 1652337, 718522177]

# Because this is addition/subtraction, the initial value is 0
result2 = 0

for i in part2:
    result2 += i

print("The addition of all items in part2 is:", result2)

part3 = [146, 875, 911, 83, 81, 439, 44, 5, 46, 76, 61, 68, 1, 14, 38, 26, 21] 

result3 = 0

# the % operator calculates the remainder of a division
for i in part3:
    if i % 2 == 0:
        result3 += i

print("the answer to part 3 is", result3)