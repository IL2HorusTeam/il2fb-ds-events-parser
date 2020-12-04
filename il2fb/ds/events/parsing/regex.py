from .literals import HUMAN_AIRCRAFT_DELIM

from .literals import SWITCH_STATE_ON_LITERAL
from .literals import SWITCH_STATE_OFF_LITERAL


ACTOR_REGEX      = r"(?P<actor>.+)"
AIRCRAFT_REGEX   = r"(?P<aircraft>.+)"
CALLSIGN_REGEX   = r"(?P<callsign>.*)"
CHANNEL_NO_REGEX = r"(?P<channel_no>\d+)"
HOST_REGEX       = r"(?P<host>.+)"
PORT_REGEX       = r"(?P<port>\d+)"
POS_REGEX        = r"(?P<x>-?\d+\.\d+) (?P<y>-?\d+\.\d+)( (?P<z>-?\d+\.\d+))?"
REASON_REGEX     = r"(?P<reason>.*)"

HUMAN_AIRCRAFT_REGEX = rf"{CALLSIGN_REGEX}{HUMAN_AIRCRAFT_DELIM}{AIRCRAFT_REGEX}"
SWITCH_STATE_REGEX   = rf"(?P<state>{SWITCH_STATE_ON_LITERAL}|{SWITCH_STATE_OFF_LITERAL})"
