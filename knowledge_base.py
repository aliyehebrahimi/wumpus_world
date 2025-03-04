# KnowledgeBase
# A knowledge base for a knowledge-based agent.
# Aliyeh Ebrahimi

from wumpus_world_agent import WumpusWorldAgent
from typing import Callable, Any


class KnowledgeBase:
    def tell(self, sentence: Any) -> None:
        """
        Add a percept sentence to the knowledge base.

        Parameters
        ----------
        sentence : Any
            The percept sentence to add to the knowledge base.
        """
        return None
        # Future logic for processing the sentence can be added here.

    def ask(self, query: Any) -> Callable:
        """
        Get an action based on the current world state.

        Parameters
        ----------
        query : Any
            The query about the world state.

        Returns
        -------
        Callable
            The action the agent should take (defaults to climb).
        """
        return WumpusWorldAgent.climb
