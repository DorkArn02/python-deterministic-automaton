# Deterministic Finite Automaton Simulator

## About the program

This is a deterministic finite automaton simulator program. The DFA can recognize regular languages. Unlike nondeterministic finite automata you can go only one way that is why deterministic.

<p style="text-align: center">
<img src="https://user-images.githubusercontent.com/28065716/221379456-03f41a77-63e8-474c-b43b-0fa58d561471.png" alt=""/>

<img src="https://user-images.githubusercontent.com/28065716/221379488-6d2b1d97-341f-4878-8e2f-698785f0335b.png" alt="">
</p>

## Math

Deterministic Finite automaton can be described by 5 things:
`M(Q, Σ, δ, q0, A)`

- Q: Finite set of states
- Σ: Finite set of input symbols
- δ: Q × Σ → Q: Transition function
- q0: Initial state
- A: set of accept states

Transition example: If you read `0` symbol you go from `s0` state to `s1` state, formally: `(s0, 0) -> s1`

Deterministic automaton can have zero accepting states that mean the accepted language is the language of empty set.

If the initial state is an accepting state the automaton can recognize the empty string.

If the automaton wants to go to an undefined state it creates an exception, if you want to avoid this you should create a dead state

## Usage

You need to give some information in order to start the machine such as:
- Initial state ex.: `s0`
- States ex.: `s1, s2, s3`
- Accepting states (optional) ex.: `s1, s2, s3`
- Input string ex.: `0001`
- Rules: ex.: `s0 1 s1`

## Error handling

- State validation
- Rules validation
- Detect nondeterminism
- Transition validation


## Example automaton

Initial state: A

State list: A, B, C

Final state: B

Rules:
- A 0 B
- A 1 C
- C 0 C
- C 1 C
- B 0 B
- B 1 B

![image](https://user-images.githubusercontent.com/28065716/218256499-cf5a4338-dcc2-416a-8e84-16099b26ac50.png)

This DFA accepts languages that start with zero and can contain 0-s, 1-s.


## Dependencies

You need to install the following dependencies in order to run the program in your computer:

- matplotlib
- networkx
- tkinter
- customtkinter

Project dependencies after manual dependency installation in PyCharm IDE:

![image](https://user-images.githubusercontent.com/28065716/221379604-d4d6f1f5-6f0b-4e93-8edd-c94e06984d03.png)
