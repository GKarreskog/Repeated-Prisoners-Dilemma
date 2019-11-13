from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        if self.round_number == 1:
            yield pages.Instructions, {"q1": 3, "q2": 0, "q3":"25%", "q4":"10%"}
