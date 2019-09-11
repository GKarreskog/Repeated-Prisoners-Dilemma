from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import numpy as np
import time
import random

class Choice(Page):
    form_model = 'player'
    form_fields = ['choice']

    def get_timeout_seconds(self):
        return self.session.config["timeout"]

    def is_displayed(self):
        if self.player.participant.vars["is_full"]:
            return False
        elif self.player.participant.vars["timeouts"] >= 3:
            return False
        elif self.player.participant.vars["opp_dropout"]:
            return False
        elif self.player.participant.vars["skip_to_next"]:
            print("Skip happend")
            return False
        elif self.round_number < self.session.vars["n_periods"]:
            i = self.player.participant.vars["interaction"]
            print("interaction number ", i)
            print(self.session.vars["epsilons"])
            self.player.ε = self.session.vars["epsilons"][i]
            self.player.δ = self.session.vars["deltas"][i]
            self.player.benefit = self.session.vars["benefits"][i]
            self.player.cost = self.session.vars["costs"][i]
            return True
        else:
            return False

    def vars_for_template(self):
        inter = self.player.participant.vars["interaction"]
        start_round = self.session.vars["interaction_changes"][inter]
        round_in_interaction = self.round_number - start_round + 1
        if self.round_number in self.session.vars["interaction_changes"]:
            return {
                    "first":  self.round_number in self.session.vars["interaction_changes"],
                    "δ": int(self.player.δ*100),
                    "ε": int(self.player.ε*100),
                    "round_in_interaction": round_in_interaction,
                    "tot_payoff": self.player.participant.payoff,
            }
        else:
            return {
                    "first":  self.round_number in self.session.vars["interaction_changes"],
                    "self_a": self.player.participant.vars["self_a"],
                    "opp_a": self.player.participant.vars["opp_a"],
                    "payoff": self.player.participant.vars["payoff"],
                    "δ": int(self.player.δ*100),
                    "ε": int(self.player.ε*100),
                    "round_in_interaction": round_in_interaction,
                    "tot_payoff": self.player.participant.payoff,
            }

    def before_next_page(self):
        if self.timeout_happened:
            print("timeout happend")
            self.player.participant.vars["timeouts"] += 1
            self.player.choice = random.choice([True, False])
        if np.random.rand() < self.player.ε:
            self.player.choice = not self.player.choice
            self.player.ε_happend = True


class GroupWaitPage(WaitPage):
    group_by_arrival_time = True
    title_text = 'Waiting for you to be matched with a new Participant'
    body_text = '''
        You have to wait until you can be matched with a new person for the next interaction. Remember
        that you are being paid an hourly wage of $7 for the time spent on this wait page.
    '''

    def is_displayed(self):
        if self.player.participant.vars["is_full"]:
            return False
        elif self.player.participant.vars["timeouts"] >= 3:
            return False
        elif self.round_number in self.session.vars["interaction_changes"] and self.round_number < self.session.vars["n_periods"]:
            return True
        else:
            return False

    def get_players_for_group(self, players):
        period = self.round_number
        print(self.session.vars["interaction_changes"])
        print(self.round_number)
        for p in players:
            if p.participant.vars["time_joined"] == 0:
                p.participant.vars["time_joined"] = time.time()

        players_to_return = []
        if len(players) >= 2:
            random.shuffle(players)
            p1 = players[0]

            p2 = next((p for p in players[1:] if p.participant.vars["uid"] != p1.participant.vars["opp_id"]), False)

            if p2 != False:
                print("Two new matched", p1.participant.vars["uid"], p2.participant.vars["uid"])
                players_to_return = [p1, p2]
                p1.participant.vars["opp_id"] = p2.participant.vars["uid"]
                p2.participant.vars["opp_id"] = p1.participant.vars["uid"]
                for p in players_to_return:
                    p.participant.vars["tot_wait_time"] += time.time() - p.participant.vars["time_joined"]
                    p.participant.vars["time_joined"] = 0
                    p.participant.vars["skip_to_next"] = False
                    p.participant.vars["interaction"] += 1
            elif len(players) == 2:
                if (time.time() - players[0].participant.vars["time_joined"]) > self.session.config["wait_to_skip"] and (time.time() - players[1].participant.vars["time_joined"]) > self.session.config["wait_to_skip"]:
                    for p in players:
                        p.participant.vars["tot_wait_time"] += time.time() - p.participant.vars["time_joined"]
                        p.participant.vars["time_joined"] = 0
                        p.participant.vars["skip_to_next"] = True
                        p.participant.vars["interaction"] += 1
                    players_to_return = players
                    print("Skipping next interaction")
                    print(p1.participant.vars["skip_to_next"])
                else:
                    print("Only two, not time to skip")
        elif self.session.vars["someone_has_passed"][self.round_number]:
            if (time.time() - players[0].participant.vars["time_joined"]) > self.session.config["wait_to_skip"]:
                p = players[0]
                p.participant.vars["tot_wait_time"] += time.time() - p.participant.vars["time_joined"]
                p.participant.vars["time_joined"] = 0
                p.participant.vars["skip_to_next"] = True
                p.participant.vars["interaction"] += 1
                players_to_return = players
                print("Skipping next interaction")
                print(p.participant.vars["skip_to_next"])
            else:
                print("Only one, not time to skip")
                print(time.time() - players[0].participant.vars["time_joined"])
                print(self.session.vars["someone_has_passed"])

        if len(players_to_return) > 0:
            self.session.vars["someone_has_passed"][self.round_number] = True
        return players_to_return




class ResultsWaitPage(WaitPage):
    title_text = 'Waiting for the other participant'
    body_text = '''
        The other participant has not yet made a decision. Remember
        that you are being paid an hourly wage of $7 for the time spent on this wait page.
    '''

    def is_displayed(self):
        if self.player.participant.vars["is_full"]:
            return False
        elif self.player.participant.vars["timeouts"] >= 3:
            return False
        elif self.player.participant.vars["opp_dropout"]:
            return False
        elif self.player.participant.vars["skip_to_next"]:
            return False
        elif self.round_number < self.session.vars["n_periods"]:
            return True
        else:
            return False

    def after_all_players_arrive(self):
        dropout = False
        players =self.group.get_players()
        for p in players:
            if p.participant.vars["timeouts"] >= 3:
                dropout = True
        if dropout:
            for p in players:
                p.participant.vars["opp_dropout"] = True
        self.group.set_payoff()




class Results(Page):
    def is_displayed(self):
        if self.player.participant.vars["is_full"]:
            return False
        elif self.player.participant.vars["timeouts"] >= 3:
            return False
        elif self.player.participant.vars["skip_to_next"]:
            return False
        elif self.round_number == self.session.vars["interaction_changes"][self.player.participant.vars["interaction"] + 1] - 1:
            return True
        else:
            return False

    def vars_for_template(self):
        inter = self.player.participant.vars["interaction"]
        start_round = self.session.vars["interaction_changes"][inter]

        prev_players = self.player.in_rounds(inter+1, self.round_number)
        cumulative_payoff = sum([p.payoff for p in prev_players])
        num_prev = len(prev_players)



        tot_payoff = self.player.participant.payoff
        # all_prev_players = self.player.in_all_rounds()
        # tot_payoff = sum([p.payoff for p in all_prev_players])
        return {
            "cumulative_payoff":cumulative_payoff,
            "tot_payoff":tot_payoff,
            "num_prev": num_prev,
            "self_a": self.player.participant.vars["self_a"],
            "opp_a": self.player.participant.vars["opp_a"],
            "payoff": self.player.participant.vars["payoff"],
            "opp_dropout": self.player.participant.vars["opp_dropout"]
        }

class LastPage(Page):
    def is_displayed(self):
        if self.player.participant.vars["is_full"]:
            return False
        elif self.player.participant.vars["timeouts"] >= 3:
            return False
        elif self.player.participant.vars["skip_to_next"]:
            return False
        # elif self.round_number == self.session.vars["interaction_changes"][-1]:
        elif self.round_number == Constants.num_rounds:
            return True
        else:
            return False

    def vars_for_template(self):
        inter = self.player.participant.vars["interaction"]
        start_round = self.session.vars["interaction_changes"][inter]

        prev_players = self.player.in_rounds(inter+1, self.round_number)
        cumulative_payoff = sum([p.payoff for p in prev_players])
        num_prev = len(prev_players)

        play_bonus = self.participant.payoff.to_real_world_currency(self.session)
        wait_bonus = round(min(self.player.participant.vars['tot_wait_time']*self.session.config['pay_for_waiting'], self.session.config['max_pay_for_waiting']),2)
        self.player.payoff = wait_bonus/self.session.config['real_world_currency_per_point']
        tot_bonus = self.participant.payoff.to_real_world_currency(self.session)
        # all_prev_players = self.player.in_all_rounds()
        # tot_payoff = sum([p.payoff for p in all_prev_players])
        tot_payoff = self.player.participant.payoff
        return {
            "cumulative_payoff":cumulative_payoff,
            "tot_payoff":tot_payoff,
            "num_prev": num_prev,
            "self_a": self.player.participant.vars["self_a"],
            "opp_a": self.player.participant.vars["opp_a"],
            "payoff": self.player.participant.vars["payoff"],
            'wait_bonus': wait_bonus,
            'play_bonus': play_bonus,
            'tot_bonus': tot_bonus
        }


class DropOutPage(Page):
    def is_displayed(self):
        if self.player.participant.vars["is_full"]:
            return False
        elif self.round_number == Constants.num_rounds and self.player.participant.vars["timeouts"] >= 3:
            print("Participant ", self.player.participant.vars["uid"], " failed more than three times and have been removed")
            return True
        else:
            return False

    def vars_for_template(self):
        return {
            "timeout": self.session.config["timeout"]
        }
page_sequence = [
    GroupWaitPage,
    Choice,
    ResultsWaitPage,
    Results,
    DropOutPage,
    LastPage
]
