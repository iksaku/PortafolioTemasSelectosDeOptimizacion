import re
import os

def parse_file(file_name: str):
    path = 'tests/' + file_name
    
    if (not os.path.exists(path)):
        raise FileNotFoundError("[Error] No se ha encontrado el archivo '" + file_name + "' en la carpeta 'tests/'")
    
    model = None

    with open(path, mode='r') as file:
        data = file.readlines()

        single_int = re.compile(r'\d+')
        multiple_int = re.compile(r'[^\d]+')

        clients = single_int.search(data[0])[0]
        trips = single_int.search(data[1])[0]
        capacity = single_int.search(data[2])[0]

        demand = [int(d) for d in multiple_int.split(data[4].strip())]
        service_time = [int(d) for d in multiple_int.split(data[6].strip())]

        coords = {}
        for i in range(8, len(data)):
            coords[i - 7] = tuple([int(pos) for pos in multiple_int.split(data[i].strip())])
        
        print('Clients:', clients)
        print('Trips:', trips),
        print('Capacity:', capacity)
        print('Demand:', demand)
        print('Service Times:', service_time)
        print('Coords:', coords)

parse_file('VRPNC12m.txt')
