from collections import Counter
import random


class Tile:

    resources = ['wood', 'sheep', 'wheat', 'brick', 'ore']
    # Number of chances of sum on 2d6 out of 36.
    hit_odds = {2:1, 3:2, 4:3, 5:4, 6:5, 8:5, 9:4, 10:3, 11:2, 12:1}

    def __init__(self, index, resource, chit):
        """
        :param resource: Resource Type of the given tile.
        :type resource: String description of Resource Type.
        :param chit: Value on the numbered chit.
        :type chit: Integer
        """
        self.index = index

        if resource != 'desert' and resource.lower() not in Tile.resources:
            raise Exception  # TODO Create valid Exception Type
        self.resource = resource.lower()

        if chit != 0 and chit not in Tile.hit_odds.keys():
            raise Exception  # TODO Create valid Exception Type
        self.chit = chit

    @property
    def odds(self):
        """
        Return the given odds that a tile will be hit.
        """
        if self.chit == 0:
            return 0
        return Tile.hit_odds[self.chit] / 36  # 36 total possibilities

    def get_turn_rates(self, trade_rate=4):
        """
        Return a dictionary of the possible odds on a given turn of each
        resource.

        :param trade_rate: The rate at which trades on this resource happen.
        :trade_rate type: Number
        """
        if self.resource == 'desert':
            return {}

        resource_odds = {}

        for r in Tile.resources:
            if r == self.resource:
                resource_odds[r] = 1 * self.odds
            else:
                resource_odds[r] = (1 / trade_rate) * self.odds

        return resource_odds


class Settlement:

    default_trade_rates = {'wood':4, 'sheep':4, 'wheat':4, 'brick':4, 'ore':4}

    def __init__(self, index, tiles):
        self.index = index
        self.tiles = tiles

    def get_turn_rates(self, port_rates=default_trade_rates):
        """
        Return the turn rates for each resource.
        :param port_rates: Dictionary of Resources and Trade Rates
        :param type: dictionary
        """
        rates = Counter()
        for tile in self.tiles:
            if tile.resource == 'desert':
                continue
            rate = tile.get_turn_rates(port_rates[tile.resource])
            rates.update(rate)

        return rates

    def get_hit_rate(self):
        """
        Return hit rate for the settlement.
        """
        return sum(t.odds for t in self.tiles)


class Board:

    tile_counts = {
        'wood':4,
        'wheat':4,
        'sheep':4,
        'brick':3,
        'ore':3,
        'desert':1
    }

    chits = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]

    settlement_i_by_tile_i = [
        (0, 4, 8, 12, 7, 3),
        (1, 5, 9, 13, 8, 4),
        (2, 6, 10, 14, 9, 5),
        (7, 12, 17, 16, 11),
        (8, 13, 18, 17, 12),
        (9, 14, 19, 18, 13),
        (10, 15, 20, 25, 19, 14),
        (16, 22, 28, 33, 27, 21),
        (17, 23, 29, 34, 28, 22),
        (18, 24, 30, 35, 29, 23),
        (19, 25, 31, 36, 30, 24),
        (20, 26, 32, 37, 31, 25),
        (28, 34, 39, 43, 38, 33),
        (29, 35, 40, 44, 39, 34),
        (30, 35, 41, 45, 40, 35),
        (31, 36, 42, 46, 41, 36),
        (39, 44, 48, 51, 47, 43),
        (40, 45, 49, 52, 48, 44),
        (41, 46, 50, 53, 49, 45)
    ]

    @classmethod
    def new_board(cls, seed=None):
        """
        Return a new random board.
        :param seed: Random seed.
        """
        if seed:
            random.seed(seed)

        tiles = []
        for resource, count in cls.tile_counts.items():
            if resource != 'desert':
                tiles += [resource] * count
        random.shuffle(tiles)

        chits = cls.chits.copy()
        random.shuffle(chits)

        spots = list(zip(tiles, chits))
        spots.append(('desert', 0))

        return cls(spots)

    def __init__(self, tiles):
        """
        :param tiles: List of tiles of the board.
        :param type: List
        """
        self.tiles = [Tile(i, resource, chit) for i, (resource, chit) in enumerate(tiles)]
        self.settlements = self.generate_settlements()

    def generate_settlements(self):
        """
        Return a list of settlements with correct tiles.
        """
        # TODO Add Port Generation to this function
        settlements = []

        for i in range(54):
            neighbor_tiles = []
            for tile_i, settlement_i in enumerate(Board.settlement_i_by_tile_i):
                if i in settlement_i:
                    neighbor_tiles.append(self.tiles[tile_i])

            settlements.append(Settlement(i, neighbor_tiles))

        return settlements
