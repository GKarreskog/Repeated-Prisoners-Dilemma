from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import time 


class ResultsWaitPage(WaitPage):
    group_by_arrival_time = True
    title_text = 'Waiting for other players to complete the instructions'
    body_text = '''
        The experiment will begin when 20 participants have completed the
        instructions. This might take a few minutes and ensures that we can match you with other
        players quickly, without making you wait long periods throughout the experiment. Remember that you are being paid an hourly wage of $7 for the time spent on this wait page. 
    '''
    # template_name = "waiting/InitialWaitPage.html"

    def get_players_for_group(self, waiting_players):
        print('get players', waiting_players)
        ready =  len(waiting_players) >= self.session.config['min_players_start']

        for player in waiting_players:
            if player.participant.vars["time_joined"] == 0:
                player.participant.vars["time_joined"] = time.time()


        self.session.vars["players_waiting"] = len(waiting_players)

        if self.session.vars["min_players_passed"]:
            for player in waiting_players:
                player.participant.vars["is_full"] = True
            return waiting_players
        elif ready:
            self.session.vars["min_players_passed"] = True
            for player in waiting_players:
                player.participant.vars["tot_wait_time"] = time.time() - player.participant.vars["time_joined"]
                player.participant.vars["time_joined"] = 0
                print(player.participant.vars["tot_wait_time"])
            return waiting_players
        


    def vars_for_template(self):
        return {
            "num_here": self.session.vars["players_waiting"],
            "num_max": self.session.config["min_players_start"]
        }

class FullPage(Page):
    def is_displayed(self):
        if self.player.participant.vars["is_full"]:
            self.player.payoff = self.session.config["quiz_bonus"]/self.session.config["real_world_currency_per_point"]
            return True
        else:
            return False

    def vars_for_template(self):
        return {
            "bonus": self.session.config["quiz_bonus"]
        }

page_sequence = [
    ResultsWaitPage,
    FullPage
]

