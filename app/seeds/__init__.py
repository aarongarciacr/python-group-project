from flask.cli import AppGroup
from .users import seed_users, undo_users
from .products import seed_products, undo_products
from .carts import seed_carts, undo_carts
from .favorites import seed_favorites, undo_favorites
from .reviews import seed_reviews, undo_reviews

from app.models.db import environment 

# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup('seed')


# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    if environment == 'production':
        # Before seeding in production, you want to run the seed undo 
        # command, which will  truncate all tables prefixed with 
        # the schema name (see comment in users.py undo_users function).
        # Make sure to add all your other model's undo functions below
        undo_users()
        undo_products()
        undo_carts()
        undo_favorites()
        undo_reviews()
    seed_users()
    seed_products()
    seed_carts()
    seed_favorites()
    seed_reviews()
    # Add other seed functions here


# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    undo_users()
    undo_products()
    undo_carts()
    undo_favorites()
    undo_reviews
    # Add other undo functions here
