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
    num_rounds = 50


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            δ_list = [0.5, 0.7, 0.8, 0.9]
            # ε_list = [0., 0.05, 0.1]
            ε_list = [0.0, 0.05, 0.1, 0.15]
            c_list = [1,2,3,4]
            b_list = [5,6,7,8]
            done = False
            deltas = []
            epsilons = []
            costs = []
            benefits = []
            interaction_changes = []
            round_count = 1
            interaction_changes.append(round_count)
            while not done:
                δ = random.choice(δ_list)
                ε = random.choice(ε_list)
                benefit = random.choice(b_list)
                cost = random.choice(c_list)


                round_count += np.random.geometric(1-δ)
                if round_count > Constants.num_rounds:
                    done = True
                else:
                    epsilons.append(ε)
                    deltas.append(random.choice(δ_list))
                    interaction_changes.append(round_count)
                    benefits.append(benefit)
                    costs.append(cost)

            self.session.vars["deltas"] = deltas
            self.session.vars["interaction_changes"] = interaction_changes
            self.session.vars["epsilons"] = epsilons
            self.session.vars["benefits"] = benefits
            self.session.vars["costs"] = costs
            self.session.vars["n_periods"] = interaction_changes[-1]
            self.session.vars["someone_has_passed"] = {i:False for i in interaction_changes}


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
    ε = models.FloatField()
    δ = models.FloatField()
    choice = models.BooleanField(
        choices=[
            [True, 'A'],
            [False, 'B'],],
            widget=widgets.RadioSelect
        )
    ε_happend = models.BooleanField(initial=False)
    opp_choice = models.BooleanField()
    played = models.BooleanField(initial=False)
    join_time = models.FloatField(initial=0)

    def set_payoff(self):
        self.played = True
        self.payoff += 0
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
