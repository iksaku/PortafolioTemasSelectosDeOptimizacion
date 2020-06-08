from __future__ import annotations
from abc import ABCMeta, abstractmethod


class BaseClient(metaclass=ABCMeta):
    def __init__(self, id: int, demand: int):
        self.demand = demand
        self.id = id
        self.name = 'Client ' + str(self.id) if self.id > 0 else 'Deposit\t'

    @abstractmethod
    def distance_to(self, client: BaseClient) -> float:
        pass
