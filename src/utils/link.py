from typing import TYPE_CHECKING


# Prevent circular dependency
if TYPE_CHECKING:
    from utils.node import Node


class Link:
    """
    Initializes the linkage between two nodes and the transition symbol
    :param node1: Starting node
    :param rule: Symbol example: 0
    :param node2: Destination node
    """
    def __init__(self, node1: 'Node', rule: str, node2: 'Node'):
        self.node1 = node1
        self.rule = rule
        self.node2 = node2

    def __str__(self):
        return f"({self.node1.get_name()}, {self.rule}) -> {self.node2.get_name()}"
