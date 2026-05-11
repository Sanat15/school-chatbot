import sys
import os

_api_dir = os.path.dirname(os.path.abspath(__file__))
_root_dir = os.path.dirname(_api_dir)

# On Vercel the build command copies backend/ into api/backend/, so _api_dir
# contains the backend package. Locally backend/ lives at the project root.
for _p in [_api_dir, _root_dir]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from backend.main import app  # noqa: F401, E402
