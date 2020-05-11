import pickle

with open(input("dat data > "), "rb") as file:
    data = pickle.load(file)

print(data)