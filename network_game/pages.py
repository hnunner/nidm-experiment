from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from random import randint


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass


class Game(Page):

    timeout_seconds = 5

    def before_next_page(self):
        self.player.compute_disease_transmission()

        if not self.session.vars['disease_introduced'] and self.round_number == 1:
            random_player = self.group.get_player_by_id(randint(1, len(self.group.get_players())))
            random_player.infect()
            print("randomly selected player " + str(random_player.id_in_group) + " infected")
            self.session.vars['disease_introduced'] = True

        if randint(1, 10) > 3:
            self.player.connect_to(self.group.get_player_by_id(randint(1, len(self.group.get_players()))))
        else:
            self.player.disconnect_from(self.group.get_player_by_id(randint(1, len(self.group.get_players()))))

    def js_vars(self):
        disease_states = dict()
        risk_perceptions = dict()
        ties = dict()
        for player in self.subsession.get_players():
            round_number = self.subsession.round_number
            p = player.in_round(round_number)
            if round_number > 1:
                p = player.in_round(round_number-1)
            disease_states[player.id_in_group] = p.disease_state
            risk_perceptions[player.id_in_group] = p.participant.vars['risk_perception']
            if not p.ties:
                ties[player.id_in_group] = ""
            else:
                ties[player.id_in_group] = p.ties.split()

        return dict(
            p_id=self.participant.id_in_session,
            disease_states=disease_states,
            risk_perceptions=risk_perceptions,
            ties=ties
        )

    pass


page_sequence = [
    ResultsWaitPage,
    Game
]
