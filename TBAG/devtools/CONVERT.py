import pickle
with open(f"{input('scv name = ')}.csv", "rt") as data:
    data = data.read()
    data = data.replace("`", ",")
    data = data.splitlines()
    final_data = []
    for i_index, line in enumerate(data):
        if not i_index == 0:
            my_list = line.split(",")
            for index, item in enumerate(my_list):
                my_list[index] = item.replace("`", ",")
            print(my_list)
            my_dict = {"desc": my_list[0], "1st_desc": my_list[1], "condition": [my_list[2], int(my_list[3]), my_list[4], my_list[5]],
                       "count": 0}
            #"n": str(my_list[5]), "e": str(my_list[6]), "s": str(my_list[7]), "w": str(my_list[8]),
            if not my_list[6] == "":
                my_dict["n"] = int(my_list[6])
            if not my_list[7] == "":
                my_dict["e"] = int(my_list[7])
            if not my_list[8] == "":
                my_dict["s"] = int(my_list[8])
            if not my_list[9] == "":
                my_dict["w"] = int(my_list[9])
            final_data.append(my_dict)
with open(f"games/{input('game name = ')}.dat", "wb") as file:
    pickle.dump(final_data, file)