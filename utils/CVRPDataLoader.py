class CVRPDataLoader:
    """
    Class to load CVRP instances. Each instance is a dictionary with keys:
    - 'id': instance number (1 to 4)
    - 'm_vehicles': number of vehicles available (Nv)
    - 'capacity': capacity of each vehicle (C)
    - 'nodes': dictionary mapping node IDs to their (x, y) coordinates
    """

    def __init__(self) -> None:
        self.depot = (0, 0)

    def get_instance(self, instance_id: int) -> dict:
        """
        Retourne l'instance correspondant à l'ID (1 à 4).
        """
        instances = {
            1: self.get_instance_1,
            2: self.get_instance_2,
            3: self.get_instance_3,
            4: self.get_instance_4,
        }
        if instance_id in instances:
            return instances[instance_id]()
        raise ValueError(f"ID {instance_id} invalide (1-4).")

    def get_instance_1(self) -> dict:
        return {
            "id": 1,
            "m_vehicles": 2,
            "capacity": 5,
            "nodes": {0: self.depot, 1: (-2, 2), 2: (-5, 8), 3: (2, 3)},
        }

    def get_instance_2(self) -> dict:
        return {
            "id": 2,
            "m_vehicles": 2,
            "capacity": 2,
            "nodes": {0: self.depot, 1: (-2, 2), 2: (-5, 8), 3: (2, 3)},
        }

    def get_instance_3(self) -> dict:
        return {
            "id": 3,
            "m_vehicles": 3,
            "capacity": 2,
            "nodes": {
                0: self.depot,
                1: (-2, 2),
                2: (-5, 8),
                3: (2, 3),
                4: (5, 7),
                5: (2, 4),
                6: (2, -3),
            },
        }

    def get_instance_4(self) -> dict:
        return {
            "id": 4,
            "m_vehicles": 4,
            "capacity": 3,
            "nodes": {
                0: self.depot,
                1: (-2, 2),
                2: (-5, 8),
                3: (6, 3),
                4: (4, 4),
                5: (3, 2),
                6: (0, 2),
                7: (-2, 3),
                8: (-4, 3),
                9: (2, 3),
                10: (2, 7),
                11: (-2, 5),
                12: (-1, 4),
            },
        }
