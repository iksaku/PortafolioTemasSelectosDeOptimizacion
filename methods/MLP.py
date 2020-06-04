from typing import List
from clients import ClientWithDistance
from . import BaseMethod


class MLP(BaseMethod):
    def __init__(self, clients: int, trips: int, capacity: int, demands: List[int], service_time: List[int],
                 travel_times: List[ClientWithDistance]):
        super().__init__(clients, trips, capacity, demands, service_time)
        self.travel_times = travel_times

    def run(self):
        pass
