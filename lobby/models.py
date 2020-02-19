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

    # q1 = models.IntegerField(choices=[sum - 3,sum-2,sum-1,sum,sum+1], widget=widgets.RadioSelect)
    # q2 = models.IntegerField(choices=[base-3,base-2,base,base+1,base+base,base+4], widget=widgets.RadioSelect)
    q1 = models.IntegerField(widget=widgets.RadioSelect)
    q2 = models.IntegerField(widget=widgets.RadioSelect)
    # q2 = models.IntegerField(choices=[base-1,base,base+1,base+2,base+3,base+base], widget=widgets.RadioSelect)
    q3 = models.StringField(choices=["90%","80%","30%","20%"], widget=widgets.RadioSelect)
    # q4 = models.StringField(choices=["50%", "75%", "25%", "30%"], widget=widgets.RadioSelect)


    def q1_choices(self):
        base = self.session.config["base_points"]
        A_val = base - 1
        A_other = 4
        sum = A_val + A_other
        return [sum - 3,sum-2,sum-1,sum,sum+1]

    def q2_choices(self):
        base = self.session.config["base_points"]
        return [base-3,base-2,base,base+1,base+base,base+4]
