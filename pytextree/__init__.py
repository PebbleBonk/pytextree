"""Create a tree object from a LaTeX project."""

__version__ = "0.1.1"
__author__ = "Olli Riikonen"
__author_email__ = "pebblebonk@gmail.com"
__description__ = """Create a tree object from a LaTeX project."""
__url__ = "https://github.com/c0fec0de/anytree"

from .node import TNode, TEnv
from .tex_walker import parse_tex_to_tree
from .tex_walker import open_tex_project
from .tex_walker import find_environments
from .tex_walker import find_sections
