"""Script to generate password hashes for one or more user accounts.

You can use this script to generate bcrypt password hashes for all of the
initial user accounts in your database creation script. Remember that each
of your user accounts should have its own unique password.

Before running this script, you'll need to replace the list of user accounts
(the block beginning "users = [") with the actual list of user accounts you
want to generate hashes for.
"""
from collections import namedtuple
from flask import Flask
from flask_bcrypt import Bcrypt

# We use a "named tuple" here to create a simple "User Account" class that can
# store a username and password.
# It lets us access the username and password by name: for example, if we create a
# UserAccount named "myuser", like this:
# 
# myuser = UserAccount('myusername', 'mypassword')
# 
# We can then access those values via "myuser.username" and "myuser.password",
# instead of having to access myuser[0] and myuser[1] like you would have to
# with a regular tuple.
UserAccount = namedtuple('UserAccount', ['username', 'password'])

app = Flask(__name__)
flask_bcrypt = Bcrypt(app)

# Replace the example UserAccount objects below with the initial user accounts
# for your own web app. You can add as many as you need to the list.
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
    # Generate a bcrypt hash using the default settings. This function returns
    # the hash as 59-60 bytes (always 60 in the current version of bcrypt).
    password_hash = flask_bcrypt.generate_password_hash(user.password)
    
    # Check whether the hash matches the original password. We don't really
    # need to do this here: this is just to show how your web app would check a
    # password supplied by the user (user.password) against a hash value
    # retrieved from the database (password_hash).
    # 
    # This returns True if the password matches, or False if it doesn't.
    password_matches_hash = flask_bcrypt.check_password_hash(password_hash, user.password)

    # Output username, password, hash, and the result of our verification test.
    # 
    # Note that username is never actually used when generating the hash or
    # checking a password. We only include username here for display purposes,
    # to make it easier for you to copy the right password for each user when
    # creating your database population script.
    #
    # We call password_hash.decode() to translate the series of bytes that make
    # up the hash into a UTF-8 encoded string of characters. Otherwise, when 
    # Python prints out the hash, it will surrounded it with `b''` to indicate
    # that the hash is a binary string. You don't need to do this if you're
    # passing the hash in to MySQL: you can just use password_hash directly, as
    # we do in the LCC Issue Tracker project, and it will accept the binary string.
    print(f'{user.username} | {user.password} | {password_hash.decode()} | {password_matches_hash}')