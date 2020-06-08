from __future__ import annotations
from . import BaseClient
import math


class ClientWithPosition(BaseClient):
    def __init__(self, id: int, demand: int, x: int, y: int):
        super().__init__(id, demand)
        self.x = x
        self.y = y

    def distance_to(self, client: ClientWithPosition):
        return math.sqrt(
            math.pow(self.x - client.x, 2) + math.pow(self.y - client.y, 2)
        )
