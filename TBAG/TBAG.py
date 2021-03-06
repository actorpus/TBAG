# TBAG/
import time
import pickle
import os
import random
import sys
import logging

try:
    import colorama
except ImportError:
    print("Please install colorama")
    print("see README.txt")
    os.system("pause")
    sys.exit()
colorama.init()

LOGGING_FORMAT = "%(levelname)s %(asctime)s %(funcName)s :: %(message)s"
logging.basicConfig(format=LOGGING_FORMAT, level=logging.DEBUG, filename="game_log.log")
logger = logging.getLogger("game_logger")

logger.info("\n---=== GAME START ===---")


class Colours:
    red = colorama.Fore.RED
    cyan = colorama.Fore.CYAN
    blue = colorama.Fore.BLUE
    black = colorama.Fore.BLACK
    green = colorama.Fore.GREEN
    magenta = colorama.Fore.MAGENTA
    white = colorama.Fore.WHITE
    yellow = colorama.Fore.YELLOW


print(Colours.white, end="")


def clear(pause=False):
    if not pause:
        if os.name == 'nt':
            _ = os.system('cls')

            # for mac and linux(here, os.name is 'posix')
        else:
            _ = os.system('clear')
    else:
        if os.name == 'nt':
            _ = os.system('pause')

        # there is no linux pause command uses input instead
        else:
            _ = input("Press enter key to continue . . .")

class Game:
    coins = 0
    room_data = []
    alive = True
    player = [0]
    slow_read_time = 0.06
    file_data = ""

    def __init__(self):
        logger.info("GAME object setup")
        if open("new").read() == "":
            logger.info("presenting 1st time info")
            self.slow_read(open("new data").read())
            time.sleep(5)
            with open("new", "w") as new_file:
                new_file.write("NO")
            clear()

        self.coins = 0
        self.alive = True
        self.player[0] = 0  # location

        self.set_game()

    def god_mode(self):
        logger.debug("GOD MODE enabled")
        self.coins = 1000
        self.slow_read_time = 0
        print(self.slow_read_time)

    def slow_read(self, read, read_time=slow_read_time, nice_end=True):
        logger.debug("slow read triggered with data {%s..., %s, %s}" % (read[:20], read_time, nice_end))
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
                    elif i == "\\" and read[ind+1] != "¬":
                        skip = 1
                        print("\n", end="")
                    elif read[ind:ind+9] == "{Colours.":
                        skip = 14
                        color = read[ind+9:ind+14]
                        print(eval(f"Colours.{color}"), end="")
                    else:
                        print(i, end="", flush=True)
                        time.sleep(read_time)
                else:
                    skip -= 1
            if nice_end:
                print(flush=True)

    def wait(self, seconds, msg="please wait", flip_rate=2):
        logger.debug("wait triggered with data {%s, %s, %s}" %(seconds, msg, flip_rate))
        stuff = "|/—\\"
        self.slow_read(f"{msg} (\\¬)", self.slow_read_time, False)
        for i in range(seconds * flip_rate):
            print(f"\r{msg} ({stuff[i % 4]})", end="")
            time.sleep(1 / flip_rate)
        print(f"\r{msg}{' '*50}")

    def move(self, position):
        logger.debug("move triggered with data {%s}" % position)
        try:
            logger.debug("player position updated from %s to %s" % (self.player[0], position))
            self.player[0] = position
            self.slow_read(self.room_data[self.player[0]]["desc"], self.slow_read_time)
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
        logger.debug("read input triggered")
        self.slow_read("What now?", self.slow_read_time, False)
        player_input = input("")
        logger.debug("player input recorded data of {%s}" % player_input)
        player_input = player_input.lower()
        logger.debug("player inputted data{%s}" % player_input)
        if player_input.lower() in ["n", "s", "e", "w"]:
            if player_input.lower() in self.room_data[self.player[0]].keys():
                return True, player_input
            else:
                return False, "You cannot go that way"
        elif player_input.lower() in ["inv", "help"]:
            return True, player_input
        elif player_input.lower() == "wwssadadqeqe":
            self.god_mode()
            return True, "GOD MODE ENABLED"
        else:
            return False, "I don't know how to '" + player_input + "'"

    def proses_input(self, command):
        logger.debug("proses_input triggered with data {%s}" % command)
        if command.lower() in ["n", "s", "e", "w", "push button", "yes", "no"]:
            self.move(self.room_data[self.player[0]][command])
        elif command.lower() == "inv":
            self.slow_read(f"player inventory;\ncoins : {self.coins}")
        elif command.lower() == "help":
            self.slow_read("Available commands are;")
            for i in ["n", "s", "e", "w", "inv", "help"]:
                self.slow_read(f"> {i}")

    def run(self, override_running=False):
        logger.debug("run triggered with data {%s}" % override_running)
        for i in self.room_data:
            i["count"] = 0
        if not override_running:
            self.move(self.player[0])
            while self.alive:
                logger.debug("game loop tick")
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
        logger.debug("reset triggered")
        self.coins = 0
        self.alive = True
        self.player = [0]

    def set_game(self):
        logger.debug("set game triggered")
        game_file = ""
        while game_file + ".dat" not in os.listdir("games"):
            # self.slow_read("Getting Game files", self.slow_read_time, False)
            self.wait(random.randrange(7, 10), "\033[33mScanning Game files:  \033[0m")
            for i in os.listdir("games"):
                if ".dat" in i:
                    self.slow_read(f">\033[34m {i[:-4]}\033[0m")
            self.slow_read(f"{Colours.yellow}game file? {Colours.white}>{Colours.blue} ", self.slow_read_time, False)
            game_file = input()
            logger.debug("set_game recorded input {%s}" % game_file)
            self.wait(random.randrange(7, 10), f"{Colours.yellow}Loading game file ({Colours.blue}"
                                               f"{game_file}{Colours.yellow}):  {Colours.white} ")
            time.sleep(0.5)
            if game_file + ".dat" not in os.listdir("games"):
                logger.debug("set_game invalid response")
                self.slow_read(f"Game file '{game_file}' could not be read, please try again")
        with open(f"games/{game_file}.dat", "rb") as File:
            logger.debug("set_game loading file {'games/%s.dat'}" % game_file)
            self.room_data = pickle.load(File)
            self.file_data = game_file
        clear()


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
            clear()
    s_deaths = 2 if deaths - 1 >= 2 else deaths - 1
    print(f"you died {deaths - 1} time{f's!s'[s_deaths]}")
    clear(True)
else:
    print("thanks for using the TBAG engine!")
