from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import numpy as np
import time
import random

class Choice(Page):
    form_model = 'player'
    form_fields = ['choice']

    def is_displayed(self):

        if self.player.participant.vars["skip_to_next"]:
            print("Skip happend")
            return False
        elif self.round_number < self.session.vars["n_periods"]:
            i = self.player.participant.vars["interaction"]
            print("interaction number ", i)
            print(self.session.vars["epsilons"])
            self.player.ε = self.session.vars["epsilons"][i]
            self.player.δ = self.session.vars["deltas"][i]
            self.player.benefit = self.session.vars["benefits"][i]
            self.player.cost = self.session.vars["costs"][i]
            return True
        else:
            return False

class GroupWaitPage(WaitPage):
    group_by_arrival_time = True
    title_text = 'Waiting for you to be matched with a new Participant'
    body_text = '''
        You have to wait until you can be matched with a new person for the next interaction. Remember
        that you are being paid an hourly wage of $7 for the time spent on this wait page.
    '''

    def is_displayed(self):
        if self.round_number in self.session.vars["interaction_changes"] and self.round_number < self.session.vars["n_periods"]:
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
                    p.participant.vars["tot_wait_time"] += time.time() - p.participant.vars["time_joined"]
                    p.participant.vars["time_joined"] = 0
                    p.participant.vars["skip_to_next"] = False
                    p.participant.vars["interaction"] += 1
            elif len(players) == 2:
                if (time.time() - players[0].participant.vars["time_joined"]) > self.session.config["wait_to_skip"] and (time.time() - players[1].participant.vars["time_joined"]) > self.session.config["wait_to_skip"]:
                    for p in players:
                        p.participant.vars["tot_wait_time"] += time.time() - p.participant.vars["time_joined"]
                        p.participant.vars["time_joined"] = 0
                        p.participant.vars["skip_to_next"] = True
                        p.participant.vars["interaction"] += 1
                    players_to_return = players
                    print("Skipping next interaction")
                    print(p1.participant.vars["skip_to_next"])
                else:
                    print("Only two, not time to skip")
                
        return players_to_return

            
    

class ResultsWaitPage(WaitPage):
    title_text = 'Waiting for the other participant'
    body_text = '''
        The other participant has not yet made a decision. Remember
        that you are being paid an hourly wage of $7 for the time spent on this wait page.
    '''

    def is_displayed(self):
        if self.player.participant.vars["skip_to_next"]:
            return False
        elif self.round_number < self.session.vars["n_periods"]:
            return True
        else:
            return False

    def after_all_players_arrive(self):
        self.group.set_payoff()
    
        


class Results(Page):
    def is_displayed(self):
        if self.player.participant.vars["skip_to_next"]:
            return False
        elif self.round_number == self.session.vars["interaction_changes"][self.player.participant.vars["interaction"] + 1] - 1:
            return True
        else:
            return False
    
    def vars_for_template(self):
        prev_players = self.player.in_all_rounds()
        cumulative_payoff = sum([p.payoff for p in prev_players])
        tot_payoff = sum([p.payoff for p in prev_players])
        num_prev = len(prev_players)

        return {
            "cumulative_payoff":cumulative_payoff, 
            "tot_payoff":tot_payoff, 
            "num_prev": num_prev
        }



page_sequence = [
    GroupWaitPage,
    Choice,
    ResultsWaitPage,
    Results
]
