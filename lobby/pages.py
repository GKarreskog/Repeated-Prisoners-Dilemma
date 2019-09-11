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
    form_model = "player"
    form_fields = ["q1", "q2", "q3", "q4"]
    def vars_for_template(self):
        points_per_dollar = int(1/self.session.config['real_world_currency_per_point'])
        return {
            "points_per_dollar": points_per_dollar,
            "initial_points": self.session.config["initial_points"],
            'wait_to_skip': self.session.config['wait_to_skip'],
            'compensation_units': self.session.config['compensation_units']
        }

    def before_next_page(self):
        super().before_next_page()
        if (self.player.q1 == 3) and (self.player.q2 == 0) and (self.player.q3 == "25%") and (self.player.q4 == "10%"):
            self.player.participant.vars['done'] = True
        else:
            self.player.participant.vars['done'] = False
            if self.player.round_number == Constants.num_rounds:
                    self.player.participant.vars['failed'] = True

class FailPage(Page):
    def is_displayed(self):
        if self.player.participant.vars['failed'] == True:
            return True
        else:
            return False



page_sequence = [
    Instructions,
    FailPage,
]
