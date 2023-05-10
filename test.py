my_list = [1, 2, 3, 4, 5]

# Iterate over the list in reverse order
for i in range(len(my_list)-1, -1, -1):
    if my_list[i] == 3:  # Condition to meet for removal
        my_list.pop(i)

print(my_list)  # Output: [1, 2, 4, 5]
