from typing import Dict, List, Tuple
from clients import BaseClient
from . import BaseMethod


class MTVRP(BaseMethod):
    def __init__(self, clients: int, trips: int, capacity: int, demands: List[int], service_time: List[int],
                 client_positions: List[BaseClient]):
        super().__init__(clients, trips, capacity, demands, service_time)
        self.client_positions = client_positions

    def run(self) -> tuple:
        clients = self.client_positions
        deposit = clients.pop(0)

        # Start at Deposit
        current: BaseClient = deposit

        trips = 1
        distances: Dict[int, List[Tuple[int, float]]] = {}
        capacity = self.capacity
        while len(clients) > 0:
            k = trips - 1

            # Sort clients by distance to current position
            clients = sorted(clients, key=lambda c: current.distance_to(c))

            # Specify that the next travel position is the client with lower distance
            next: BaseClient = clients[0]

            prev_capacity = capacity
            capacity -= next.demand

            self.report(
                current.name + '\t->\t' + next.name +
                '\t|\tCapacity: ' + str(prev_capacity) + ' - ' + str(next.demand) +
                ' -> ' + str(capacity) + ' ' + ('✔️' if capacity >= 0 else '❌')
            )

            # If vehicle didn't exceed stock, remove client from pending list
            if capacity >= 0:
                if k not in distances:
                    distances[k] = []

                distances[k].append((len(clients), current.distance_to(next)))

                current = clients.pop(0)

            # If vehicle has no more stock, make a trip back to deposit and recalculate next route
            if capacity <= 0:
                # Exceeds stock, maybe we could try to extra look for other client
                if capacity < 0:
                    # Restore demand to look somewhere else
                    # Need to use 'next' because 'current' may or not be removed from list
                    capacity += next.demand

                    clients = sorted(clients, key=lambda c: (current.distance_to(c), c.demand))
                    for candidate in clients:
                        virtual_capacity = capacity - candidate.demand
                        if virtual_capacity >= 0:
                            prev_capacity = capacity
                            capacity = virtual_capacity
                            self.report(
                                current.name + '\t->\t' + candidate.name +
                                '\t|\tCapacity: ' + str(prev_capacity) + ' - ' + str(candidate.demand) +
                                ' -> ' + str(capacity) + ' ' + ('✔️' if capacity >= 0 else '❌')
                            )
                            distances[k].append((len(clients), current.distance_to(candidate)))
                            clients.remove(candidate)
                            current = candidate

                if len(clients) > 0:
                    distances[k].append((len(clients), current.distance_to(deposit)))

                trips += 1
                capacity = self.capacity
                self.report(current.name + '\t->\t' + deposit.name + '\n')
                current = deposit

        total_distance = 0
        for i in range(0, trips):
            for remaining, distance in distances[i]:
                total_distance += (trips - 1 - i + remaining) * distance

        return trips, total_distance
