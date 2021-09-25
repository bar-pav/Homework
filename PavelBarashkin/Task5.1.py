# ### Task 4.1
# Open file `data/unsorted_names.txt` in data folder. Sort the names and write them to a new file called
# `sorted_names.txt`. Each name should start with a new line as in the following example:

# ```
# Adele
# Adrienne
# ...
# Willodean
# Xavier
# ```


unsorted_file = open('../data/unsorted_names.txt', 'r')
sorted_file = open('../data/sorted_names.txt', 'w')
sorted_file.writelines(sorted(unsorted_file.readlines()))
unsorted_file.close()
sorted_file.close()
