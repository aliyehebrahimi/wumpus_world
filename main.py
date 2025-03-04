# Main
# A demonstration of the WumpusWorld and WumpusWorldAgent.
# Aliyeh Ebrahimi


from wumpus_world import WumpusWorld
from wumpus_world_agent import WumpusWorldAgent
from knowledge_base import KnowledgeBase


def main():
    # Initialize the Wumpus World with the example configuration from tests
    world = WumpusWorld(
        agent_location=(1, 1),
        agent_direction="East",
        agent_alive=True,
        wumpus_alive=True,
        wumpus_location=(1, 3),
        gold_location=(2, 3),
        pit_locations=[(3, 1), (3, 3), (4, 4)],
    )

    # Initialize the Knowledge Base and Agent
    kb = KnowledgeBase()
    agent = WumpusWorldAgent(kb)
    agent.world_arg = world  # Temporary hack to give agent access to world state

    # Simulation loop
    print("Starting Wumpus World Simulation...")
    print(f"Agent starts at {world.agent_location}, facing {world.agent_direction}")
    print(
        f"Wumpus at {world.wumpus_location}, "
        f"Gold at {world.gold_location}, "
        f"Pits at {world.pit_locations}"
    )
    print("-" * 40)

    step = 0
    max_steps = 50  # Prevent infinite loop

    while (
        step < max_steps
        and world.agent_alive
        and world.agent_location is not None
        and agent.action is not None
    ):
        step += 1
        current_percept = world.percept(world.agent_location)
        new_line_str = "\n" if step > 1 else ""
        print(
            f"{new_line_str}Step {step}: Agent at {world.agent_location}, "
            f"facing {world.agent_direction}"
        )
        print(f"Percept: {current_percept}")

        # Agent decides and performs an action
        action = agent.action(current_percept)
        action_name = action.__name__
        print(f"Action: {action_name}")
        action(agent, world)

        if (
            not world.agent_alive
            or world.agent_location is None
            or (world.gold_location is None and action_name != "climb")
        ):
            print("-" * 40)

        # Check agent's status
        if not world.agent_alive:
            print("Agent died! Game Over.")
            break
        elif world.agent_location is None:
            print(f"Agent climbed out at {WumpusWorld.EXIT_LOCATION}!")
            if world.gold_location is None:
                print("Victory! Agent grabbed the gold and escaped!")
            else:
                print("Agent escaped but didn’t grab the gold.")
            break
        elif world.gold_location is None and action_name != "climb":
            print("Gold has been grabbed!")

    if step >= max_steps:
        print("Simulation ended: Maximum steps reached.")


if __name__ == "__main__":
    main()
