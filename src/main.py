'''
this is the main file of the project
'''
# pylint: disable=C0115,C0116,C0301

from pypresence import Presence
from pypresence.exceptions import (
    DiscordNotFound,
    PyPresenceException
)
from time import sleep

from models import Config, Game, User, PresenceUpdate, asdict
from steam import get_user_by_id, get_users_owned_games
from utils import write_error_log


__version__ = '0.1.0'

CONFIG = Config.load_from_json_file('config.json')

RPC = Presence(CONFIG.discord_application_id)

USERS_GAMES: list[Game] = get_users_owned_games(
    CONFIG.steam_api_key, CONFIG.steam_id)


def generate_presence(user: User, games: list[Game], config: Config) -> PresenceUpdate:
    if user.is_playing:
        if user.is_in_lobby:
            print("User is playing and in lobby")
            return PresenceUpdate.make_lobby(user=user, games=games, config=config)
        print("User is playing")
        return PresenceUpdate.make_simple(user=user, games=games, config=config)
    print("User is idle")
    return PresenceUpdate.idle()


def presence_loop():
    try:
        # connect to discord
        RPC.connect()
        while True:

            # get the user
            user = get_user_by_id(CONFIG.steam_api_key, CONFIG.steam_id)

            # generate presence based on known data
            presence = generate_presence(user, USERS_GAMES, CONFIG)

            # update presence
            _ = RPC.update(**asdict(presence))
            sleep(15)
    except DiscordNotFound as e:
        print("Discord not found. Make sure Discord is running.")
        write_error_log(e.with_traceback())


def main():
    presence_loop()


if __name__ == '__main__':
    main()
