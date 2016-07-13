#!/usr/bin/env python
import sys

if len(sys.argv) < 2:
    print('Needs target Database as input!')
    sys.exit()

def query_yes_no(question, default="yes"):  # From http://stackoverflow.com/questions/3041986/apt-command-line-interface-like-yes-no-input
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

if not query_yes_no('This will delete all entries in the Database. Are you sure?'):
    sys.exit()

from app import models, db

users = models.User.query.all()
for u in users:
    db.session.delete(u)

posts = models.Post.query.all()
for p in posts:
    db.session.delete(p)

db.session.commit()
print('Done!')
