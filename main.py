# Main Wumpus World Simulation
# Revised with proper termination conditions and enhanced debugging

from wumpus_world import WumpusWorld
from wumpus_world_agent import WumpusWorldAgent
from knowledge_base import KnowledgeBase

def main():
    # Initialize world with test configuration
    world = WumpusWorld(
        agent_location=(1, 1),
        agent_direction="East",
        agent_alive=True,
        wumpus_alive=True,
        wumpus_location=(1, 3),
        gold_location=(2, 3),
        pit_locations=[(3, 1), (3, 3), (4, 4)],
    )

    # Initialize agent components
    kb = KnowledgeBase()
    agent = WumpusWorldAgent(kb)
    
    # Simulation parameters
    print("Starting Wumpus World Simulation...")
    print(f"Agent starts at {world.agent_location}, facing {world.agent_direction}")
    print(f"Wumpus at {world.wumpus_location}, Gold at {world.gold_location}, Pits at {world.pit_locations}")
    print("-" * 40)

    step = 0
    max_steps = 50
    has_gold = False

    while step < max_steps and world.agent_alive:
        step += 1
        current_loc = world.agent_location
        current_dir = world.agent_direction
        
        # Get current percepts
        percept = world.percept(current_loc)
        action = agent.action(percept)
        
        # Print step header
        print(f"\nStep {step}: Agent at {current_loc}, facing {current_dir}")
        print(f"Percept: {percept}")
        print(f"Action: {action.__name__ if action else 'None'}")

        # Execute action if possible
        if action:
            action(agent, world)
            
            # Update gold status
            if action.__name__ == "grab" and world.gold_location is None:
                if not has_gold:
                    print("Gold grabbed!")
                    has_gold = True
                else:
                    print("Agent tries to grab but already has gold")

        # Check termination conditions
        if not world.agent_alive:
            print("\nAgent died! Game Over.")
            break
            
        if world.agent_location is None:
            if has_gold:
                print("\nVictory! Agent escaped with the gold!")
            else:
                print("\nAgent escaped empty-handed")
            break
            
        # Print world state
        print(f"New position: {world.agent_location}")
        print(f"Gold carried: {has_gold}")
        print("-" * 40)

        # Early exit if gold collected and at exit
        if has_gold and world.agent_location == (1, 1):
            print("Agent returned to exit with gold!")
            break

    if step >= max_steps:
        print("\nSimulation stopped: Maximum steps reached")

if __name__ == "__main__":
    main()