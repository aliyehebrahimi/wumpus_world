# WumpusWorldAgent
# An agent designed to perform in the wumpus world environment.
# Aliyeh Ebrahimi


from typing import Any, Tuple, Optional, Callable

# Type alias for percepts
Percept = Tuple[str]


class WumpusWorldAgent:
    """WumpusWorldAgent
    An agent designed to perform in the Wumpus World environment.

    Parameters
    ----------
    kb : Any
        The knowledge base used by the agent for decision making.

    Attributes
    ----------
    kb : Any
        The agent's knowledge base.
    time : int
        The current time step of the agent, initialized to 0.

    Notes
    -----
    Created by Aliyeh Ebrahimi
    """

    def __init__(self, kb: Any) -> None:
        self.kb = kb
        self.time = 0

    def make_percept_sentence(self, percept: Percept) -> Tuple[Percept, int]:
        """Create a percept sentence with current time.

        Parameters
        ----------
        percept : Percept
            The percept received from the environment as a tuple of strings.

        Returns
        -------
        tuple
            A tuple containing the percept and current time (percept, time).
        """
        pass

    def make_action_query(self) -> Tuple[str, int]:
        """Create an action query with current time.

        Returns
        -------
        tuple
            A tuple containing the action query string and current time ("action?", time).
        """
        pass

    def make_action_sentence(self, action: Callable) -> Tuple[Callable, int]:
        """Create an action sentence with current time.

        Parameters
        ----------
        action : Callable
            The action to be formatted into a sentence.

        Returns
        -------
        tuple
            A tuple containing the action and current time (action, time).
        """
        pass

    def action(self, percept: Percept) -> Optional[Callable]:
        """Process a percept and return an action based on the knowledge base.

        Parameters
        ----------
        percept : Percept
            The percept received from the environment as a tuple of strings.

        Returns
        -------
        Any or None
            The action to be performed, or None if no action is determined.

        Notes
        -----
        This method follows these steps:
        1. Tells the KB the percept sentence
        2. Asks the KB for an action
        3. Tells the KB the action sentence (if action exists)
        4. Increments the time
        """
        # Tell KB the percept sentence
        percept_sentence = self.make_percept_sentence(percept)
        self.kb.tell(percept_sentence)

        # Ask KB for action
        query = self.make_action_query()
        action = self.kb.ask(query)

        # Tell KB the action sentence
        if action is not None:  # Handle case where KB might return None
            action_sentence = self.make_action_sentence(action)
            self.kb.tell(action_sentence)

        # Increment time
        self.time += 1
        return action

    def turn_left(self, world: Any) -> None:
        """Turn the agent left in the world.

        Parameters
        ----------
        world : Any
            The Wumpus World environment object.
        """
        print("Turning left")
        world.turned_left()

    def turn_right(self, world: Any) -> None:
        """Turn the agent right in the world.

        Parameters
        ----------
        world : Any
            The Wumpus World environment object.
        """
        print("Turning right")
        world.turned_right()

    def move_forward(self, world: Any) -> None:
        """Move the agent forward in the world.

        Parameters
        ----------
        world : Any
            The Wumpus World environment object.
        """
        print("Moving forward")
        world.moved_forward()

    def shoot(self, world: Any) -> None:
        """Make the agent shoot an arrow in the world.

        Parameters
        ----------
        world : Any
            The Wumpus World environment object.
        """
        print("Shooting")
        world.shot()

    def grab(self, world: Any) -> None:
        """Make the agent grab an object in the world.

        Parameters
        ----------
        world : Any
            The Wumpus World environment object.
        """
        print("Grabbing")
        world.grabbed()

    def climb(self, world: Any) -> None:
        """Make the agent climb out of the pit in the world.

        Parameters
        ----------
        world : Any
            The Wumpus World environment object.
        """
        print("Climbing out")
        world.climbed()
