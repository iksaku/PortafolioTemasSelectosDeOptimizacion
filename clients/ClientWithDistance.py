from __future__ import annotations
from typing import List
from . import BaseClient


class ClientWithDistance(BaseClient):
    def __init__(self, id: int, demand: int, distances: List[int]):
        super().__init__(id, demand)
        self.distances = distances

    def distance_to(self, client: ClientWithDistance):
        return self.distances[client.id] if self.id is not client.id else None
