# WumpusWorld
# A simulated representation of a real Wumpus World, aligned with the specified
# characteristics in the AIMA text.
# Note: This is not a state model. It _is_ the real world / environment within
# which the agent operates. Think of it as actual, physical, reality.
# Note 2: This simulation will not include the modeling of time, for the sake of
# simplicity. This only affects the 'Bump' and 'Scream' percepts. In the case of
# 'Bump', we assume that when an agent is in a room facing a wall, it should receive
# the 'Bump' percept. For 'Scream', when the wumpus is killed we let the scream
# linger throughout the cave indefinitely.
# Aliyeh Ebrahimi


from typing import Optional, List, Tuple


class WumpusWorld:
    """
    A simulated representation of a real Wumpus World, aligned with the specified
    characteristics in the AIMA text. This is the real world in which the agent operates.
    This simulation does not model time (for simplicity) but includes basic actions and
    percepts such as 'Bump' and 'Scream'.
    """

    EXIT_LOCATION: Tuple[int, int] = (1, 1)

    def __init__(
        self,
        agent_location: Optional[Tuple[int, int]] = None,
        agent_direction: str = "East",
        agent_alive: bool = True,
        wumpus_alive: Optional[bool] = None,
        wumpus_location: Optional[Tuple[int, int]] = None,
        gold_location: Optional[Tuple[int, int]] = None,
        pit_locations: List[Tuple[int, int]] = [],
    ) -> None:
        """
        Initializes the WumpusWorld with the agent's location, direction, and other
        relevant properties such as the Wumpus' status and the locations of pits and gold.

        Parameters
        ----------
        agent_location : Optional[Tuple[int, int]], optional
            The location of the agent on the grid (defaults to (1, 1)).
        agent_direction : str, optional
            The direction the agent is facing (defaults to "East").
        agent_alive : bool, optional
            Whether the agent is alive (defaults to True).
        wumpus_alive : Optional[bool], optional
            Whether the Wumpus is alive (defaults to None, meaning not set).
        wumpus_location : Optional[Tuple[int, int]], optional
            The location of the Wumpus on the grid (defaults to None).
        gold_location : Optional[Tuple[int, int]], optional
            The location of the gold on the grid (defaults to None).
        pit_locations : List[Tuple[int, int]], optional
            A list of locations of pits on the grid (defaults to an empty list).
        """
        self.agent_location = agent_location or self.EXIT_LOCATION
        self.agent_direction = agent_direction
        self.agent_alive = agent_alive
        self.wumpus_alive = wumpus_alive
        self.wumpus_location = wumpus_location
        self.gold_location = gold_location
        self.pit_locations = pit_locations

    def percept(
        self, location: Optional[Tuple[int, int]] = None
    ) -> Tuple[
        Optional[str], Optional[str], Optional[str], Optional[str], Optional[str]
    ]:
        """
        Returns a percept tuple ('Stench', 'Breeze', 'Glitter', 'Bump', 'Scream') based on the
        agent's location or the specified location.

        Parameters
        ----------
        location : Optional[Tuple[int, int]], optional
            The location to check for percepts. If None, the percepts for the agent's current location are returned.

        Returns
        -------
        Tuple[Optional[str], Optional[str], Optional[str], Optional[str], Optional[str]]
            A tuple containing the percepts: 'Stench', 'Breeze', 'Glitter', 'Bump', 'Scream'.
            Each percept may be None if not applicable.
        """
        if location is None:
            location = self.agent_location

        stench = breeze = glitter = bump = scream = None

        # Stench: Wumpus is at location or adjacent
        if self.wumpus_location and (
            location == self.wumpus_location
            or self.adjacent(location, self.wumpus_location)
        ):
            stench = "Stench"

        # Breeze: Pit is adjacent
        if any(self.adjacent(location, pit) for pit in self.pit_locations):
            breeze = "Breeze"

        # Glitter: Gold is at location
        if location == self.gold_location:
            glitter = "Glitter"

        # Bump: Agent is at location and facing a wall
        if location == self.agent_location and self.agent_bumped_wall():
            bump = "Bump"

        # Scream: Wumpus is dead (lingers indefinitely)
        if self.wumpus_alive is False:
            scream = "Scream"

        return (stench, breeze, glitter, bump, scream)

    def turned_left(self) -> None:
        """
        Turn the agent counter-clockwise, to the left, resulting in a new `agent_direction`.

        Returns
        -------
        None
        """
        if not self.agent_alive or self.agent_location is None:
            return
        directions = {
            "East": "North",
            "North": "West",
            "West": "South",
            "South": "East",
        }
        self.agent_direction = directions[self.agent_direction]

    def turned_right(self) -> None:
        """
        Turn the agent clockwise, to the right, resulting in a new `agent_direction`.

        Returns
        -------
        None
        """
        if not self.agent_alive or self.agent_location is None:
            return
        directions = {
            "East": "South",
            "South": "West",
            "West": "North",
            "North": "East",
        }
        self.agent_direction = directions[self.agent_direction]

    def moved_forward(self) -> None:
        """
        Attempt to move the agent forward. If the move is successful, the agent's location is updated.
        Moving into a pit or a Wumpus' location kills the agent.

        Returns
        -------
        None
        """
        if not self.agent_alive or self.agent_location is None:
            return

        x, y = self.agent_location
        if self.agent_direction == "East" and self.agent_can_move_east():
            new_location = (x + 1, y)
        elif self.agent_direction == "West" and self.agent_can_move_west():
            new_location = (x - 1, y)
        elif self.agent_direction == "North" and self.agent_can_move_north():
            new_location = (x, y + 1)
        elif self.agent_direction == "South" and self.agent_can_move_south():
            new_location = (x, y - 1)
        else:
            return  # Bump into wall, no change

        self.agent_location = new_location

        # Check for hazards
        if new_location in self.pit_locations:
            self.agent_alive = False
        elif new_location == self.wumpus_location and self.wumpus_alive:
            self.agent_alive = False

    def grabbed(self) -> None:
        """
        Attempt to grab the gold. The gold is successfully grabbed when the agent is at the gold's location,
        after which the gold location is set to None.

        Returns
        -------
        None
        """
        if self.agent_alive and self.agent_location == self.gold_location:
            self.gold_location = None

    def climbed(self) -> None:
        """
        Attempt to climb out of the cave. The agent successfully climbs out if at the EXIT_LOCATION (1, 1),
        setting the agent location to None.

        Returns
        -------
        None
        """
        if self.agent_alive and self.agent_location == self.EXIT_LOCATION:
            self.agent_location = None

    def shot(self) -> None:
        """
        Shoot the arrow. If the arrow strikes the Wumpus, the Wumpus dies.

        Returns
        -------
        None
        """
        if (
            not self.agent_alive
            or self.agent_location is None
            or not self.wumpus_alive
            or self.wumpus_location is None
        ):
            return

        ax, ay = self.agent_location
        wx, wy = self.wumpus_location

        self.wumpus_alive = not any(
            [
                self.agent_direction == "East" and ay == wy and ax < wx,
                self.agent_direction == "West" and ay == wy and ax > wx,
                self.agent_direction == "North" and ax == wx and ay < wy,
                self.agent_direction == "South" and ax == wx and ay > wy,
            ]
        )

    def adjacent(
        self,
        location: Optional[Tuple[int, int]] = None,
        target: Optional[Tuple[int, int]] = None,
    ) -> bool:
        """
        Check if `location` is adjacent to `target` (i.e., one step in any cardinal direction).

        Parameters
        ----------
        location : Optional[Tuple[int, int]], optional
            The location to check, by default None.
        target : Optional[Tuple[int, int]], optional
            The target location to compare against, by default None.

        Returns
        -------
        bool
            True if the location is adjacent to the target, False otherwise.
        """
        if location is None or target is None:
            return False
        x1, y1 = location
        x2, y2 = target
        return abs(x1 - x2) + abs(y1 - y2) == 1

    def agent_bumped_wall(self) -> bool:
        """
        Check if the agent is facing a wall (i.e., cannot move in the current direction).

        Returns
        -------
        bool
            True if the agent bumped into a wall, False otherwise.
        """
        return bool(self.agent_location) and any(
            [
                self.agent_direction == "East" and not self.agent_can_move_east(),
                self.agent_direction == "West" and not self.agent_can_move_west(),
                self.agent_direction == "North" and not self.agent_can_move_north(),
                self.agent_direction == "South" and not self.agent_can_move_south(),
            ]
        )

    # Helper methods for movement
    def agent_can_move_east(self) -> bool:
        """
        Check if the agent can move east.

        Returns
        -------
        bool
            True if the agent can move east, False otherwise.
        """
        if self.agent_location is None:
            return False
        x, _ = self.agent_location
        return x < 4

    def agent_can_move_west(self) -> bool:
        """
        Check if the agent can move west.

        Returns
        -------
        bool
            True if the agent can move west, False otherwise.
        """
        if self.agent_location is None:
            return False
        x, _ = self.agent_location
        return x > 1

    def agent_can_move_north(self) -> bool:
        """
        Check if the agent can move north.

        Returns
        -------
        bool
            True if the agent can move north, False otherwise.
        """
        if self.agent_location is None:
            return False
        _, y = self.agent_location
        return y < 4

    def agent_can_move_south(self) -> bool:
        """
        Check if the agent can move south.

        Returns
        -------
        bool
            True if the agent can move south, False otherwise.
        """
        if self.agent_location is None:
            return False
        _, y = self.agent_location
        return y > 1

    def agent_bumped_wall(self) -> bool:
        """
        Checks if the agent bumped into a wall or is facing a wall.

        Returns
        -------
        bool
            True if the agent is facing a wall and cannot move forward, False otherwise.
        """
        return bool(self.agent_location) and any(
            [
                self.agent_direction == "East" and not self.agent_can_move_east(),
                self.agent_direction == "West" and not self.agent_can_move_west(),
                self.agent_direction == "North" and not self.agent_can_move_north(),
                self.agent_direction == "South" and not self.agent_can_move_south(),
            ]
        )

    def wumpus_east_of_agent(self) -> bool:
        """
        Checks if the Wumpus is located to the east of the agent.

        The Wumpus is considered to be east of the agent if its x-coordinate is greater than
        the agent's x-coordinate, and they share the same y-coordinate.

        Returns
        -------
        bool
            True if the Wumpus is east of the agent, False otherwise.
        """
        if self.agent_location is None or self.wumpus_location is None:
            return False
        ax, ay = self.agent_location
        wx, wy = self.wumpus_location
        return wx > ax and wy == ay

    def wumpus_west_of_agent(self) -> bool:
        """
        Checks if the Wumpus is located to the west of the agent.

        The Wumpus is considered to be west of the agent if its x-coordinate is less than
        the agent's x-coordinate, and they share the same y-coordinate.

        Returns
        -------
        bool
            True if the Wumpus is west of the agent, False otherwise.
        """
        if self.agent_location is None or self.wumpus_location is None:
            return False
        ax, ay = self.agent_location
        wx, wy = self.wumpus_location
        return wx < ax and wy == ay

    def wumpus_north_of_agent(self) -> bool:
        """
        Checks if the Wumpus is located to the north of the agent.

        The Wumpus is considered to be north of the agent if its y-coordinate is greater than
        the agent's y-coordinate, and they share the same x-coordinate.

        Returns
        -------
        bool
            True if the Wumpus is north of the agent, False otherwise.
        """
        if self.agent_location is None or self.wumpus_location is None:
            return False
        ax, ay = self.agent_location
        wx, wy = self.wumpus_location
        return wy > ay and wx == ax

    def wumpus_south_of_agent(self) -> bool:
        """
        Checks if the Wumpus is located to the south of the agent.

        The Wumpus is considered to be south of the agent if its y-coordinate is less than
        the agent's y-coordinate, and they share the same x-coordinate.

        Returns
        -------
        bool
            True if the Wumpus is south of the agent, False otherwise.
        """
        if self.agent_location is None or self.wumpus_location is None:
            return False
        ax, ay = self.agent_location
        wx, wy = self.wumpus_location
        return wy < ay and wx == ax
