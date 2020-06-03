import os
import re
from typing import List


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Method:
    def __init__(self, clients: int, trips: int, capacity: int, demands: List[int], service_time: List[int]):
        self.clients = clients
        self.trips = trips
        self.capacity = capacity
        self.demands = demands
        self.service_time = service_time

    def run(self):
        pass


class MTVRP(Method):
    def __init__(self, clients: int, trips: int, capacity: int, demands: List[int], service_time: List[int],
                 client_positions: List[Position]):
        super().__init__(clients, trips, capacity, demands, service_time)
        self.client_positions = client_positions

    def run(self):
        pass


class MLP(Method):
    def __init__(self, clients: int, trips: int, capacity: int, demands: List[int], service_time: List[int],
                 travel_times: List[List[int]]):
        super().__init__(clients, trips, capacity, demands, service_time)
        self.travel_times = travel_times

    def run(self):
        pass


def parse_file(file_name: str) -> Method:
    path = 'tests/' + file_name

    if not os.path.exists(path):
        raise FileNotFoundError("[Error] No se ha encontrado el archivo '" + file_name + "' en la carpeta 'tests/'")

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
            if len(extra) == 2:
                extra = Position(extra[0], extra[1])
            extra_data.append(extra)

        if isinstance(extra_data[0], Position):
            return MTVRP(clients, trips, capacity, demand, service_time, extra_data)

        return MLP(clients, trips, capacity, demand, service_time, extra_data)


for file in [
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
    method = parse_file(file + '.txt')

    if isinstance(method, MTVRP):
        print('File \'' + file + '\' corresponds to method MTVRP')
    else:
        print('File \'' + file + '\' corresponds to method MLP')
