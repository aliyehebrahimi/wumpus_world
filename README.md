# Wumpus World

A knowledge-based agent designed to navigate and survive in the Wumpus World.

## Overview

This project implements a **WumpusWorldAgent**, a goal-based, knowledge-based agent that interacts with a simulated **WumpusWorld** environment. The agent makes decisions based on a knowledge base (KB) that follows the KB-AGENT specification from the **Artificial Intelligence: A Modern Approach (AIMA)** book. The simulation adheres to the PEAS (Performance measure, Environment, Actuators, and Sensors) description of the Wumpus World.

## Features

- **WumpusWorldAgent**: Implements an intelligent agent that makes decisions based on logical reasoning.
- **KnowledgeBase**: Stores and processes percepts to derive the best course of action.
- **WumpusWorld Simulation**: Models the physical environment, including hazards like pits and the Wumpus.
- **Unit Tests**: Ensures the correctness of implementations with predefined test cases.

## Setup & Usage

1. Clone the repository and navigate to the project directory.
2. Ensure you have Python 3 installed.
3. Run the initial scratchpad script to see the setup:

   ```sh
   python3 scratchpad.py
   ```

4. Implement the missing components in the following files:
   - `wumpus_world_agent.py` (Agent logic)
   - `knowledge_base.py` (Reasoning and inference engine)
   - `wumpus_world.py` (World physics and interactions)

5. Run the unit tests to validate your implementation:

   ```sh
   python3 -m unittest
   ```

6. Once all tests pass, create a demonstration script in `main.py` to showcase the agent’s decision-making in a simulated world.

## Development Guide

### Step 1: Implement the WumpusWorldAgent
- Start by reviewing `scratchpad.py` to understand how the agent interacts with the world and knowledge base.
- Modify `wumpus_world_agent.py` to complete the `WumpusWorldAgent` class.
- Use `test_wumpus_world_agent.py` to iteratively implement and test each functionality.
- Ensure that the agent can take percepts and generate logical actions.

### Step 2: Build the KnowledgeBase
- Implement the logic to `tell` and `ask` the knowledge base about world states.
- Run `test_knowledge_base.py` to verify your implementation.

### Step 3: Implement the WumpusWorld Simulation
- Define the rules for agent movement, pit hazards, Wumpus encounters, and percept generation.
- Use `test_wumpus_world.py` to validate the environment’s logic.

### Step 4: Demonstrate the Agent in Action
- Write a `main.py` script to instantiate a world, agent, and knowledge base.
- Simulate different scenarios where the agent intelligently navigates the Wumpus World.

## Notes & Hints

- Follow the KB-AGENT agent function and Wumpus World rules as outlined in AIMA.
- Ensure each class and method includes descriptive docstrings.
- The agent should print short messages to indicate actions (e.g., `print("Climbing out")`).
- Test frequently to ensure incremental progress.
- The simulated WumpusWorld includes minor simplifications, such as an eternally echoing **Scream** when the Wumpus dies.

## Conclusion

This project explores AI-based logical reasoning through the **Wumpus World** problem. By implementing the agent and knowledge base, you’ll gain a deep understanding of how AI systems make decisions in uncertain environments.

Happy coding! 🚀

