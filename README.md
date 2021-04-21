# PasswordManager
With this simple CLI password manager you can add accounts, look up accounts, and generate random passwords.
When first runnning the program you will be forced to create a master password that you will use to gain access to the program's functions.
The master password format should be the same as the program uses to genereate account passwords.

The master password will be obfuscated and any account passwords will be encrypted. Account passwords are never shown in plain text unless looking up an account.
When account is looked up, you are warned of plain text passwords being shown. The password is shown for 5 seconds then the screen is cleared.

When adding an account a random password is generated automatically using the following format:

1. At least 1 lower case character.
2. At least 1 upper case character.
3. At least 1 special character.
4. The password is separated in four 8 character sections by a dash ( - ).
5. The password will have this format: 00000000-00000000-00000000-00000000.

Unfortunately, I have found that some websites will not allow this many characters in it's password creation.
I feel this limitation is quite silly, considering the importance of security today as well as the implimentation of password managers.
