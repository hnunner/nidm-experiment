from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Questionnaire(Page):
    timeout_seconds = 1
    form_model = 'player'
    form_fields = [
        'risk_perception'
    ]

    def before_next_page(self):
        print("risk perception: ", self.player.risk_perception)
        self.participant.vars['risk_perception'] = self.player.risk_perception
        self.session.vars['disease_introduced'] = False

    pass


page_sequence = [
    Questionnaire
]
