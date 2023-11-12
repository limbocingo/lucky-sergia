"""
LuckySergia manager.

[version: v1]
[author: mrcingo]
"""
import sys

import peewee

sys.path.append('.')

from backend.app import app
from backend.models import *


def main(args):
    with db:
        db.create_tables([User])

    if len(args) >= 2:
        if args[1] == 'start':
            app.run(debug=False)
            return 1

        if args[1] == 'administrator':
            username = input('* Username (Ej: Josep): ')
            password = input(
                f'* Password (Ej: {"".join(choices(ascii_letters + digits, k=16))}): ')

            if len(username) < 4:
                print('Username too short.')
                return 0

            if len(password) < 8:
                print('Password too short.')
                return 0

            try:
                user = User.get(User.username == username)
            except peewee.DoesNotExist:
                user = User.create(username=username,
                                   password=password, administrator=True)
                
                print('User created.')
                print(f'    ID:       {user.id}')
                print(f'    SID:      {user.sid}')
                print(f'    USERNAME: {user.username}')
                print(f'    EMAIL:    {user.email}')
                print(f'    BALANCE:  {user.balance}')
                return 1

            print('User already exists.')
            return 0


if __name__ == '__main__':
    main(sys.argv)
