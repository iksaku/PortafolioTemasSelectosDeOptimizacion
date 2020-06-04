from __future__ import annotations
from . import BaseClient
import math


class ClientWithPosition(BaseClient):
    def __init__(self, id: int, demand: int, x: int, y: int):
        super().__init__(id, demand)
        self.x = x
        self.y = y

    def distance_to(self, client: ClientWithPosition):
        return math.sqrt(abs((self.x - client.x) + (self.y - client.y)))