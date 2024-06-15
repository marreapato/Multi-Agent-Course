import random
import matplotlib.pyplot as plt
import networkx as nx
import os
from natsort import natsorted
import imageio
from agentpy import Agent, Model
import numpy as np

class OpinionAgent(Agent):
    def setup(self, theme='default'):
        self.opinion = -1
        self.influence = self.set_init_opinion_inf(theme)  # Influência base do agente ajustada pelo tema
        self.mailbox = []  # Caixa de entrada para mensagens

    def set_init_opinion_inf(self, theme):
        op_distributions = {
            'default': np.random.normal,
            'politics': lambda: np.random.normal(loc=-1, scale=1),
            'health': lambda: np.random.normal(loc=0.5, scale=0.5),
            'movies': lambda: np.random.normal(loc=-0.5, scale=0.5),
            # Add more themes and their distributions here
        }
        if theme in op_distributions:
            return op_distributions[theme]()
        else:
            return op_distributions['default']()

    def interact(self):
        if hasattr(self, 'neighbors') and self.neighbors:
            neighbor_id = random.choice(self.neighbors)  # Escolhe um vizinho aleatoriamente
            self.send_message(neighbor_id)

    def send_message(self, recipient_id):
        message = {
            'sender': self.id,
            'opinion': self.opinion,
            'influence': self.influence
        }
        self.model.agents[recipient_id].receive_message(message)

    def receive_message(self, message):
        self.mailbox.append(message)

    def process_mailbox(self):
        while self.mailbox:
            message = self.mailbox.pop(0)
            self.update_opinion(message)

    def update_opinion(self, message):
        influence_factor = message['influence']
        sender_opinion = message['opinion']
        self.opinion += influence_factor * (sender_opinion - self.opinion)
        self.opinion = max(min(self.opinion, 1), -1)  # Mantém a opinião dentro do intervalo [-1, 1]
