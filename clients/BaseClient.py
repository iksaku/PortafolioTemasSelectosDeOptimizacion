class BaseClient:
    def __init__(self, id: int, demand: int):
        self.demand = demand
        self.id = id
        self.name = 'Client ' + str(self.id) if self.id > 0 else 'Deposit\t'
