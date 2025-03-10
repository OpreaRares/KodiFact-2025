import sqlite3
import os

#DOAR PENTRU RESETAREA DATABASE-ULUI!!
def reset_database():
    if os.path.exists("users.db"):
        os.remove("users.db")
    print("Database has been reset.")

#reset_database()