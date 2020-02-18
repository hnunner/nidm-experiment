from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from random import randint


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass


class Game(Page):
    # timeout_seconds = 20
    form_model = 'player'
    form_fields = [
        'ties_form_req_options',
        'ties_form_res_options',
        'ties_rem_options',
        'ties_form_req_selected',
        'ties_form_res_selected',
        'ties_rem_selected'
    ]

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
        ties = dict()
        ties_form_req_options = dict()
        ties_form_res_options = dict()
        ties_rem_options = dict()

        disease_states = dict()
        risk_perceptions = dict()

        for player in self.subsession.get_players():
            round_number = self.subsession.round_number
            p = player.in_round(round_number)
            if round_number > 1:
                p = player.in_round(round_number-1)

            if not p.ties:
                ties[player.id_in_group] = ""
            else:
                ties[player.id_in_group] = p.ties.split()

            # if not p.ties_form_req_options:
            #     ties_form_req_options[player.id_in_group] = ""
            # else:
            #     ties_form_req_options[player.id_in_group] = p.ties_form_req_options.split()
            if player.id_in_group == 1:
                ties_form_req_options[player.id_in_group] = "3 6 9".split()
            else:
                ties_form_req_options[player.id_in_group] = "1 3 12 34".split()

            # if not p.ties_form_res_options:
            #     ties_form_res_options[player.id_in_group] = ""
            # else:
            #     ties_form_res_options[player.id_in_group] = p.ties_form_res_options.split()
            if player.id_in_group == 1:
                ties_form_res_options[player.id_in_group] = "".split()
            else:
                ties_form_res_options[player.id_in_group] = "24 28".split()

            # if not p.ties_rem_options:
            #     ties_rem_options[player.id_in_group] = ""
            # else:
            #     ties_rem_options[player.id_in_group] = p.ties_rem_options.split()
            if player.id_in_group == 1:
                ties_rem_options[player.id_in_group] = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 " \
                                                       "16 17 18 19 20 21 22 23".split()
            else:
                ties_rem_options[player.id_in_group] = "3 5".split()

            disease_states[player.id_in_group] = p.disease_state
            risk_perceptions[player.id_in_group] = p.participant.vars['risk_perception']

        return dict(
            p_id=self.participant.id_in_session,
            ties=ties,
            ties_form_req_options=ties_form_req_options,
            ties_form_res_options=ties_form_res_options,
            ties_rem_options=ties_rem_options,
            disease_states=disease_states,
            risk_perceptions=risk_perceptions
        )

    pass


page_sequence = [
    ResultsWaitPage,
    Game
]
