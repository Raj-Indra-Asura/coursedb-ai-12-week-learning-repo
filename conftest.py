"""Root pytest configuration.

Ensures the repository root is importable so that both ``app`` and
``dbms_internals`` packages resolve regardless of the test's location.
"""

import os
import sys

_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
