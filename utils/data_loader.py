class CVRPDataLoader:
    """
    Class to load CVRP (Capacitated Vehicle Routing Problem) instances.
    Each instance returns a dictionary containing information about vehicles,
    capacities, and node coordinates.
    """

    def load_instance(self, instance_id: int) -> dict:
        """
        Loads the specific CVRP instance based on the ID (1-4).

        Args:
            instance_id (int): The instance identifier (1 to 4).

        Returns:
            dict: Data instance with 'id', 'm_vehicles', 'capacity', and 'nodes'.

        Raises:
            ValueError: If the instance_id is outside the valid range.
        """
        instances = {
            1: self._load_instance_1,
            2: self._load_instance_2,
            3: self._load_instance_3,
            4: self._load_instance_4,
        }
        if instance_id in instances:
            return instances[instance_id]()
        raise ValueError(f"Invalid instance ID {instance_id}. Must be between 1 and 4.")

    def _load_instance_1(self) -> dict:
        return {
            "id": 1,
            "m_vehicles": 2,
            "capacity": 5,
            "nodes": [(-2, 2), (-5, 8), (2, 3)],
        }

    def _load_instance_2(self) -> dict:
        return {
            "id": 2,
            "m_vehicles": 2,
            "capacity": 2,
            "nodes": [(-2, 2), (-5, 8), (2, 3)],
        }

    def _load_instance_3(self) -> dict:
        return {
            "id": 3,
            "m_vehicles": 3,
            "capacity": 2,
            "nodes": [(-2, 2), (-5, 8), (2, 3), (5, 7), (2, 4), (2, -3)],
        }

    def _load_instance_4(self) -> dict:
        return {
            "id": 4,
            "m_vehicles": 4,
            "capacity": 3,
            "nodes": [
                (-2, 2),
                (-5, 8),
                (6, 3),
                (4, 4),
                (3, 2),
                (0, 2),
                (-2, 3),
                (-4, 3),
                (2, 3),
                (2, 7),
                (-2, 5),
                (-1, 4),
            ],
        }


