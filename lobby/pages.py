from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class MyPage(Page):
    def is_displayed(self):
        if self.player.participant.vars['failed'] == True:
            return False
        else:
            return not self.player.participant.vars.get('done', False)


class FullLobbyPage(Page):
    def is_displayed(self):
        if self.session.vars['min_players_passed'] == True and self.round_number == 1:
            return True
        else:
            return False

class Instructions(MyPage):
    form_model = "player"
    # form_fields = ["q1", "q2", "q3", "q4"]
    form_fields = ["q1", "q2", "q3"]
    def vars_for_template(self):
        points_per_dollar = int(1/self.session.config['real_world_currency_per_point'])
        return {
            "points_per_dollar": points_per_dollar,
            "initial_points": self.session.config["initial_points"],
            'wait_to_skip': self.session.config['wait_to_skip'],
            'compensation_units': self.session.config['compensation_units'],
            'base': self.session.config["base_points"],
            'A_val': self.session.config["base_points"] - 1,
            'A_other': 4,
            "q1_label": "If choice A gets you {} points and the other participant {} points and you both choose A, what is the payoff you will receive?".format(self.session.config["base_points"] - 2, 5),
        }

    def before_next_page(self):
        super().before_next_page()
        base = self.session.config["base_points"]
        # if (self.player.q1 == base + 3) and (self.player.q2 == base) and (self.player.q3 == "20%") and (self.player.q4 == "25%"):
        if (self.player.q1 == base + 3) and (self.player.q2 == base) and (self.player.q3 == "20%"):
            self.player.participant.vars['done'] = True
        else:
            self.player.participant.vars['done'] = False
            # print(self.player.q1,self.player.q2,self.player.q3,self.player.q4)
            print(self.player.q1,self.player.q2,self.player.q3)
            if self.player.round_number == Constants.num_rounds:
                    self.player.participant.vars['failed'] = True

class FailPage(Page):
    def is_displayed(self):
        if self.player.participant.vars['failed'] == True:
            return True
        else:
            return False



page_sequence = [
    FullLobbyPage,
    Instructions,
    FailPage,
]
