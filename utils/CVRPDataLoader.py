class CVRPDataLoader:
    """
    Class to load CVRP instances. Each instance is a dictionary with keys:
    - 'id': instance number (1 to 4)
    - 'm_vehicles': number of vehicles available (Nv)
    - 'capacity': capacity of each vehicle (C)
    - 'nodes': list of nodes with their coordinates
    """

    def get_instance(self, instance_id: int) -> dict:
        """
        Returns the instance corresponding to the given ID (1-4).

        Args:
            instance_id (int): The instance number (1 to 4).

        Returns:
            dict: The instance data with keys: id, m_vehicles, capacity, nodes.

        Raises:
            ValueError: If instance_id is not between 1 and 4.
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
            "nodes": [(-2, 2), (-5, 8), (2, 3)],
        }

    def get_instance_2(self) -> dict:
        return {
            "id": 2,
            "m_vehicles": 2,
            "capacity": 2,
            "nodes": [(-2, 2), (-5, 8), (2, 3)],
        }

    def get_instance_3(self) -> dict:
        return {
            "id": 3,
            "m_vehicles": 3,
            "capacity": 2,
            "nodes": [(-2, 2), (-5, 8), (2, 3), (5, 7), (2, 4), (2, -3)],
        }

    def get_instance_4(self) -> dict:
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

    def get_fleur_de_lys(self) -> dict:
        return {
            "id": 5,
            "m_vehicles": 4,
            "capacity": 3,
            "nodes": [
                (0, 5),
                (-1, 2),
                (1, 2),
                (-2.5, 1),
                (-1.5, 1),
                (-2, 0.5),
                (2.5, 1),
                (1.5, 1),
                (2, 0.5),
                (0.5, -1),
                (-0.5, -1),
                (0, -1.5),
            ],
        }
