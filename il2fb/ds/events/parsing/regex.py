from .literals import HUMAN_AIRCRAFT_DELIM

ACTOR_REGEX      = r"(?P<actor>.+)"
AIRCRAFT_REGEX   = r"(?P<aircraft>.+)"
CALLSIGN_REGEX   = r"(?P<callsign>.*)"
CHANNEL_NO_REGEX = r"(?P<channel_no>\d+)"
HOST_REGEX       = r"(?P<host>.+)"
PORT_REGEX       = r"(?P<port>\d+)"
POS_REGEX        = r"(?P<x>-?\d+\.\d+) (?P<y>-?\d+\.\d+)( (?P<z>-?\d+\.\d+))?"
REASON_REGEX     = r"(?P<reason>.*)"

HUMAN_AIRCRAFT_REGEX = rf"{CALLSIGN_REGEX}{HUMAN_AIRCRAFT_DELIM}{AIRCRAFT_REGEX}"
