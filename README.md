# GR1_simulations

## graph_builder.py
This module contains the functions to create graphs given a GR1 product automaton. 
The green arrows represent transitions taken by the environment, and the blue arrows represent transitions taken by the system.

## runner_blocker/runner_blocker.py
This is an example GR1 game that is visualized in RunnerBlockerStatesExplained.jpeg.

The system, known as the runner, tries to eventually reach state 4 while always staying away from the state that the environment, or blocker, is in.

This python file creates runner_blocker_game.pdf, which shows the GR1 game graph of runner blocker.

It also creates runner_blocker_states.pdf, which shows all the states in the GR1 game and the transitions the environment and system take to reach them. 
