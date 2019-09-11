from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'lobby'
    players_per_group = None
    num_rounds = 10


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            for p in self.get_players():
                p.participant.vars["failed"] = False



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q1 = models.IntegerField(choices=[-1,0,1,2,3,4], widget=widgets.RadioSelect)
    q2 = models.IntegerField(choices=[-1,0,1,2,3,4], widget=widgets.RadioSelect)
    q3 = models.StringField(choices=["75%","50%","25%","100%"], widget=widgets.RadioSelect)
    q4 = models.StringField(choices=["10%", "90%", "80%", "20%"], widget=widgets.RadioSelect)

