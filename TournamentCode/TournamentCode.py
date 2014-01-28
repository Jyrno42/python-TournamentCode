import json
import base64


class TournamentCodeException(Exception):
    pass


class GameConfig(object):
    def __init__(self, name, password='test', report_url='http://example.com/report', extra_data=None):
        self.name = name
        self.password = password
        self.report_url = report_url

        if isinstance(extra_data, dict):
            self.extra_data = extra_data
        else:
            self.extra_data = {
                'game': extra_data or 1,
            }

    def serialize(self):
        return base64.b64encode(json.dumps({
            "name": self.name,
            "password": self.password,
            "report": self.report_url,
            "extra": json.dumps(self.extra_data),
        }))


class TournamentCode(object):
    SUMMONERS_RIFT = 1
    TWISTED_TREELINE = 4
    PROVING_GROUNDS = 7
    CRYSTAL_SCAR = 8

    BLIND_PICK = 1
    DRAFT_MODE = 2
    ALL_RANDOM = 4
    TOURNAMENT_DRAFT = 6

    SPEC_NONE = "NONE"
    SPEC_ALL = "ALL"
    SPEC_LOBBY_ONLY = "LOBBYONLY"
    SPEC_FRIENDS = "DROPINONLY"

    MAPS = (
        (SUMMONERS_RIFT, 'Summoners Rift'),
        (TWISTED_TREELINE, 'Twisted Treeline'),
        (PROVING_GROUNDS, 'Proving Grounds'),
        (CRYSTAL_SCAR, 'Crystal Scar'),
    )

    PICK_MODES = (
        (BLIND_PICK, 'Blind Pick'),
        (DRAFT_MODE, 'Draft Pick'),
        (ALL_RANDOM, 'All Random'),
        (TOURNAMENT_DRAFT, 'Tournament Draft'),
    )

    SPEC_CONFIG = (
        (SPEC_NONE, 'None'),
        (SPEC_ALL, 'All'),
        (SPEC_LOBBY_ONLY, 'Invite only'),
        (SPEC_FRIENDS, 'Friends only'),
    )

    @staticmethod
    def generate(config, map_id=None, pick_mode=None, team_size=5, spec_config=None):
        map_id = map_id or TournamentCode.SUMMONERS_RIFT
        pick_mode = pick_mode or TournamentCode.BLIND_PICK
        spec_config = spec_config or TournamentCode.SPEC_ALL

        if not isinstance(config, GameConfig):
            raise TournamentCodeException('Invalid game config')

        if map_id not in dict(TournamentCode.MAPS):
            raise TournamentCodeException('Invalid map specified.')

        if pick_mode not in dict(TournamentCode.PICK_MODES):
            raise TournamentCodeException('Invalid pick mode specified.')

        if spec_config not in dict(TournamentCode.SPEC_CONFIG):
            raise TournamentCodeException('Invalid spectator mode specified.')

        if team_size not in [1, 2, 3, 4, 5]:
            raise TournamentCodeException('Invalid team size')

        if map_id == TournamentCode.TWISTED_TREELINE and team_size > 3:
            raise TournamentCodeException('Maximum team size in twisted treeline is 3')

        return TournamentCode._build_url({
            'mapId': map_id,
            'pickMode': pick_mode,
            'teamSize': team_size,
            'specConfig': spec_config,
            'otherData': config.serialize(),
        })

    @staticmethod
    def _build_url(args):
        return ("pvpnet://lol/customgame/joinorcreate/"
                "map%(mapId)d/pick%(pickMode)d/team%(teamSize)d"
                "/spec%(specConfig)s/%(otherData)s") % args


class TournamentPlayer(object):

    def __init__(self, raw_data=None):
        self.raw_data = raw_data

        self.level = None
        self.team_id = None
        self.summoner_name = None
        self.skin_name = None
        self.profile_icon_id = None
        self.spell_1_id = None
        self.spell_2_id = None
        self.is_winner = False
        self.is_leaver = False
        self.is_bot = False
        self.statistics = dict()

        if raw_data:
            if isinstance(raw_data, dict):
                self.load_dict(raw_data)
            elif isinstance(raw_data, basestring):
                self.load_str(raw_data)
            else:
                raise NotImplementedError("Can't load player info from type %s" % type(raw_data))

    def load_dict(self, raw_data):
        assert isinstance(raw_data, dict), "raw_data type is %s (dict expected)" % (type(raw_data))

        self.level = raw_data.get('level', None)
        self.team_id = raw_data.get('teamId', None)
        self.summoner_name = raw_data.get('summonerName', None)
        self.skin_name = raw_data.get('skinName', None)
        self.profile_icon_id = raw_data.get('profileIconId', None)
        self.spell_1_id = raw_data.get('spell1Id', None)
        self.spell_2_id = raw_data.get('spell2Id', None)
        self.is_winner = raw_data.get('isWinningTeam', None)
        self.is_leaver = raw_data.get('leaver', None)
        self.is_bot = raw_data.get('botPlayer', None)

        for item in raw_data.get('statistics', []):
            self.statistics[item['statTypeName']] = item['value']

    def load_str(self, raw_data):
        assert isinstance(raw_data, basestring), "raw_data type is %s (string expected)" % (type(raw_data))

        try:
            data = json.loads(raw_data)
        except ValueError:
            raise ValueError("raw_data is not valid json")
        else:
            self.load_dict(data)


class TournamentGameResult(object):
    BLUE_TEAM = 100
    PURPLE_TEAM = 200

    TEAMS = (
        (BLUE_TEAM, 'Blue'),
        (PURPLE_TEAM, 'Purple'),
    )

    def __init__(self, raw_data=None):
        self.raw_data = raw_data

        self.version = None
        self.meta_data = None
        self.game_id = None
        self.game_length = None
        self.game_type = None
        self.game_mode = None
        self.ranked = None
        self.winning_team_id = None

        self.teams = dict()

        for key, name in TournamentGameResult.TEAMS:
            self.teams[key] = list()

        if raw_data:
            if isinstance(raw_data, dict):
                self.load_dict(raw_data)
            elif isinstance(raw_data, basestring):
                self.load_str(raw_data)
            else:
                raise NotImplementedError("Can't load game info from type %s" % type(raw_data))

    def __load_meta_data(self, metadata):
        if isinstance(metadata, dict):
            packet = metadata.get('passbackDataPacket', '{}')
            try:
                val = json.loads(packet)
            except ValueError:
                pass
            else:
                metadata['passbackDataPacket'] = val

        self.meta_data = metadata

    def load_dict(self, raw_data):
        assert isinstance(raw_data, dict), "raw_data type is %s (dict expected)" % (type(raw_data))

        self.version = raw_data.get('version', None)

        self.__load_meta_data(raw_data.get('tournamentMetaData', {}))

        self.game_id = raw_data.get('gameId', None)
        self.game_length = raw_data.get('gameLength', None)
        self.game_type = raw_data.get('gameType', None)
        self.game_mode = raw_data.get('gameMode', None)
        self.ranked = raw_data.get('ranked', None)

        for player in raw_data.get('teamPlayerParticipantsSummaries', []):
            player = TournamentPlayer(player)
            self.teams[TournamentGameResult.BLUE_TEAM].append(player)

            if player.is_winner:
                self.winning_team_id = TournamentGameResult.BLUE_TEAM

        for player in raw_data.get('otherTeamPlayerParticipantsSummaries', []):
            player = TournamentPlayer(player)
            self.teams[TournamentGameResult.PURPLE_TEAM].append(player)

            if player.is_winner:
                self.winning_team_id = TournamentGameResult.PURPLE_TEAM

    def load_str(self, raw_data):
        assert isinstance(raw_data, basestring), "raw_data type is %s (string expected)" % (type(raw_data))

        try:
            data = json.loads(raw_data)
        except ValueError:
            raise ValueError("raw_data is not valid json")
        else:
            self.load_dict(data)
