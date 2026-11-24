"""Swarms of local agents on the math and logic problems of Self-Organizing Agent Teams. See README.md and CURRENT.md.

    from mathswarm import Arm, RandomLooks      # what an experiment file needs
"""
from swarm_engine import Sampling

from .looks import RandomLooks
from .swarm import Arm, play

__all__ = ["Arm", "play", "Sampling", "RandomLooks"]
