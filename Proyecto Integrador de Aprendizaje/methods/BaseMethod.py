from typing import List


class BaseMethod:
    def __init__(self, clients: int, trips: int, capacity: int, demands: List[int], service_time: List[int]):
        self.clients = clients
        self.trips = trips
        self.capacity = capacity
        self.demands = demands
        self.service_time = service_time
        self._report = ''

    def report(self, line: str, new_line: bool = True):
        if new_line:
            self._report += '\n'
        self._report += line

    def get_report(self) -> str:
        return self._report

    def run(self) -> tuple:
        pass
