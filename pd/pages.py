from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import numpy as np
import time
import random

class Choice(Page):
    form_model = 'player'
    form_fields = ['choice']
    # timeout_seconds = 20

    def get_timeout_seconds(self):
        return self.session.config["timeout"]

    def is_displayed(self):
        i = self.player.participant.vars["interaction"]
        # self.player.ε = self.session.vars["epsilons"][i]
        self.player.δ = self.session.vars["deltas"][i]
        self.player.benefit = self.session.vars["benefits"][i]
        self.player.cost = self.session.vars["costs"][i]
        self.player.base = self.session.vars["bases"][i]
        if self.player.participant.vars["is_full"]:
            return False
        elif self.player.participant.vars["timeouts"] >= 3:
            return False
        elif self.player.participant.vars["skip_to_next"]:
            print("Skip happend in round", self.round_number)
            return False
        elif self.round_number < self.session.vars["n_periods"]:
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
                    "notδ": int(100 - self.player.δ*100),
                    # "ε": int(self.player.ε*100),
                    "round_in_interaction": round_in_interaction,
                    "tot_payoff": self.player.participant.payoff,
                    "base": self.session.config["base_points"],
                    "A_val": self.session.config["base_points"] - self.player.cost

            }
        else:
            return {
                    "first":  self.round_number in self.session.vars["interaction_changes"],
                    "self_a": self.player.participant.vars["self_a"],
                    "opp_a": self.player.participant.vars["opp_a"],
                    "payoff": self.player.participant.vars["payoff"],
                    "notδ": int(100 - self.player.δ*100),
                    "δ": int(self.player.δ*100),
                    # "ε": int(self.player.ε*100),
                    "round_in_interaction": round_in_interaction,
                    "tot_payoff": self.player.participant.payoff,
                    "base": int(self.session.config["base_points"]),
                    "A_val": int(self.session.config["base_points"] - self.player.cost)
            }

    def before_next_page(self):
        if self.timeout_happened:
            print("timeout happend", self.player.participant.vars["uid"])
            self.player.participant.vars["timeouts"] += 1
            print("Timeouts: ", self.player.participant.vars["timeouts"], " for player", self.player.participant.vars["uid"])
            if self.player.participant.vars["timeouts"] == 3:
                self.session.vars["n_active"] = self.session.vars["n_active"] - 1
            self.player.choice = random.choice([True, False])
            self.player.timeout = True
        else:
            self.player.timeout = False
        # if np.random.rand() < self.player.ε:
        #     self.player.choice = not self.player.choice
        #     self.player.ε_happend = True


class RoundResultsPage(Page):
    # timeout_seconds = 30
    def get_timeout_seconds(self):
        return self.session.config["timeout"]

    def is_displayed(self):
        if self.player.participant.vars["is_full"]:
            return False
        # elif self.player.participant.vars["timeouts"] >= 3:
        #     return False
        # elif self.player.participant.vars["opp_dropout"]:
        #     return False
        elif self.player.participant.vars["skip_to_next"]:
            print("Skip happend", self.round_number)
            return False
        elif self.round_number < self.session.vars["n_periods"]:
            return True
        else:
            return False

    def vars_for_template(self):
        inter = self.player.participant.vars["interaction"]
        start_round = self.session.vars["interaction_changes"][inter]
        round_in_interaction = self.round_number - start_round + 1
        last_round = self.round_number == (self.session.vars["interaction_changes"][self.player.participant.vars["interaction"] + 1] - 1)
        last_interaction = self.round_number == (self.session.vars["interaction_changes"][-1] - 1)
        prev_players = self.player.in_rounds(start_round, self.round_number)

        cumulative_payoff = sum([p.payoff for p in prev_players])
        num_prev = len(prev_players)

        self_a = self.player.participant.vars["self_a"]
        opp_a = self.player.participant.vars["opp_a"]
        id_choosen = self_a + opp_a
        return {
                "self_a": self.player.participant.vars["self_a"],
                "opp_a": self.player.participant.vars["opp_a"],
                "payoff": self.player.participant.vars["payoff"],
                "δ": int(self.player.δ*100),
                # "ε": int(self.player.ε*100),
                # "ε_happend": self.player.ε_happend,
                "comp_units": self.session.config["compensation_units"],
                "last_round": last_round,
                "last_interaction": last_interaction,
                "round_in_interaction": round_in_interaction,
                "opp_dropout": self.player.participant.vars["opp_dropout"],
                "tot_payoff": self.player.participant.payoff,
                "cumulative_payoff":cumulative_payoff,
                "num_prev": num_prev,
                "id_choosen": id_choosen,
                "base": int(self.session.config["base_points"]),
                "A_val": int(self.session.config["base_points"] - self.player.cost)
        }

    def before_next_page(self):
        if self.player.participant.vars["opp_dropout"]:
            self.player.participant.vars["skip_to_next"] = True
            self.player.participant.vars["opp_dropout"] = False
            self.player.payoff = self.session.config["compensation_units"]



class ResultsWaitPage(WaitPage):
    title_text = 'Waiting for the other participant to take an action'
    body_text = '''
        The other participant has not yet made a decision. Remember
        that you are being paid an hourly wage of $7 for the time spent on this wait page.
    '''

    def is_displayed(self):
        if self.player.participant.vars["is_full"]:
            return False
        # elif self.player.participant.vars["timeouts"] >= 3:
        #     return False
        # elif self.player.participant.vars["opp_dropout"]:
        #     return False
        elif self.player.participant.vars["skip_to_next"]:
            return False
        elif self.round_number < self.session.vars["n_periods"]:
            return True
        else:
            return False

    def after_all_players_arrive(self):
        dropout = False
        timeout = False
        players =self.group.get_players()
        for p in players:
            p.opp_timeout = False
            p.opp_dropout = False
            if p.participant.vars["timeouts"] >= 3:
                dropout = True
                p.participant.vars["skip_to_next"] = True
            if p.timeout:
                timeout = True

        if dropout:
            for p in players:
                p.participant.vars["opp_dropout"] = True
                if p.participant.vars["timeouts"] < 3:
                    p.opp_dropout = True
        if timeout:
            for p in players:
                if p.timeout == False:
                    p.opp_timeout = True

        self.group.set_payoff()




class GroupWaitPage(WaitPage):
    group_by_arrival_time = True
    title_text = 'Waiting for you to be matched with a new worker'
    body_text = '''
        You have to wait until you can be matched with a new worker for the next interaction. Remember
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
        if period > 80:
            self.session.vars["experiment_done"] = True
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
                    p.wait_time = time.time() - p.participant.vars["time_joined"]
                    p.participant.vars["tot_wait_time"] += time.time() - p.participant.vars["time_joined"]
                    p.participant.vars["time_joined"] = 0
                    p.participant.vars["skip_to_next"] = False
                    p.participant.vars["interaction"] += 1
                    self.session.vars["n_passed"][self.round_number] += 1
            elif p2 == False and (len(players) + self.session.vars["n_passed"][self.round_number]  == self.session.vars["n_active"]):
                for p in players:
                    p.wait_time = time.time() - p.participant.vars["time_joined"]
                    p.participant.vars["tot_wait_time"] += time.time() - p.participant.vars["time_joined"]
                    p.participant.vars["time_joined"] = 0
                    p.participant.vars["skip_to_next"] = True
                    p.participant.vars["interaction"] += 1
                    print(p.participant.vars["skip_to_next"])
                    self.session.vars["n_passed"][self.round_number] += len(players)
                players_to_return = players
                print("Skipping next interaction")
            #     if (time.time() - p1.participant.vars["time_joined"]) > self.session.config["wait_to_skip"]:
            #
            else:
                print("Only two, max wait time", max([time.time() - p.participant.vars["time_joined"] for p in players]))
        if self.session.vars["someone_has_passed"][self.round_number] and len(players_to_return) == 0:
            if (time.time() - players[0].participant.vars["time_joined"]) > self.session.config["wait_to_skip"] or 1 + self.session.vars["n_passed"][self.round_number] == self.session.vars["n_active"]:
                p = players[0]
                p.wait_time = time.time() - p.participant.vars["time_joined"]
                p.participant.vars["tot_wait_time"] += time.time() - p.participant.vars["time_joined"]
                p.participant.vars["time_joined"] = 0
                p.participant.vars["skip_to_next"] = True
                p.participant.vars["interaction"] += 1
                players_to_return = [p]
                self.session.vars["n_passed"][self.round_number] += len(players_to_return)
                print("Skipping next interaction")
                print(p.participant.vars["skip_to_next"])
            else:
                print("Only one, not time to skip")
                print(time.time() - players[0].participant.vars["time_joined"])
                print(max([time.time() - p.participant.vars["time_joined"] for p in players]))
                print(self.session.vars["someone_has_passed"])

        if self.session.vars["n_active"] == 1:
            p = players[0]
            p.wait_time = time.time() - p.participant.vars["time_joined"]
            p.participant.vars["tot_wait_time"] += time.time() - p.participant.vars["time_joined"]
            p.participant.vars["time_joined"] = 0
            p.participant.vars["skip_to_next"] = True
            p.participant.vars["interaction"] += 1
            players_to_return = players

        if len(players_to_return) > 0:
            print("interaction number ", players_to_return[0].participant.vars["interaction"])
            print("interaction frist round ",  self.session.vars["interaction_changes"][players_to_return[0].participant.vars["interaction"]])
            print("Round number ", self.round_number)
            self.session.vars["someone_has_passed"][self.round_number] = True
        return players_to_return



class LastPage(Page):
    def is_displayed(self):
        if self.player.participant.vars["is_full"]:
            return False
        elif self.player.participant.vars["timeouts"] >= 3:
            return False
        elif self.player.participant.vars["skip_to_next"] and self.round_number < Constants.num_rounds:
            return False
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
        print("tot_bonus", tot_bonus)
        print("wait_bonus", wait_bonus)
        print("play_bonus", play_bonus)
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
        # elif self.round_number == Constants.num_rounds and self.player.participant.vars["timeouts"] >= 3:
        elif self.player.participant.vars["timeouts"] >= 3:
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
    RoundResultsPage,
    DropOutPage,
    LastPage
]
