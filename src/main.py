from tkinter import messagebox

import customtkinter as ctk
import matplotlib.pyplot as pyplot
import networkx
from utils import link, node, automaton

# DFA - Deterministic Finite Automaton
# Regular languages
# Accepts empty string if the initial state is an accepting state
# https://en.wikipedia.org/wiki/Deterministic_finite_automaton
ctk.set_appearance_mode("dark")


def open_help():
    messagebox.showinfo("Help", """
    You can make an arbitrary DFA with this simulator
    Usage:
      1) Create some states seperated by comma ex.: s1, s2, s3
      2) Give an input string ex.: 00001
      3) Give the initial state where the automaton starts
      4) Give the transitions seperated by whitespace, format should be: FROM_STATE SYMBOL TO_STATE
      5) Give the accepting states seperated by comma ex.: s1, s2, s3
    """)


# Draw graph with networkx in different window (PyCharm settings -> Tools -> PyCharm Scientific disable)
def draw_graph(links):
    graph = {}
    for _link in links:
        if not _link.node1.get_name() in graph:
            graph[_link.node1.get_name()] = [_link.node2.get_name()]
        else:
            graph[_link.node1.get_name()].append(_link.node2.get_name())
    g = networkx.DiGraph(graph)
    pos = networkx.circular_layout(g)

    fig, ax = pyplot.subplots(figsize=(10, 10))

    options = {
        'node_color': 'red',
        'node_size': 1000,
        'width': 3,
        'arrowsize': 15,
        'connectionstyle': 'arc3, rad=0.1',
        'ax': ax,
        'arrows': True,
        'with_labels': True,
    }

    networkx.draw_networkx(g, pos, **options)

    labels = {}

    for _link in links:
        labels[(_link.node1.get_name(), _link.node2.get_name())] = _link.rule

    networkx.draw_networkx_edge_labels(g, pos, edge_labels=labels, font_color="blue", font_size=15, label_pos=0.75)

    ax.autoscale_view()

    pyplot.axis("off")
    pyplot.show()


class App(ctk.CTk):
    # GUI settings
    def __init__(self):
        ctk.CTk.__init__(self)
        self.title("DFA Simulator")
        self.geometry("500x800")
        self.resizable(False, True)
        frame = ctk.CTkFrame(master=self)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        title = ctk.CTkLabel(master=frame, text="DFA simulator", font=('Roboto', 20))
        title.pack(padx=10, pady=10)

        self.states = ctk.CTkEntry(master=frame, placeholder_text="List of states")
        self.states.pack(padx=10)
        self.states.insert(ctk.END, "s0, s1, s2")

        self.input = ctk.CTkEntry(master=frame, placeholder_text="Input string")
        self.input.pack(padx=10, pady=10)
        self.input.insert(ctk.END, "000001")

        self.initial_state = ctk.CTkEntry(master=frame, placeholder_text="Initial state")
        self.initial_state.pack(padx=10)
        self.initial_state.insert(ctk.END, "s0")

        self.rules = ctk.CTkTextbox(master=frame, font=('monospace', 17))
        self.rules.pack(padx=10, pady=10)
        self.rules.insert(ctk.END, "s0 0 s0\ns0 1 s1\ns0 2 s2\ns1 0 s0")

        self.accepting_states = ctk.CTkEntry(master=frame, placeholder_text="Accepting states")
        self.accepting_states.pack(padx=10, pady=10)
        self.accepting_states.insert(ctk.END, "s1")

        self.checkbox_status = ctk.BooleanVar(value=True)
        self.checkbox = ctk.CTkCheckBox(master=frame, text="Draw a directed graph", onvalue=True, offvalue=False,
                                        variable=self.checkbox_status, command=self.handle_checkbox)
        self.checkbox.pack(padx=10, pady=10)

        btn = ctk.CTkButton(master=frame, text="Start machine", command=self.parse_rules)
        btn.pack(padx=10, pady=10)

        self.help = ctk.CTkButton(master=frame, text="Get help", command=open_help)
        self.help.pack(padx=10, pady=10)

        self.status = ctk.CTkTextbox(master=frame)
        self.status.pack(padx=10, pady=10, fill='both')
        self.status.insert(ctk.END, "Status of machine: ")

        ctk.CTk.mainloop(self)

    def handle_checkbox(self):
        if self.checkbox_status:
            self.checkbox_status = False
        else:
            self.checkbox_status = True

    # Get data from input boxes and turn into parseable format
    def parse_rules(self):
        self.status.delete('1.0', ctk.END)
        # ['s1', 's2', ...] + Clear empty string with filter
        state_list = list(filter(None, [x.strip() for x in self.states.get().split(',')]))
        # 's1'
        initial_state = self.initial_state.get()
        # ['s1', 's2', ...] + Clear empty string with filter
        accepting_states = list(filter(None, [x.strip() for x in self.accepting_states.get().split(',')]))

        # No states defined
        if len(state_list) == 0:
            messagebox.showerror('Error', 'Please give some states!')
            return

        # No initial state set
        if len(initial_state.strip()) == 0:
            messagebox.showerror('Error', 'Please give an initial state!')
            return

        # Initial state is not defined
        if not any(x == initial_state for x in state_list):
            messagebox.showerror('Error', 'The given initial state is not defined in the state list!')
            return

        # Given accepting state is not defined

        if len(accepting_states) != 0:
            if not any(x in accepting_states for x in state_list):
                messagebox.showerror('Error', 'The given accepting state(s) is (are) not defined in the state list!')
                return

        # If there are not any accepting states then the accepted language will be the empty set...
        # Parse rules + Clear empty string with filter
        # ['s0 0 s1', 's1 1 s2', ...]
        rules = list(filter(None, [x.strip() for x in self.rules.get("1.0", ctk.END).split('\n')]))
        rules_cleaned = []

        # Remove unnecessary whitespace from rules ex. ['     s0   1  s1 ']
        for rule in rules:
            rules_cleaned.append([x.strip() for x in rule.split(' ')])

        # Parse nodes
        nodes = []
        for _node in state_list:
            nodes.append(node.Node(_node))

        # Parse accepting states
        # Parse links
        links = []

        for rule in rules_cleaned:
            if len(rule) != 3:
                messagebox.showerror('Error', "The format of the rules are wrong, the format should be:\n"
                                              "STATE TRANSITION_SYMBOL STATE")
                return
            from_node = next((n for n in nodes if n.name == rule[0]), None)
            to_node = next((n for n in nodes if n.name == rule[2]), None)

            if any(n.node1 == from_node and n.rule == rule[1] for n in links):
                messagebox.showerror('Error',
                                     "Your automaton has a state where you can go to more than one state with same "
                                     "transition symbol that turns your automaton into a nondeterministic automaton ("
                                     "NFA).")
                return

            links.append(link.Link(from_node, rule[1], to_node))

        # Connect states by links
        for _link in links:
            if _link.node1 is None or _link.node2 is None:
                messagebox.showerror('Error',
                                     "You specified a state in the rules that does not exist!")
                return
            else:
                _link.node1.add_link(_link)

        initial_node = next((n for n in nodes if n.name == initial_state), None)

        a = automaton.Automaton(initial_node=initial_node, terminal_nodes=accepting_states, node_list=nodes,
                                status=self.status)

        accepted = a.accepts_input(self.input.get())

        if accepted:
            self.status.insert(ctk.END, f"[PROGRAM]: Initial state: {initial_state}\n")
            self.status.insert(ctk.END, f"[PROGRAM]: Input string: {self.input.get()}\n")
            self.status.insert(ctk.END, f"[PROGRAM]: States: {state_list}\n")
            self.status.insert(ctk.END, f"[PROGRAM]: Accepting states: {accepting_states}\n")
            self.status.insert(ctk.END, f"[PROGRAM]: Transition function: {[x.__str__() for x in links]}\n")
            self.status.insert(ctk.END, "[PROGRAM]: Machine status: ACCEPTED")

            # Make adjacency list for DFA visualisation
            messagebox.showinfo("DFA Simulator", "The automaton is accepted the given input!")

            if self.checkbox_status:
                draw_graph(links)
        else:
            # self.status.delete('1.0', ctk.END)
            messagebox.showerror("DFA Simulator", "The automaton is rejected the given input!")
            self.status.insert(ctk.END, "[PROGRAM]: Machine status: FAILED")
            if self.checkbox_status:
                draw_graph(links)


if __name__ == '__main__':
    app = App()
