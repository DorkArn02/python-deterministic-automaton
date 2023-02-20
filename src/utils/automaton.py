from tkinter import messagebox

import customtkinter as ctk

from utils.node import Node


class Automaton:
    """
    :param initial_node: The node where the automaton starts
    :param node_list: List of all defined nodes
    :param terminal_nodes: List of all accepting nodes
    :param status: Reference of the status box from the GUI
    """
    def __init__(self, initial_node: Node, node_list: list[Node], terminal_nodes: list[Node], status):
        self.initial_node = initial_node
        self.node_list = node_list
        self.terminal_nodes = terminal_nodes
        self.status = status

    def process_state(self, current_node: Node, rule: str):
        """
        :param current_node: The node where the automaton is
        :param rule: The transition symbol
        :return:
        """
        for link in current_node.links:
            if link.rule == rule:
                return link.node2
        return None

    def accepts_input(self, input_string: str):
        current_node = self.initial_node
        # Read the input symbol and start from the initial state
        for symbol in input_string:
            self.status.insert(ctk.END, f'[STEP]: Symbol: {symbol} and current state {current_node.get_name()}\n')

            # If you can't go to next state
            if len(current_node.links) == 0 \
                    or not any(x.rule == symbol for x in current_node.links):
                self.status.insert(ctk.END,
                                   f"[ERROR]: Transition does not exist from {current_node.get_name()} to other node "
                                   f"with symbol: {symbol}\n")
                messagebox.showerror('Error',
                                     f"From state {current_node.get_name()} can't go to another state by using {symbol}"
                                     f" transition symbol, because there are not any rules defined yet ")
                return False
            else:
                current_node = self.process_state(current_node, symbol)

        if current_node is None:
            messagebox.showerror('Error', "The given state does not exist")
            return False
        else:
            return current_node.get_name() in self.terminal_nodes
