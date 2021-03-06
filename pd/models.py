from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import numpy as np
import random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'Repeated_interaction'
    players_per_group = 2
    num_rounds = 100


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            # treatments = []
            # δ_list = [0.5, 0.6, 0.7, 0.8]
            # δ_list = [1/2, 2/3, 3/4, 4/5, 5/6]
            # δ_list = [3/4]
            # δ_list = [round(δ,2) for δ in δ_list]
            δ = 0.75
            # ε_list = [0., 0.05, 0.1]
            # ε_list = [0.0, 0.05, 0.1, 0.15]
            # l = g = c/(b - c)
            # this results in possible l ∈
            # gives
            # c_list = [0,1,2,3,4]
            c_list = [2]
            c = 2
            bc_list = [1,4,6]



            if self.session.config["treatment"] == 1:
                bc_list = [1,1,1,1,3,3,3,3,6,6,6,6]
            elif self.session.config["treatment"] == 2:
                bc_list = [6,6,6,6,3,3,3,3,1,1,1,1]
            elif self.session.config["treatment"] == 3:
                bc_list = [3,6,1,6,1,6,1,3,1,3,6,3]
            else:
                bc_list = [3,6,1,6,1,6,1,3,1,3,6,3]


            done = False
            while not done:
                deltas = []
                epsilons = []
                costs = []
                benefits = []
                bases = []
                interaction_changes = []
                round_count = 1
                interaction_changes.append(round_count)
                for i in range(len(bc_list)):
                    cost = c
                    bc = bc_list[i]
                    benefit = cost + bc
                    base = self.session.config["base_points"]
                    round_count += np.random.geometric(1-δ)
                    deltas.append(δ)
                    interaction_changes.append(round_count)
                    benefits.append(benefit)
                    costs.append(cost)
                    bases.append(base)
                # ε = random.choice(ε_list)
                if round_count < Constants.num_rounds:
                    done = True


            self.session.vars["deltas"] = deltas
            self.session.vars["interaction_changes"] = interaction_changes
            self.session.vars["epsilons"] = epsilons
            self.session.vars["benefits"] = benefits
            self.session.vars["costs"] = costs
            self.session.vars["bases"] = bases
            self.session.vars["n_periods"] = interaction_changes[-1]
            self.session.vars["someone_has_passed"] = {i:False for i in interaction_changes}
            self.session.vars["n_passed"] = {i:0 for i in interaction_changes}
            # self.session.vars["n_active"] = self.session.config["min_players_start"]


            # self.session.vars["num_passed"] = [0]*(Constants.num_rounds+2) ## Todo: find right value






class Group(BaseGroup):
    def set_payoff(self):
        players = self.get_players()
        players[0].opp_choice = players[1].choice
        players[1].opp_choice = players[0].choice
        players[0].set_payoff()
        players[1].set_payoff()


class Player(BasePlayer):
    benefit = models.FloatField()
    cost = models.FloatField()
    δ = models.FloatField()
    base = models.FloatField()
    treatment = models.IntegerField()
    interaction = models.IntegerField()
    timeout = models.BooleanField()
    opp_timeout = models.BooleanField()
    opp_dropout = models.BooleanField()
    choice = models.BooleanField(
        choices=[
            [True, 'A'],
            [False, 'B'],],
            widget=widgets.RadioSelect
        )
    # ε_happend = models.BooleanField(initial=False)
    opp_choice = models.BooleanField()
    played = models.BooleanField(initial=False)
    # join_time = models.FloatField(initial=0)
    wait_time = models.FloatField(initial=0)

    def set_payoff(self):
        self.played = True
        self.interaction = self.participant.vars["interaction"]
        self.payoff += self.base
        if self.choice:
            self.payoff += -self.cost
            self.participant.vars["self_a"] = "A"
        else:
            self.participant.vars["self_a"] = "B"
        if self.opp_choice:
            self.payoff += self.benefit
            self.participant.vars["opp_a"] = "A"
        else:
            self.participant.vars["opp_a"] = "B"

        self.participant.vars["payoff"] = self.payoff
