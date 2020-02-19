from otree.api import Currency as c, currency_range
from otree.api import Submission
from . import pages
from ._builtin import Bot
from .models import Constants
import time
import numpy as np


class PlayerBot(Bot):

    def play_round(self):
        if self.round_number < self.session.vars["n_periods"]:
            # print(self.PlayerClass.__dict__.keys())
            # time.sleep(2)
            decision = np.random.rand() < 0.4
            # yield Submission(pages.Choice, {"choice":False}, timeout_happened=True)
            # if np.random.rand() < 0.7:
            #     print("Timeout!!!!")
            #     yield Submission(pages.Choice, {"choice": decision}, timeout_happened=True)
            # else:
            yield pages.Choice, {"choice": decision}

            # time.sleep(2)
            yield pages.RoundResultsPage
        if self.round_number == Constants.num_rounds:
            time.sleep(10)
            yield pages.LastPage
