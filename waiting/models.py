from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'waiting'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            self.session.vars["min_players_passed"] = False
            self.session.vars["timeout"] = False
            self.session.vars["experiment_done"] = False
            self.session.vars["n_active"] = self.session.config["min_players_start"]

            id = 1
            for p in self.get_players():
                p.payoff = 50
                p.participant.vars["is_full"] = False
                p.participant.vars["time_joined"] = 0
                p.participant.vars["interaction"] = -1
                p.participant.vars["tot_wait_time"] = 0
                p.participant.vars["skip_to_next"] = False
                p.participant.vars["timeout"] = False
                p.participant.vars["uid"] = id
                p.participant.vars["opp_id"] = 0
                p.participant.vars["timeouts"] = 0
                p.participant.vars["opp_dropout"] = False
                id += 1


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    wait_time = models.FloatField()
