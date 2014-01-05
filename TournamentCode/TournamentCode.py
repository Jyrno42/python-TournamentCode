


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
    SPEC_LOBBYONLY = "LOBBYONLY"
    SPEC_FRIENDS = "DROPINONLY"

    MAPS = (
        (SUMMONERS_RIFT, 'Summoners Rift'),
        (TWISTED_TREELINE, 'Twisted Treeline'),
        (PROVING_GROUNDS, 'Proving Grounds'),
        (CRYSTAL_SCAR, 'Crystal Scar'),
    )

    def generate(self, config, mapId=None, pickMode=None, teamSize=5, specConfig=None):
        pass

    def _build_url(self, args):
        return ("pvpnet://lol/customgame/joinorcreate/"
               "map%(mapId)d/pick%(pickMode)d/team%(teamSize)d"
               "/spec%(specConfig)s/%(otherData)s") % args