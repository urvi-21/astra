class SharedMemory:

    def __init__(self):

        self.memory = {
            "forecast_history": [],
            "pricing_history": [],
            "inventory_history": [],
            "risk_history": [],
            "decisions": []
        }

    def update(self, key, value):

        self.memory[key].append(value)

    def get(self, key):

        return self.memory.get(key, [])