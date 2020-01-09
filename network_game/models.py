from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'network_game'
    players_per_group = 4
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # possible fields
    disease_state = models.IntegerField(
        choices=[
            [1, "susceptible"],
            [2, "infected"],
            [3, "recovered"],
        ]
    )
    # male = models.BooleanField()
    # earnings = models.CurrencyField(initial=0)
    # height = models.IntegerField(min=100, max=220, initial=150)
    # risk_perception = models.FloatField(min=0.0, max=2.0, initial=1.0)
    # name = models.StringField()
    # comments = models.LongStringField()

    pass
