'''
this module holds dataclasses
'''
# pylint: disable=C0115,C0116,C0301

from dataclasses import dataclass, asdict
import json


@dataclass
class Config:
    # discord
    discord_application_id: str

    # steam
    steam_api_key: str
    steam_id: str

    # settings
    autostart: bool = False
    show_invite_button: bool = True
    show_all_games: bool = True
    allowed_games: list[str] = None

    @classmethod
    def load_from_json_file(cls, path):
        with open(path, 'r', encoding="utf-8") as f:
            data = json.load(f)

        return cls(
            # discord
            discord_application_id=data['discord']['application_id'],

            # steam
            steam_api_key=data['steam']['api_key'],
            steam_id=data['steam']['id'],

            # settings
            autostart=data['settings']['autostart'],
            show_invite_button=data['settings']['show_invite_button'],
            show_all_games=data['settings']['show_all_games'],
            allowed_games=data['settings']['allowed_games']
        )

    @classmethod
    def create_default(cls, path: str = "config.json"):
        with open(path, 'w', encoding="utf-8") as f:
            json.dump({
                "discord": {
                    "application_id": "your_discord_application_id"
                },
                "steam": {
                    "api_key": "your_steam_api_key",
                    "id": "your_steam_id"
                },
                "settings": {
                    "autostart": cls.autostart,
                    "show_invite_button": cls.show_invite_button,
                    "show_all_games": cls.show_all_games,
                    "allowed_games": []
                }
            }, f, indent=4)


@dataclass
class Game:

    appid: int
    name: str
    playtime_2weeks: int = None
    playtime_forever: int = None
    img_icon_url: str = None
    has_community_visible_stats: bool = None
    playtime_windows_forever: int = None
    playtime_mac_forever: int = None
    playtime_linux_forever: int = None
    playtime_deck_forever: int = None
    rtime_last_played: int = None
    playtime_disconnected: int = None
    has_leaderboards: bool = None
    content_descriptorids: list[int] = None

    @property
    def icon_url(self):
        return f"http://media.steampowered.com/steamcommunity/public/images/apps/{self.appid}/{self.img_icon_url}.jpg"

    @property
    def total_playtime_hours(self):
        playtime_minutes = self.playtime_forever
        playtime_hours = playtime_minutes // 60
        return playtime_hours


@dataclass
class User:
    steamid: str
    communityvisibilitystate: int
    personaname: str
    profileurl: str
    avatar: str
    avatarmedium: str
    avatarfull: str
    personastate: int
    profilestate: int = None
    avatarhash: str = None
    lastlogoff: int = None
    realname: str = None
    primaryclanid: str = None
    timecreated: int = None
    personastateflags: int = None
    gameextrainfo: str = None
    gameid: str = None
    lobbysteamid: str = None
    loccountrycode: str = None
    locstatecode: str = None
    loccityid: int = None

    @property
    def join_uri(self):
        return f"steam://joinlobby/{self.gameid}/{self.lobbysteamid}/{self.steamid}"

    @property
    def is_online(self):
        '''
        The user's current status.
        0 = Offline
        1 = Online
        2 = Busy
        3 = Away
        4 = Snooze
        5 = looking to trade
        6 = looking to play
        If the player's profile is private, this will always be "0"
        '''
        return self.personastate == 1

    @property
    def is_playing(self):
        return self.gameid is not None

    @property
    def is_in_lobby(self):
        return self.lobbysteamid is not None


@dataclass
class PresenceUpdate:
    # general status
    state: str = None
    details: str = None

    # timestamps
    start: int = None
    end: int = None

    # large image
    large_image: str = None
    large_text: str = None

    # small image
    small_image: str = None
    small_text: str = None

    # party
    party_id: str = None
    party_size: list = None
    join: str = None
    spectate: str = None
    match: str = None

    buttons: list[dict[str, str]] = None
    instance: bool = True
    payload_override: dict = None

    @classmethod
    def make_lobby(
        cls,
        user: User,
        games: list[Game],
        config: Config
    ):
        # todo: get the game the user is playing
        game: Game = None
        for g in games:
            if int(g.appid) == int(user.gameid):
                game = g
                break

        if game is None:
            return PresenceUpdate.idle()

        return PresenceUpdate(
            # general status
            state=game.name,
            details=f"{game.total_playtime_hours}h total playtime",

            # large image
            large_image=user.avatarfull,
            large_text=user.personaname,

            # small image
            small_image=game.icon_url,
            small_text=game.name,

            # buttons
            buttons=[
                {
                    'label': 'Join Lobby',
                    'url': user.join_uri
                },
                {
                    'label': 'Download SteamRPC',
                    'url': "https://github.com/EchterTimo/SteamRPC"
                }
            ]
        )

    @classmethod
    def idle(cls):
        return PresenceUpdate(
            state='Idle',
            details='No game running',
            large_text='Steam',
            buttons=[
                {
                    'label': 'Download SteamRPC',
                    'url': "https://github.com/EchterTimo/SteamRPC"
                }
            ]
        )

    @classmethod
    def make_simple(
        cls,
        user: User,
        games: list[Game],
        config: Config
    ):
        return PresenceUpdate(
            # general status
            state=user.gameextrainfo,
            details=None,

            # large image
            large_image=user.avatar,
            large_text=user.personaname,

            # small image
            small_image=None,
            small_text=None,

            # buttons
            buttons=[
                {
                    'label': 'Download SteamRPC',
                    'url': "https://github.com/EchterTimo/SteamRPC"
                }
            ]
        )
