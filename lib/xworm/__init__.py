from . import intelligence
from . import attack

submodules = {"ATTACK":attack}
funcs      = {"scanfile":
              {'f':intelligence.scan,"arglen":1}}
