import random
import time
import os.path
from os import path
from os import system, name
import math
import getpass
import re
import binascii
from cryptography.fernet import Fernet

class PasswordGenerator:
    def __init__(self):
        self.lower_case_letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                                  'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                                  'u', 'v', 'w', 'x', 'y', 'z')

        self.upper_case_letters = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K',
                                 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                                 'V', 'W', 'X', 'Y', 'Z')

        self.numbers = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')

        self.symbols = ('~', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')','-', '_', '=',
                        '+', '[', ']', '{', '}', '|', ';', ':', "'", '"', ',', '<', '>', '/', '?')

        self.characters = (self.lower_case_letters, self.upper_case_letters,
                           self.numbers, self.symbols)

        self.password = []
        """Password format."""
        # 00000000-00000000-00000000-00000000
        self.master_file = 'master'
        self.account_file = ''
        self.option = 0

    def enter_master(self):
        """Create password if one does not exist."""
        all_good = False
        
        if path.exists(self.master_file) == False:
            master_password = '0'
            master_pw = '1'
            all_good = False
            
            while all_good == False:
                print("\nA master password has not been created.")
                print("Let's create your master password.\n")
                print("Passwords must be at least 15 characters long.")
                print("Passwords must include lower case, upper case, numbers, and special characters.\n")
                master_password = getpass.getpass(prompt="Enter new master password: ")
                master_pw = getpass.getpass(prompt="Retype master password: ")
                
                if master_password != master_pw:
                    print("\nPasswords do not match.\n")
                elif len(master_password) < 15:
                    print("\nPassword must be at least 15 characters in length.\n")
                else:   
                    is_lower = [characters in self.lower_case_letters for characters in master_password]
                    is_upper = [characters in self.upper_case_letters for characters in master_password]
                    is_number = [characters in self.numbers for characters in master_password]
                    is_symbol = [characters in self.symbols for characters in master_password]

                    if any(is_lower) == True and any(is_upper) == True and any(is_number) == True and any(is_symbol) == True:
                        all_good = True
                        self.hash_password(master_password)
                        self.generate_key()
                    else:
                        pass
                    
        """Login if password has been created."""
        stored_hash = '0'
        hashed = '1'
        count = 0
        while hashed != stored_hash and count < 3:
            password = getpass.getpass("\nEnter master password: ")
            hashed = self.hash_password(password)

            with open(self.master_file, 'r') as file:
                stored_hash = file.read()

            if stored_hash != hashed:    
                print("\nIncorrect password.\n")
                count += 1
            else:
                pass
            
        if count == 3:
            os.sys.exit()
        else:
            self.display_options()

    def clear_screen(self):
        """Clears the screen for prettier formatting."""
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

    def display_options(self):
        choice = ''
        while choice != '1' or choice != '2' or choice != '3' or choice != '4' or choice != '5':
            print("\nChoose an option(1 - 5).\n")
            print("1. Add New Account")
            print("2. Find Account")
            print("3. Generate Password")
            print("4. Change Master Password")
            print("5. Quit\n")
            choice = input(":> ")
        
            if choice == '1':
                self.option = 1
                self.add_account()
            elif choice == '2':
                self.option = 2
                self.find_account()
            elif choice == '3':
                self.option =3
                self.generate_password()
            elif choice == '4':
                self.option = 4
                self.change_master_password()
            elif choice == '5':
                os.sys.exit()
            else:
                print("\nInvalid choice.\n")

    def add_account(self):
        check_conts = ''
        print("\nA randomly generated password will be stored for each new account.")
        self.account_file = input("Enter account name: ")
        password = self.generate_password()
        encrypted_password = self.encrypt_password(password)

        if path.exists(self.account_file) == False:
            with open(self.account_file, 'ab') as file:
                file.write(encrypted_password)

            print("\nAccount added.")
        else:
            print("\nThat account already exists.")

    def find_account(self):
        check_contents = ''
        print("\nWARNING: Account passwords will be shown in plain text!")
        self.account_file = input("Which account are you looking for? ")
        
        if path.exists(self.account_file) == False:
            print("\nThat account does not exist.")
        else:
            with open(self.account_file, 'rb') as file:
                password = file.read()
                cleartext_password = self.decrypt_password(password)
                print(f"\nThe password for {self.account_file} is {cleartext_password}\n")
                print("Screen will clear in 5 seconds.")
                time.sleep(5)
                self.clear_screen()
                
    def change_master_password(self):
        stored_hash = '0'
        hashed = '1'
        count = 0
        while hashed != stored_hash and count < 3:
            password = getpass.getpass("\nEnter master password: ")
            hashed = self.hash_password(password)

            with open(self.master_file, 'r') as file:
                stored_hash = file.read()

            if stored_hash != hashed:    
                print("\nIncorrect password.\n")
                count += 1
            else:
                master_password = '0'
                master_pw = '1'
                all_good = False
            
                while all_good == False:
                    print("Let's create your master password.\n")
                    print("Passwords must be at least 15 characters long.")
                    print("Passwords must include lower case, upper case, numbers, and special characters.\n")
                    master_password = getpass.getpass(prompt="Enter new master password: ")
                    master_pw = getpass.getpass(prompt="Retype master password: ")
                
                    if master_password != master_pw:
                        print("\nPasswords do not match.\n")
                    elif len(master_password) < 15:
                        print("\nPassword must be at least 15 characters in length.\n")
                    else:   
                        is_lower = [characters in self.lower_case_letters for characters in master_password]
                        is_upper = [characters in self.upper_case_letters for characters in master_password]
                        is_number = [characters in self.numbers for characters in master_password]
                        is_symbol = [characters in self.symbols for characters in master_password]

                        if any(is_lower) == True and any(is_upper) == True and any(is_number) == True and any(is_symbol) == True:
                            all_good = True
                            new_password = self.hash_password(master_password)
                            self.save_password(new_password)
                            print("\nMaster password has been changed.\n")
                        else:
                            print("\nMaster password has not been changed.\n")        

    def hash_password(self, pw):
        unhexed = []
        shift_pw = []
        # convert pw to binary
        bin_pw = ''.join(format(ord(i), '08b') for i in pw)
        # Shift digits
        for bit in bin_pw:
            shift_pw.append(bit)
        
        shift_pw.reverse()

        rev_pw = ''.join(shift_pw)
        # Convert to decimal
        dec_pw = int(rev_pw, 2)
        # Multiply by diameter of the sun
        calc_pw = dec_pw * 865370
        # Back to binary
        binary_pw = bin(calc_pw)
        # Shift digits
        shift_pw.clear()
        for bit in binary_pw:
            shift_pw.append(bit)
        
        shift_pw.reverse()
        rev_pw = ''

        rev_pw = ''.join(shift_pw)
        # Convert to Hex
        bits = []
        bites = []
        count = 0
        for bit in rev_pw:
            if count < 8:
                bits.append(bit)
                count += 1
            if count == 8:
                octet = "".join(bits)
                hashed = binascii.b2a_uu(bytes(octet, encoding='utf-8'))
                bites.append(hashed)
                bits.clear()
                count = 0

        hashed_password = ''.join(str(bites))
        # Save / Return hashed password
        if path.exists(self.master_file) == False:
            self.save_password(hashed_password)
        else:
            return hashed_password

    def save_password(self, pw):
        with open(self.master_file, 'wb') as file:
            encoded_pw = pw.encode()
            file.write(encoded_pw)

    def generate_key(self):
        key = Fernet.generate_key()
        with open('key', 'wb') as file:
            file.write(key)

    def load_key(self):
        with open('key', 'rb') as file:
            key = file.read()

        return key

    def encrypt_password(self, pw):
        key = self.load_key()
        encoded_password = pw.encode()
        f = Fernet(key)
        encrypted_password = f.encrypt(encoded_password)
        return encrypted_password

    def decrypt_password(self, pw):
        key = self.load_key()
        f = Fernet(key)
        decrypted_password = f.decrypt(pw)
        return decrypted_password.decode()

    def generate_password(self):
        x = 35
        while x != 0:
            pick_character_type = random.choice(self.characters)
            pick_character = random.choice(pick_character_type)
            self.password.append(pick_character)
            x -= 1
            if x == 27:
                self.password.append('-')
                x -= 1
            elif x == 18:
                self.password.append('-')
                x -= 1
            elif x == 9:
                self.password.append('-')
                x -= 1

        random_password = ''
        for char in self.password:
            random_password += char

        if self.option == 3:
            print(f"\nRandomly generated password is: {random_password}")
            self.password.clear()
        else:
            self.password.clear()
            return random_password

if __name__ == '__main__':       
    gp = PasswordGenerator()
    gp.enter_master()
