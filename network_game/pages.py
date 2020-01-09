from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Questionnaire(Page):
    form_model = 'player'
    form_fields = [
        'disease_state',

        # 'male',
        # 'earnings',
        # 'height',
        # 'risk_perception',
        # 'name',
        # 'comments'
    ]
    pass


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass


class Game(Page):

    def js_vars(self):
        disease_states = dict();
        for player in self.subsession.get_players():
            disease_states[player.id_in_group] = player.disease_state

        return dict(
            p_id=self.participant.id_in_session,
            disease_states=disease_states,
        )

    pass


class Results(Page):
    pass


page_sequence = [
    Questionnaire,
    ResultsWaitPage,
    Game,
    Results
]
