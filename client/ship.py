class Ship:
    def __init__(self, coordinates):
        self.coordinates = coordinates  # lijst [(r,c), ...]
        self.hits = set()

    def is_hit(self, r, c):
        return (r, c) in self.coordinates

    def register_hit(self, r, c):
        if self.is_hit(r, c):
            self.hits.add((r, c))

    def is_sunk(self):
        return set(self.coordinates) == self.hits
