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
    num_rounds = 10


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    disease_state = models.IntegerField(initial=1)
    ties = models.StringField()

    def get_id(self):
        return self.participant.id_in_session

    def get_player_with_current_settings(self):
        p = self
        # New player instances are generated for each round. Thus, if rounds have been played already,
        # the current disease state is stored in the previous player instance.
        if self.subsession.round_number > 1:
            p = self.in_round(self.subsession.round_number - 1)
        return p

    def change_disease_state(self):
        p = self.get_player_with_current_settings()
        if p.disease_state == 1:
            self.disease_state = 2
        elif p.disease_state == 2:
            self.disease_state = 3
        else:
            self.disease_state = 1

    def connect_to(self, other):
        p = self.get_player_with_current_settings()
        if other.get_id() == self.get_id():
            return
        if not p.ties:
            self.ties = str(other.get_id())
        elif str(other.get_id()) not in p.ties.split():
            self.ties = p.ties + " " + str(other.get_id())
        else:
            self.ties = p.ties

    def disconnect_from(self, other):
        p = self.get_player_with_current_settings()
        if not p.ties or other.get_id() == self.get_id():
            return
        elif str(other.get_id()) in p.ties.split():
            ties = p.ties.split()
            ties.remove(str(other.get_id()))
            self.ties = ' '.join(ties)
        else:
            self.ties = p.ties

    pass
