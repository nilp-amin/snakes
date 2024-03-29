# fix ModuleNotFoundError
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from .world import World
from .manager import ScoreManager
from .boundry import Boundry, Wall
from .apple import Apple
from .snake import Snake, SnakeChunk, Head, Body, Tail