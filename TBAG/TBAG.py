# TBAG/
import time
import pickle
import os
import random
import sys

try:
    import colorama
except ImportError:
    print("Please install colorama")
    print("see README.txt")
    os.system("pause")
    sys.exit()
colorama.init()


class Colours:
    red = colorama.Fore.RED
    cyan = colorama.Fore.CYAN
    blue = colorama.Fore.BLUE
    black = colorama.Fore.BLACK
    green = colorama.Fore.GREEN
    magenta = colorama.Fore.MAGENTA
    white = colorama.Fore.WHITE
    yellow = colorama.Fore.YELLOW


class Game:
    coins = 0
    room_data = []
    alive = True
    player = [0]
    slow_read_time = 0
    file_data = ""

    def __init__(self):
        if "NEW" in os.listdir("games"):
            self.slow_read(f"Thank you for playing!\n"
                           f"The default map is called '{Colours.blue}default{Colours.white}'\n"
                           f"all commands can be listed by typing help when loaded into a game\n"
                           f"{Colours.red}ONLY load games that come from yourself or a trusted source!{Colours.white}\n"
                           f"please run with python.exe, editors like PyCharm can cause bug's\n"
                           f"TBAG is an engine, the '{Colours.blue}default{Colours.white}' map is just to show "
                           f"potential")
            time.sleep(5)
            os.remove("games/NEW")
            os.system("cls")

        self.coins = 0
        self.alive = True
        self.player[0] = 0  # location

        self.set_game()

    def slow_read(self, read, read_time=slow_read_time, nice_end=True):
        skip = 0
        if read == "CONGRATULATIONS YOU WIN":
            self.alive = False
            self.run(True)
        else:
            for ind, i in enumerate(read):
                if skip == 0:
                    if i == "\033" or i == "\x1b":
                        skip = 4
                        if read[ind + 2] == "0":
                            print(f"\033[{read[ind + 2]}{read[ind + 3]}", end="")
                        else:
                            print(f"\033[{read[ind + 2]}{read[ind + 3]}{read[ind + 4]}", end="")
                    else:
                        print(i, end="", flush=True)
                        time.sleep(read_time)
                else:
                    skip -= 1
            if nice_end:
                print(flush=True)

    def wait(self, seconds, msg="please wait", flip_rate=2):
        stuff = "|/—\\"
        self.slow_read(f"{msg} (\\)", self.slow_read_time, False)
        for i in range(seconds * flip_rate):
            print(f"\r{msg} ({stuff[i % 4]})", end="")
            time.sleep(1 / flip_rate)
        print(f"\r{msg}                  ")

    def move(self, position):
        try:
            self.player[0] = position
            self.slow_read(self.room_data[self.player[0]]["desc"])
            self.room_data[self.player[0]]["count"] += 1
            if self.room_data[self.player[0]]["count"] == 1 and self.room_data[self.player[0]]["1st_desc"]:
                self.slow_read(self.room_data[self.player[0]]["1st_desc"])
            if self.room_data[self.player[0]]["condition"][0] == "visits":
                if self.room_data[self.player[0]]["count"] == self.room_data[self.player[0]]["condition"][1]:
                    self.slow_read(self.room_data[self.player[0]]["condition"][2])
                    self.alive = False
            elif self.room_data[self.player[0]]["condition"][0] == "coins":
                if self.coins < self.room_data[self.player[0]]["condition"][1]:
                    self.slow_read(self.room_data[self.player[0]]["condition"][2])
                    self.alive = False
                if self.coins > self.room_data[self.player[0]]["condition"][1]:
                    self.slow_read(self.room_data[self.player[0]]["condition"][3])
            elif self.room_data[self.player[0]]["condition"][0] == "coins_add":
                self.coins += self.room_data[self.player[0]]["condition"][1]
                self.slow_read(self.room_data[self.player[0]]["condition"][2])
                self.room_data[self.player[0]]["condition"] = [""]
            elif self.room_data[self.player[0]]["condition"][0] == "coins_subtract":
                self.coins -= self.room_data[self.player[0]]["condition"][1]
                self.slow_read(self.room_data[self.player[0]]["condition"][2])
                self.room_data[self.player[0]]["condition"] = [""]
        except KeyError:
            print(end="", flush=True)

    def read_input(self):
        self.slow_read("What now?", self.slow_read_time, False)
        player_input = input("")
        player_input = player_input.lower()
        if player_input.lower() in ["n", "s", "e", "w"]:
            if player_input.lower() in self.room_data[self.player[0]].keys():
                return True, player_input
            else:
                return False, "You cannot go that way"
        elif player_input.lower() in ["inv", "help"]:
            return True, player_input
        else:
            return False, "I don't know how to '" + player_input + "'"

    def proses_input(self, command):
        if command.lower() in ["n", "s", "e", "w", "push button", "yes", "no"]:
            self.move(self.room_data[self.player[0]][command])
        elif command.lower() == "inv":
            self.slow_read(f"player inventory;\ncoins : {self.coins}")
        elif command.lower() == "help":
            self.slow_read("Available commands are;")
            for i in ["n", "s", "e", "w", "inv", "help"]:
                self.slow_read(f"> {i}")

    def run(self, override_running=False):
        for i in self.room_data:
            i["count"] = 0
        if not override_running:
            self.move(self.player[0])
            while self.alive:
                command = self.read_input()
                if command[0]:
                    self.proses_input(command[1])
                else:
                    self.slow_read(command[1])
            if self.player[0] == len(self.room_data) - 1:
                return True
        else:
            return True

    def reset(self):
        self.coins = 0
        self.alive = True
        self.player = [0]

    def set_game(self):
        game_file = ""
        while game_file + ".dat" not in os.listdir("games"):
            # self.slow_read("Getting Game files", self.slow_read_time, False)
            self.wait(random.randrange(7, 10), "\033[33mScanning Game files:  \033[0m")
            for i in os.listdir("games"):
                if ".dat" in i:
                    self.slow_read(f">\033[34m {i[:-4]}\033[0m")
            self.slow_read(f"{Colours.yellow}game file? {Colours.white}>{Colours.blue} ", self.slow_read_time, False)
            game_file = input()
            self.wait(random.randrange(7, 10), f"{Colours.yellow}Loading game file ({Colours.blue}"
                                               f"{game_file}{Colours.yellow}):  {Colours.white} ")
            time.sleep(0.5)
            if game_file + ".dat" not in os.listdir("games"):
                self.slow_read(f"Game file '{game_file}' could not be read, please try again")
        with open(f"games/{game_file}.dat", "rb") as file:
            self.room_data = pickle.load(file)
            self.file_data = game_file
        os.system("cls")


if __name__ == "__main__":
    deaths = 0
    game = Game()
    while True:
        game.reset()
        alive_at_end = game.run()
        deaths += 1
        if alive_at_end:
            break
        else:
            game.wait(random.randrange(7, 10), f"{Colours.yellow}Reloading game file:  {Colours.white}")
            with open(f"games/{game.file_data}.dat", "rb") as file:
                game.room_data = pickle.load(file)
            os.system("cls")
    s_deaths = 2 if deaths - 1 >= 2 else deaths - 1
    print(f"you died {deaths - 1} time{f's!s'[s_deaths]}")
    os.system("pause")
