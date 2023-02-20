from utils.link import Link


class Node:
    """
    Node (state) with a specified name and relationship with other node
    :param name: Name of the state
    """
    def __init__(self, name: str):
        self.name = name
        self.links = []

    def add_link(self, linking: Link):
        """
        Connect a node to another node
        :param linking: Describes the relation between two nodes
        """
        self.links.append(linking)

    def get_name(self):
        """
        Get the name of the node
        :return: Name of the node
        """
        return self.name
