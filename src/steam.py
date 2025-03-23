'''
This module is used to interact with the Steam Web API.
'''
# pylint: disable=C0115,C0116,C0301

from steam_web_api import Steam
from models import Game, User


def get_user_by_id(api_key: str, steam_id: str) -> User:
    steam = Steam(api_key)
    user_data = steam.users.get_user_details(steam_id)["player"]
    user = User(**user_data)
    return user


def get_users_owned_games(api_key: str, steam_id: str) -> list[Game]:
    steam = Steam(api_key)
    games_data = steam.users.get_owned_games(steam_id)["games"]
    games = [Game(**game) for game in games_data]
    return games
