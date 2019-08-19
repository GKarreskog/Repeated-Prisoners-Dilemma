from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class MyPage(Page):
    def is_displayed(self):
        if self.player.participant.vars['failed'] == True:
            return False
        else:
            return not self.player.participant.vars.get('done', False)

class Instructions(MyPage):
    def vars_for_template(self):
        points_per_dollar = int(1/self.session.config['real_world_currency_per_point'])
        return {
            "points_per_dollar": points_per_dollar,
            "initial_points": self.settings.config["initial_points"],
            'wait_to_skip': self.settings.config['wait_to_skip'],
            'compensation_units': self.settings.config['compensation_units']
        }




page_sequence = [
    MyPage,
    Instructions
]
