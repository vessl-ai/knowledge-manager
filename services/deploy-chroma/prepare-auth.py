#!/usr/bin/env python3

import argparse
import crypt
import sys

import bcrypt
import dotenv

config = dotenv.dotenv_values(".env")

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--username", help="Username to add to the htpasswd file")
    parser.add_argument("--password", help="Password to add to the htpasswd file")

    args = parser.parse_args()

    username = args.username
    password = args.password

    with open("server.htpasswd", "w") as userdb:
        encrypted_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        userdb.write(f"{username}:{str(encrypted_password.decode())}\n")

if __name__ == "__main__":
    main()