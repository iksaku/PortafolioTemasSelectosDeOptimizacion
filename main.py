from __future__ import annotations
from clients import ClientWithDistance, ClientWithPosition
from methods import BaseMethod, MTVRP
from pathlib import Path
import os
import re
import time


def parse_file(file_name: str) -> BaseMethod:
    path = 'tests/' + file_name

    if not os.path.exists(path):
        raise FileNotFoundError('[Error] No se ha encontrado el archivo \'' + file_name + '\' en la carpeta \'tests/\'')

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

        return MTVRP(clients, trips, capacity, demand, service_time, extra_data)


Path('results').mkdir(exist_ok=True)

for file_name in [
    'MT-DMP10s0-01',
    'MT-DMP10s0-05',
    'MT-DMP15s0-03',
    'MT-DMP15s0-04',
    'VRPNC1m',
    'VRPNC2m',
    'VRPNC3m',
    'VRPNC4m',
    'VRPNC5m',
    'VRPNC11m',
    'VRPNC12m'
]:
    file_name += '.txt'

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
