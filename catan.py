from collections import Counter


class Tile:
    
    resources = ['wood', 'sheep', 'wheat', 'brick', 'ore']
    # Number of chances of sum on 2d6 out of 36.
    hit_odds = {2:1, 3:2, 4:3, 5:4, 6:5, 8:5, 9:4, 10:3, 11:2, 12:1}

    def __init__(self, resource, chit):
        """
        :param resource: Resource Type of the given tile.
        :type resource: String description of Resource Type.
        :param chit: Value on the numbered chit.
        :type chit: Integer
        """
        if resource.lower() not in Tile.resources:
            raise Exception  # TODO Create valid Exception Type
        self.resource = resource.lower()

        if chit not in Tile.hit_odds.keys():
            raise Exception  # TODO Create valid Exception Type
        self.chit = chit

    @property
    def odds(self):
        """
        Return the given odds that a tile will be hit.
        """
        return Tile.hit_odds[self.chit] / 36  # 36 total possibilities

    def get_turn_rates(self, trade_rate=4):
        """
        Return a dictionary of the possible odds on a given turn of each
        resource.

        :param trade_rate: The rate at which trades on this resource happen.
        :trade_rate type: Number
        """
        resource_odds = {}

        for r in Tile.resources:
            if r == self.resource:
                resource_odds[r] = 1 * self.odds
            else:
                resource_odds[r] = (1 / trade_rate) * self.odds

        return resource_odds


class Settlement:

    default_trade_rates = {'wood':4, 'sheep':4, 'wheat':4, 'brick':4, 'ore':4}

    def __init__(self, tiles):
        self.tiles = tiles

    def get_turn_rates(self, port_rates=default_trade_rates):
        """
        Return the turn rates for each resource.
        :param port_rates: Dictionary of Resources and Trade Rates
        :param type: dictionary
        """
        rates = Counter()
        for tile in self.tiles:
            rate = tile.get_turn_rates(port_rates[tile.resource])
            rates.update(rate)

        return rates

    def get_hit_rate(self):
        """
        Return hit rate for the settlement.
        """
        return sum(t.odds for t in self.tiles)


class Board:
    pass
