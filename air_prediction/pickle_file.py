import pickle

# take user input to take the amount of data

data = [2,3]

# take input of the data


# open a file, where you ant to store the data
file = open('model.pkl', 'wb')

# dump information to that file
pickle.dump(data, file)

# close the file
file.close()