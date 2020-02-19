from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time


class InitialWaitPage(WaitPage):
    group_by_arrival_time = True
    title_text = 'Waiting for other players to complete the instructions'
    template_name = "waiting/InitialWaitPage.html"

    def get_players_for_group(self, waiting_players):
        print('get players', waiting_players)
        ready =  len(waiting_players) >= self.session.config['min_players_start']

        for player in waiting_players:
            if player.participant.vars["time_joined"] == 0:
                player.participant.vars["time_joined"] = time.time()


        self.session.vars["players_waiting"] = len(waiting_players)
        max_wait = max([time.time() - player.participant.vars["time_joined"] for player in waiting_players])
        print(max_wait)
        if self.session.vars["min_players_passed"]:
            if self.session.vars["experiment_done"] == False:
                self.session.vars["n_active"] += len(waiting_players)
            else:
                for player in waiting_players:
                    player.participant.vars["is_full"] = True
            return waiting_players
        elif ready:
            self.session.vars["min_players_passed"] = True
            for player in waiting_players:
                player.wait_time = time.time() - player.participant.vars["time_joined"]
                player.participant.vars["tot_wait_time"] = time.time() - player.participant.vars["time_joined"]
                player.participant.vars["time_joined"] = 0
                print(player.participant.vars["tot_wait_time"])
            return waiting_players
        elif max_wait > self.session.config["timeout_mins"]*60 and len(waiting_players) >= 4:
            self.session.vars["min_players_passed"] = True
            for player in waiting_players:
                player.wait_time = time.time() - player.participant.vars["time_joined"]
                # player.participant.vars["timeout"] = True
                player.participant.vars["tot_wait_time"] = time.time() - player.participant.vars["time_joined"]
                print(player.participant.vars["tot_wait_time"])
                self.session.vars["n_active"] = len(waiting_players)
            return waiting_players





    def vars_for_template(self):
        return {
            "num_here": self.session.vars["players_waiting"],
            "num_max": self.session.config["min_players_start"],
            "timeout_mins": self.session.config["timeout_mins"]
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

class TimeoutPage(Page):
    def is_displayed(self):
        if self.player.participant.vars["timeout"]:
            # self.player.payoff = self.session.config["timeout_bonus"]/self.session.config["real_world_currency_per_point"]
            return True
        else:
            return False

    def vars_for_template(self):
        wait_bonus = round(min(self.player.participant.vars['tot_wait_time']*self.session.config['pay_for_waiting'], self.session.config['max_pay_for_waiting']),2)
        self.player.payoff = (wait_bonus + 1)/self.session.config['real_world_currency_per_point']
        tot_bonus = self.participant.payoff.to_real_world_currency(self.session)
        return {
            "timeout_bonus": "1",
            "wait_bonus": wait_bonus,
            "tot_bonus": tot_bonus
        }

page_sequence = [
    InitialWaitPage,
    FullPage,
    TimeoutPage
]
