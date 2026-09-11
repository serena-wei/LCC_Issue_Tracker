"""Generate bcrypt password hashes for initial user accounts.

Replace the `users` list below with the accounts you need hashes for,
then run this script and copy the output into your database population SQL.
"""
from collections import namedtuple
from flask import Flask
from flask_bcrypt import Bcrypt

UserAccount = namedtuple('UserAccount', ['username', 'password'])

app = Flask(__name__)
flask_bcrypt = Bcrypt(app)

users = [UserAccount('visitor1', 'Visitor1pass*'), 
         UserAccount('visitor2', 'Visitor2pass*'),
         UserAccount('visitor3', 'Visitor3pass*'), 
         UserAccount('visitor4', 'Visitor4pass*'),
         UserAccount('visitor5', 'Visitor5pass*'), 
         UserAccount('visitor6', 'Visitor6pass*'),
         UserAccount('visitor7', 'Visitor7pass*'), 
         UserAccount('visitor8', 'Visitor8pass*'),
         UserAccount('visitor9', 'Visitor9pass*'), 
         UserAccount('visitor10', 'Visitor10pass*'),
         UserAccount('visitor11', 'Visitor11pass*'), 
         UserAccount('visitor12', 'Visitor12pass*'),
         UserAccount('visitor13', 'Visitor13pass*'), 
         UserAccount('visitor14', 'Visitor14pass*'),
         UserAccount('visitor15', 'Visitor15pass*'), 
         UserAccount('visitor16', 'Visitor16pass*'),
         UserAccount('visitor17', 'Visitor17pass*'), 
         UserAccount('visitor18', 'Visitor18pass*'),
         UserAccount('visitor19', 'Visitor19pass*'), 
         UserAccount('visitor20', 'Visitor20pass*'),
         UserAccount('helper1', 'Helper1pass*'),
         UserAccount('helper2', 'Helper2pass*'),
         UserAccount('helper3', 'Helper3pass*'),
         UserAccount('helper4', 'Helper4pass*'),
         UserAccount('helper5', 'Helper5pass*'),
         UserAccount('admin1', 'Admin1pass*'),
         UserAccount('admin2', 'Admin2pass*')]

print('Username | Password | Hash | Password Matches Hash')

for user in users:
    password_hash = flask_bcrypt.generate_password_hash(user.password)
    password_matches_hash = flask_bcrypt.check_password_hash(password_hash, user.password)
    print(f'{user.username} | {user.password} | {password_hash.decode()} | {password_matches_hash}')
