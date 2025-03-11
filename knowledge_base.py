from wumpus_world_agent import WumpusWorldAgent
from wumpus_world import WumpusWorld
from typing import Tuple, Set, Dict, Optional, List, Callable
from collections import deque

# Type aliases for clarity
Location = Tuple[int, int]  # Represents a grid location (x, y)
Percept = Tuple[str, str, str, str, str]  # (stench, breeze, glitter, bump, scream)


class KnowledgeBase:
    """
    A knowledge base for tracking and reasoning about the Wumpus World environment.
    
    Attributes
    ----------
    all_locations : Set[Location]
        A set containing all possible locations in the 4x4 grid.
    EXIT_LOCATION : Location
        The exit location (1,1) in the grid.
    percepts : Dict[Location, Tuple[Percept, int]]
        Stores percepts observed at specific locations along with the time step.
    visited : Set[Location]
        Locations that have been visited by the agent.
    safe_locations : Set[Location]
        Locations inferred to be safe.
    stench_locations : Set[Location]
        Locations where a stench has been perceived.
    no_stench_locations : Set[Location]
        Locations confirmed to have no stench.
    possible_wumpus_locations : Set[Location]
        Locations that may contain the Wumpus.
    no_wumpus_locations : Set[Location]
        Locations confirmed to not contain the Wumpus.
    _wumpus_location : Optional[Location]
        The inferred exact location of the Wumpus if determinable.
    no_pit_locations : Set[Location]
        Locations confirmed to not contain pits.
    possible_pit_locations : Set[Location]
        Locations that may contain pits.
    gold_location : Optional[Location]
        The inferred location of the gold if known.
    wumpus_alive : bool
        Whether the Wumpus is still alive.
    has_arrow : bool
        Whether the agent still has the arrow.
    has_gold : bool
        Whether the agent has picked up the gold.
    agent_location : Location
        The current location of the agent.
    agent_direction : str
        The current facing direction of the agent (North, East, South, West).
    previous_location : Optional[Location]
        The previous location of the agent.
    """
    all_locations: Set[Location] = {(i, j) for i in range(1, 5) for j in range(1, 5)}
    EXIT_LOCATION: Location = (1, 1)

    def __init__(self) -> None:
        """
        Initialize the knowledge base with storage for percepts and inferred knowledge.
        """
        self.percepts: Dict[Location, Tuple[Percept, int]] = {}
        self.visited: Set[Location] = {self.EXIT_LOCATION}
        self.safe_locations: Set[Location] = {self.EXIT_LOCATION}
        self.stench_locations: Set[Location] = set()
        self.no_stench_locations: Set[Location] = set()
        self.possible_wumpus_locations: Set[Location] = self.all_locations - {self.EXIT_LOCATION}
        self.no_wumpus_locations: Set[Location] = {self.EXIT_LOCATION}
        self._wumpus_location: Optional[Location] = None
        self.no_pit_locations: Set[Location] = {self.EXIT_LOCATION}
        self.possible_pit_locations: Set[Location] = set()
        self.gold_location: Optional[Location] = None
        self.wumpus_alive: bool = True
        self.has_arrow: bool = True
        self.has_gold: bool = False
        self.agent_location: Location = self.EXIT_LOCATION
        self.agent_direction: str = 'East'
        self.previous_location: Optional[Location] = None

    def tell(self, sentence: Tuple) -> None:
        """
        Updates the knowledge base with new percepts or actions.

        Parameters
        ----------
        sentence : Tuple
            Either an action or percept tuple to update the knowledge base.
        """
        if not sentence:
            return

        # Handle action update
        if len(sentence) == 2 and callable(sentence[0]):
            action, _ = sentence
            self._update_agent_state(action)
            return

        # Handle percept update
        if len(sentence) == 2 and isinstance(sentence[0], tuple):
            percept, time = sentence
            stench, breeze, glitter, bump, scream = percept

            current_location = self.agent_location

            # Record percepts and update state
            self.visited.add(self.agent_location)
            self.safe_locations.add(self.agent_location)
            self.no_pit_locations.add(self.agent_location)
            self.no_wumpus_locations.add(self.agent_location)
            self.percepts[self.agent_location] = (percept, time)

            # Perform inferences
            self._infer_pits(breeze)
            self._infer_wumpus_location_from_stench(stench)

            if glitter == "Glitter" and not self.has_gold:
                self.gold_location = current_location

            elif glitter != "Glitter":
                self.gold_location = None

            if scream == "Scream":
                self.wumpus_alive = False
                self.possible_wumpus_locations.clear()

            self.previous_location = current_location

    def _update_agent_state(self, action: Callable) -> None:
        """
        Update the agent's position and direction based on the given action.

        Parameters
        ----------
        action : Callable
            The action performed by the agent, which may involve movement, turning, or grabbing gold.
        """
        if action == WumpusWorldAgent.move_forward:
            x, y = self.agent_location
            delta = {
                'East': (1, 0), 'West': (-1, 0),
                'North': (0, 1), 'South': (0, -1)
            }[self.agent_direction]
            new_loc = (x + delta[0], y + delta[1])
            if new_loc in self.all_locations:
                self.agent_location = new_loc

        if action == WumpusWorldAgent.grab:
            self.has_gold = True

        elif action == WumpusWorldAgent.turn_left:
            dirs = ['North', 'West', 'South', 'East']
            self.agent_direction = dirs[(dirs.index(self.agent_direction) + 1) % 4]

        elif action == WumpusWorldAgent.turn_right:
            dirs = ['North', 'East', 'South', 'West']
            self.agent_direction = dirs[(dirs.index(self.agent_direction) + 1) % 4]

    def ask(self, query: Tuple[str, int]) -> Optional[Callable]:
        """
        Determines the next best action based on the current knowledge.
        
        Parameters
        ----------
        query : Tuple[str, int]
            A query specifying the type of information needed.

        Returns
        -------
        Optional[Callable]
            The best action for the agent to take based on knowledge.
        """
        if self.has_gold:
            if self.agent_location == self.EXIT_LOCATION:
                return WumpusWorldAgent.climb
            return self._navigate_to(self.EXIT_LOCATION)

        if self.gold_location == self.agent_location and not self.has_gold:
            return WumpusWorldAgent.grab

        if self._should_shoot():
            self.has_arrow = False
            return WumpusWorldAgent.shoot

        return self._explore_safe()


    def _navigate_to(self, target: Location) -> Optional[Callable]:
        """
        Get action to move towards target location using pathfinding.

        Parameters
        ----------
        target : Location
            The desired destination location.

        Returns
        -------
        Optional[Callable]
            The next action to move towards the target, or None if no path is found.
        """       
        # Already at target
        if self.agent_location == target:
            return None
        
        # Check direct adjacent path first
        adj = [loc for loc in self._get_adjacent(self.agent_location) 
            if loc in self.safe_locations]        
        # Direct path available
        if target in adj:
            return self._next_action_toward_target(target)
        
        # Find full path using BFS through safe locations
        path = self._find_path_to(target)
        if not path:
            return None
        
        next_step = path[0]
        return self._next_action_toward_target(next_step)

    def _find_path_to(self, target: Location) -> List[Location]:
        """
        Perform BFS pathfinding through safe visited locations.

        Parameters
        ----------
        target : Location
            The desired destination location.

        Returns
        -------
        List[Location]
            The path to the target location, or an empty list if no path exists.
        """
        
        start = self.agent_location
        visited = set()
        queue = deque()
        queue.append((start, []))
        
        while queue:
            current, path = queue.popleft()
            if current == target:
                return path
            if current in visited:
                continue
            visited.add(current)
            
            # Only move through safe, visited locations
            for neighbor in self._get_adjacent(current):
                if (neighbor in self.safe_locations and 
                    neighbor in self.visited and 
                    neighbor not in visited):
                    queue.append((neighbor, path + [neighbor]))
        
        return []

    def _should_shoot(self) -> bool:
        """
        Determine if shooting conditions are met.

        Returns
        -------
        bool
            True if shooting is advisable, otherwise False.
        """
        return (self.wumpus_alive and self.has_arrow and
                self.wumpus_location and
                self._is_in_line_of_sight())

    @property
    def safe_locations(self) -> None:
        """Update safe locations based on current knowledge."""
        if not self.wumpus_alive:
            self._safe_locations = self.no_pit_locations.copy()
        else:
            self._safe_locations = (self.no_pit_locations - self.possible_wumpus_locations).copy()
        return self._safe_locations
    
    @safe_locations.setter
    def safe_locations(self, value):
        self._safe_locations = value


    @property
    def wumpus_location(self) -> Optional[Location]:
        """Get inferred Wumpus location if uniquely determined."""
        if self._wumpus_location is None and len(self.possible_wumpus_locations) == 1:
            self._wumpus_location = next(iter(self.possible_wumpus_locations))
        return self._wumpus_location

    def _infer_pits(self, breeze: str) -> None:
        """
        Updates possible pit locations based on the presence or absence of a breeze.
        
        Parameters
        ----------
        breeze  str
            The breeze percept received at the current location.
        """
        adjacent = self._get_adjacent(self.agent_location)
        if breeze == "Breeze":
            for adj_loc in adjacent:
                if adj_loc not in self.no_pit_locations:
                    self.possible_pit_locations.add(adj_loc)
        else:
            for adj_loc in adjacent:
                self.no_pit_locations.add(adj_loc)
                self.possible_pit_locations.discard(adj_loc)

    def _infer_wumpus_location_from_stench(self, stench: str) -> None:
        """
        Updates possible Wumpus locations based on the presence or absence of a stench.
        
        Parameters
        ----------
        stench : str
            The stench percept received at the current location.
        """
        if stench != "Stench":
            self.no_stench_locations.add(self.agent_location)
            for adj in self._get_adjacent(self.agent_location):
                self.no_wumpus_locations.add(adj)
                self.possible_wumpus_locations.discard(adj)
        else:
            self.stench_locations.add(self.agent_location)
            possible = set.intersection(*(self._get_adjacent(s) for s in self.stench_locations))
            self.possible_wumpus_locations = possible - self.no_wumpus_locations


    def update_after_action(self, action: Callable) -> None:
        """
        Update the agent's state after performing an action.

        Parameters
        ----------
        action : Callable
            The action performed by the agent.
        """
        if action == WumpusWorldAgent.grab:
            if self.gold_location == self.agent_location:  # Changed condition
                self.has_gold = True
                self.gold_location = None
        elif action == WumpusWorldAgent.shoot:
            self.has_arrow = False

    def _get_adjacent(self, location: Location) -> Set[Location]:
        """
        Returns adjacent valid locations within the 4x4 grid.
        
        Parameters
        ----------
        location : Location
            The current location in the grid.
        
        Returns
        -------
        Set[Location]
            A set of adjacent locations.
        """
        x, y = location
        return {(x+dx, y+dy) for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)] 
                if 1 <= x+dx <= 4 and 1 <= y+dy <= 4}

    def _direction_to(self, target: Location) -> str:
        """
        Determines the direction from the current location to a target location.
        
        Parameters
        ----------
        target : Location
            The target location in the grid.
        
        Returns
        -------
        str
            The direction towards the target (North, East, South, or West).
        """
        cx, cy = self.agent_location
        tx, ty = target
        if tx > cx: return 'East'
        if tx < cx: return 'West'
        if ty > cy: return 'North'
        return 'South'

    def _next_action_toward_target(self, target: Location) -> Optional[Callable]:
        """Get action required to move towards an adjacent target."""
        desired_dir = self._direction_to(target)
        if desired_dir == self.agent_direction:
            return WumpusWorldAgent.move_forward
        dirs = ['North', 'East', 'South', 'West']
        current_idx = dirs.index(self.agent_direction)
        target_idx = dirs.index(desired_dir)
        return (WumpusWorldAgent.turn_right if (target_idx - current_idx) % 4 == 1 
                else WumpusWorldAgent.turn_left)

    def _is_in_line_of_sight(self) -> bool:
        """
        Check if the Wumpus is in a direct line of sight for shooting.

        Returns
        -------
        bool
            True if the Wumpus is directly in line with the agent, otherwise False.
        """
        if not self.wumpus_location:
            return False
        wx, wy = self.wumpus_location
        ax, ay = self.agent_location
        return (
            (self.agent_direction == 'East' and ay == wy and ax < wx) or
            (self.agent_direction == 'West' and ay == wy and ax > wx) or
            (self.agent_direction == 'North' and ax == wx and ay < wy) or
            (self.agent_direction == 'South' and ax == wx and ay > wy)
        )

    def _explore_safe(self) -> Optional[Callable]:
        """
        Choose the safest exploration move from adjacent safe locations.

        Returns
        -------
        Optional[Callable]
            The next action to take, or None if no safe move is available.
        """
        safe_unvisited = (self.safe_locations - self.visited).copy()
        for loc in safe_unvisited:
            if loc in self._get_adjacent(self.agent_location):
                return self._next_action_toward_target(loc)

        candidates = [loc for loc in self._get_adjacent(self.agent_location) 
                     if loc in self.safe_locations]
        if not candidates:
            return None

        location_scores = []
        for candidate in candidates:
            danger = sum(0.2 if n in self.possible_pit_locations else 
                        0.3 if n in self.possible_wumpus_locations else 0 
                        for n in self._get_adjacent(candidate))
            location_scores.append((candidate, 1.0 - danger*0.25))

        best = max(location_scores, key=lambda x: x[1])[0]
        return self._next_action_toward_target(best)