from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import numpy as np 


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'Repeated_interaction'
    players_per_group = 2
    num_rounds = 10


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            δ = 0.2
            num_interactions = self.session.config["num_interactions"]
            deltas = []
            epsilons = []
            costs = []
            benefits = []
            interaction_changes = []
            round_count = 1
            i = 0
            while i < num_interactions:
                epsilons.append(0.1)
                deltas.append(δ)
                interaction_changes.append(round_count)
                benefits.append(4)
                costs.append(1)
                round_count += np.random.geometric(1-δ)
                i += 1
                # if round_count > Constants.num_rounds:
                if round_count > Constants.num_rounds:
                    i = 0
                    deltas = []
                    epsilons = []
                    costs = []
                    benefits = []
                    interaction_changes = []
                    round_count = 1
            interaction_changes.append(round_count)

            
            self.session.vars["deltas"] = deltas
            self.session.vars["interaction_changes"] = interaction_changes
            self.session.vars["epsilons"] = epsilons
            self.session.vars["benefits"] = benefits
            self.session.vars["costs"] = costs
            self.session.vars["n_periods"] = interaction_changes[-1]
            

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
        [False, 'B'],
    ], 
    widget=widgets.RadioSelect
)
    opp_choice = models.BooleanField()
    played = models.BooleanField(initial=False)
    join_time = models.FloatField(initial=0)

    def set_payoff(self):
        self.played = True
        self.payoff = 0
        if self.choice:
            self.payoff += -self.cost
        if self.opp_choice:
            self.payoff += self.benefit


