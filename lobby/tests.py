from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import time
import numpy as np


class PlayerBot(Bot):

    def play_round(self):
        if self.round_number == 1:
            base = self.session.config["base_points"]
            A_val = base - 1
            A_other = 4
            sum = A_val + A_other
            time.sleep(10 + 120*np.random.rand())
            # yield pages.Instructions, {"q1": sum, "q2":base, "q3":"20%", "q4":"25%"}
            yield pages.Instructions, {"q1": sum, "q2":base, "q3":"20%"}
