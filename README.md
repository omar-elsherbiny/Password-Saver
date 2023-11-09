# Password-Saver
One of the very old proects i made with a _PyQt5_ GUI

It basically lets you make an account to store your usernames and passwords for various websites
- The passwords for the accounts are saved int the `"account_name".txt` using a hashing algorithm i made myself along with a salt
- The websites/usernames/passwords saved in each account are in `"account_name".csv` and encrypted with another algorithm i tried to come up with
- The range of numbers in the main screen is supposed to give an estimate of the strength of the password based on its entropy 
- `seed.env` just stores a number used by both the encryption and hashing algorithm, not really a pepper but still adds more security