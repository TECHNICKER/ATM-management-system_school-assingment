from os import system, stat
from time import sleep
import pickle

ATMs = []
name_scale = 0
path_scale = 0
cash_scale = 0
refresh = 0

class Cash_machine:

    def __init__(self, name: str, vault_path: str):

        self.path_validity = True
        self.name = name
        self.vault_path = vault_path
        self.total_cash_avilable = 0
        self.cash_dict = {}
        self.withdraw_dict = {}

    def load_vault(self):
        occurences = 0
        try:
            with open(self.vault_path, "r") as vault:
                while line := vault.readline():
                    self.cash_dict.update([line.split()])

            for key in self.cash_dict.keys():
                self.cash_dict[key] = int(self.cash_dict[key])

            self.withdraw_dict = dict.fromkeys(self.cash_dict.keys(), 0)

            for atm in ATMs:
                if atm.vault_path == self.vault_path:
                    occurences += 1
                
            if occurences > 1 and self.vault_path != "placeholder.txt":
                self.path_validity = False
                self.total_cash_avilable = 0

            else:
                self.path_validity = True
                self.total_cash_avilable = sum([int(bill)*self.cash_dict[bill] for bill in self.cash_dict.keys()])
            
        except:
            self.path_validity = False

    def withdraw(self, ammount: int):
        sub_ammount = ammount

        if self.path_validity == True:

            if ammount <= self.total_cash_avilable:
                while sub_ammount > 0:
                    for key in self.withdraw_dict.keys():

                        times = sub_ammount // int(key)

                        if times > self.cash_dict[key]:
                            self.withdraw_dict[key] = self.cash_dict[key]
                            sub_ammount -= (self.cash_dict[key] * int(key))
                        else:
                            self.withdraw_dict[key] = times
                            sub_ammount -= (times * int(key))

                if sum([int(bill)*self.withdraw_dict[bill] for bill in self.withdraw_dict.keys()]) == ammount:

                    with open(self.vault_path, "w") as vault:
                        for key in self.cash_dict.keys():
                            vault.write(f"{key} {self.cash_dict[key] - self.withdraw_dict[key]}\n")

                else:
                    print("\nATM doesn't have enough bill variety\n")

            else:
                print("\nentered ammount not avilable.\n")

        else:
            print("\nthis ATM has an invalid vault path.\n")

print("Welcome to your ATM management system\n")

if stat("database.db").st_size > 0: 
    with open("database.db", "rb") as database:
        ATMs = pickle.load(database)

while True:

    system("clear")

    if len(ATMs) == 0:
        print("No ATMs avilable. To create an ATM use the create (c) command in format: 'assigned number (0 adds as last)' 'c' 'ATM name:ATMvaultpath.xyz'\n")
    
    for atm in ATMs:
            if len(atm.name) > name_scale:
                name_scale = len(atm.name)

            if len(atm.vault_path) > path_scale:
                path_scale = len(atm.vault_path)

            if len(str(atm.total_cash_avilable)) > cash_scale:
                cash_scale = len(str(atm.total_cash_avilable))

    for atm in ATMs:
        atm.load_vault()

        print(f"| {ATMs.index(atm) + 1:{len(str(len(ATMs)))}} | {atm.name:{name_scale}} | {atm.vault_path:{path_scale}} | {atm.total_cash_avilable:{cash_scale}} |")
        if atm.path_validity == False:
            print("   Δ This ATMs path doesn't point to a valid vault file or it shares a path with another ATM.")
    
        if refresh > 0:
            refresh -= 1
            continue
    
    if len(ATMs) > 0:
        print("\nInput command in the specified format:\n'ATM number' 'desired action' 'action value' or 'ATM name':'ATM path'\nwhere the desired action can be:\n c - ATM creation\n n - ATM name change\n w - withdrawal from specified ATM\n p - ATM vult path change\n r - ATM removal\n\nrl - reload, refresh list\n q - save and exit, quit.\n")
    
    command = input().split()

    print()

    try:
            
        if command[0] == "q":
            raise SystemExit

        elif command[0] == "rl":
            refresh = len(ATMs)
            continue    

        name = command[2]

        for i in range(3, len(command)):
            name += " " + command[i]

        if command[1] == "c":

            if int(command[0]) == 0:
                ATMs.append(Cash_machine(name.split(":")[0], name.split(":")[1]))

            elif int(command[0]) == len(ATMs) + 1:
                ATMs.append(Cash_machine(name.split(":")[0], name.split(":")[1]))

            elif int(command[0]) <= len(ATMs):
                if ATMs[int(command[0]) - 1].name == "placeholder" and ATMs[int(command[0]) - 1].vault_path == "placeholder.txt":
                    ATMs.remove(ATMs[int(command[0]) - 1])
                    ATMs.insert(int(command[0]) - 1, Cash_machine(name.split(":")[0], name.split(":")[1]))
                else:
                    ATMs.insert(int(command[0]) - 1, Cash_machine(name.split(":")[0], name.split(":")[1]))

            else:
                for spacer in range(int(command[0]) - len(ATMs) - 1):
                    ATMs.insert(len(ATMs) + spacer, Cash_machine("placeholder", "placeholder.txt"))

                ATMs.insert(int(command[0]) - 1, Cash_machine(name.split(":")[0], name.split(":")[1]))

        elif int(command[0]) != 0 and int(command[0]) <= len(ATMs):

            if   command[1] == "w":
                ATMs[int(command[0]) - 1].withdraw(int(name.replace(" ", "")))

            elif command[1] == "p":
                ATMs[int(command[0]) - 1].vault_path = name

            elif command[1] == "n":
                ATMs[int(command[0]) - 1].name = name

            elif command[1] == "r":
                if ATMs[int(command[0]) - 1].name == "placeholder" and ATMs[int(command[0]) - 1].vault_path == "placeholder.txt":
                    ATMs.remove(ATMs[int(command[0]) - 1])

                else:
                    ATMs.remove(ATMs[int(command[0]) - 1])
                    ATMs.insert(int(command[0]) - 1, Cash_machine("placeholder", "placeholder.txt"))

        else:
            print("invalid ATM number or command specifier\n")
            sleep(2)

    except SystemExit:
        with open("database.db", "wb") as database:
            pickle.dump(ATMs, database)

        raise SystemExit

    except:
        print("invalid command format\n")
        sleep(2)
