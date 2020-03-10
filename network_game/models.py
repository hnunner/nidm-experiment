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
from random import uniform


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'network_game'
    players_per_group = 12
    num_rounds = 100
    gamma = 0.4
    tau = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    ties = models.StringField()
    ties_form_req_options = models.StringField(blank=True)
    ties_form_res_options = models.StringField(blank=True)
    ties_rem_options = models.StringField(blank=True)
    ties_form_req_selected = models.StringField(blank=True)
    ties_form_res_selected = models.StringField(blank=True)
    ties_rem_selected = models.StringField(blank=True)

    disease_state = models.IntegerField(initial=1)
    rounds_infected = models.IntegerField(initial=0)

    def get_player_with_current_settings(self):
        p = self
        # New player instances are generated for each round. Thus, if rounds have been played already,
        # the current disease state is stored in the previous player instance.
        if self.subsession.round_number > 1:
            p = self.in_round(self.subsession.round_number - 1)
        return p

    def get_id(self):
        return self.participant.id_in_session

    def is_infected(self):
        return self.disease_state == 2

    def get_infected_ties(self):
        p = self.get_player_with_current_settings()
        infected = list()
        if p.ties:
            for other_id in p.ties.split():
                other = self.group.get_player_by_id(other_id)
                if other.is_infected():
                    infected.append(other)
        return infected

    def compute_disease_transmission(self):
        p = self.get_player_with_current_settings()
        if p.disease_state == 1:
            n_infected = len(self.get_infected_ties())
            if uniform(0, 1) <= 1 - pow(1 - Constants.gamma, n_infected):
                self.disease_state = 2
            else:
                self.disease_state = 1
        elif p.disease_state == 2:
            self.rounds_infected = p.rounds_infected + 1
            print("agent " + str(p.get_id()) + " infected for " + str(self.rounds_infected) + " rounds")
            if self.rounds_infected >= Constants.tau:
                self.disease_state = 3
            else:
                self.disease_state = 2
        else:
            self.disease_state = 3

    def infect(self):
        self.disease_state = 2

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
