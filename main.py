from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Tuple
import math
import os
import re
import time


class Client:
    def __init__(self, id: int, demand: int):
        self.demand = demand
        self.id = id
        self.name = 'Client ' + str(self.id) if self.id > 0 else 'Deposit\t'


class ClientWithPosition(Client):
    def __init__(self, id: int, demand: int, x: int, y: int):
        super().__init__(id, demand)
        self.x = x
        self.y = y

    def distance_to(self, client: ClientWithPosition):
        return math.sqrt(abs((self.x - client.x) + (self.y - client.y)))


class ClientWithDistance(Client):
    def __init__(self, id: int, demand: int, distances: List[int]):
        super().__init__(id, demand)
        self.distances = distances

    def distance_to(self, client: ClientWithDistance):
        return self.distances[client.id] if self.id is not client.id else None


class Method:
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


class MTVRP(Method):
    def __init__(self, clients: int, trips: int, capacity: int, demands: List[int], service_time: List[int],
                 client_positions: List[ClientWithPosition]):
        super().__init__(clients, trips, capacity, demands, service_time)
        self.client_positions = client_positions

    def run(self) -> tuple:
        clients = self.client_positions
        deposit = clients.pop(0)

        # Start at Deposit
        current: ClientWithPosition = deposit

        trips = 1
        distances: Dict[int, List[Tuple[int, float]]] = {}
        capacity = self.capacity
        while len(clients) > 0:
            k = trips - 1

            # Sort clients by distance to current position
            clients = sorted(clients, key=lambda c: current.distance_to(c))

            # Specify that the next travel position is the client with lower distance
            next: ClientWithPosition = clients[0]

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
                prev = current

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
                current = deposit
                self.report(prev.name + '\t->\t' + current.name + '\n')

        total_distance = 0
        for i in range(0, trips):
            for remaining, distance in distances[i]:
                total_distance += (trips - 1 - i + remaining) * distance

        return trips, total_distance


class MLP(Method):
    def __init__(self, clients: int, trips: int, capacity: int, demands: List[int], service_time: List[int],
                 travel_times: List[ClientWithDistance]):
        super().__init__(clients, trips, capacity, demands, service_time)
        self.travel_times = travel_times

    def run(self):
        pass


def parse_file(file_name: str) -> Method:
    path = 'tests/' + file_name

    if not os.path.exists(path):
        raise FileNotFoundError('[Error] No se ha encontrado el archivo '" + file_name + "' en la carpeta \'tests/\'')

    with open(path, mode='r') as file:
        data = file.readlines()

        single_int = re.compile(r'\d+')
        multiple_int = re.compile(r'[^\d]+')

        clients = int(single_int.search(data[0])[0])
        trips = int(single_int.search(data[1])[0])
        capacity = int(single_int.search(data[2])[0])

        demand = [int(d) for d in multiple_int.split(data[4].strip())]
        service_time = [int(d) for d in multiple_int.split(data[6].strip())]

        extra_data = []
        for i in range(8, len(data)):
            extra = [int(pos) for pos in multiple_int.split(data[i].strip())]

            real_i = i - 8

            i_demand = demand[real_i - 1] if real_i > 0 else 0

            if len(extra) == 2:
                extra = ClientWithPosition(real_i, i_demand, extra[0], extra[1])
            else:
                extra = ClientWithDistance(real_i, i_demand, extra)

            extra_data.append(extra)

        if isinstance(extra_data[0], ClientWithPosition):
            return MTVRP(clients, trips, capacity, demand, service_time, extra_data)

        return MLP(clients, trips, capacity, demand, service_time, extra_data)


Path('results').mkdir(exist_ok=True)

for file_name in [
    'VRPNC1m',
    'VRPNC2m',
    'VRPNC3m',
    'VRPNC4m',
    'VRPNC5m',
    'VRPNC11m',
    'VRPNC12m',
    'MT-DMP10s0-01',
    'MT-DMP10s0-05',
    'MT-DMP15s0-03',
    'MT-DMP15s0-04'
]:
    file_name += '.txt'
    if file_name[0] == 'M':
        break

    start = time.process_time()

    method = parse_file(file_name)

    [trips, distance] = method.run()

    end = time.process_time()

    with open('results/' + file_name, mode='w') as file:
        file.writelines([
            'Elapsed Time: ' + str(end - start) + ' seconds\n',
            'Expected Trips: ' + str(method.trips) + '\n',
            'Actual Trips: ' + str(trips) + '\n',
            'Total Distance: ' + str(distance) + '\n',
            method.get_report()
        ])
