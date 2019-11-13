from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import time


class PlayerBot(Bot):

    def play_round(self):
        if self.round_number < self.session.vars["n_periods"]:
            # print(self.PlayerClass.__dict__.keys())
            time.sleep(2)
            yield pages.Choice, {"choice": True}
            time.sleep(5)
            yield pages.RoundResultsPage
        if self.round_number == Constants.num_rounds:
            time.sleep(5)
            yield pages.LastPage
