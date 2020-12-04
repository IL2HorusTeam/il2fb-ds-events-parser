from .literals import HUMAN_AIRCRAFT_DELIM

from .literals import SWITCH_STATE_ON_LITERAL
from .literals import SWITCH_STATE_OFF_LITERAL


ACTOR_REGEX        = r"(?P<actor>.+)"
CHANNEL_NO_REGEX   = r"(?P<channel_no>\d+)"
HOST_REGEX         = r"(?P<host>.+)"
PORT_REGEX         = r"(?P<port>\d+)"
POS_REGEX          = r"(?P<x>-?\d+\.\d+) (?P<y>-?\d+\.\d+)( (?P<z>-?\d+\.\d+))?"
REASON_REGEX       = r"(?P<reason>.*)"
SWITCH_STATE_REGEX = rf"(?P<state>{SWITCH_STATE_ON_LITERAL}|{SWITCH_STATE_OFF_LITERAL})"

AIRCRAFT_REGEX     = r"(?P<aircraft>.+)"
CALLSIGN_REGEX     = r"(?P<callsign>.*)"
CREW_MEMBER_REGEX  = r"\((?P<crew_index>\d+)\)"

TARGET_AIRCRAFT_REGEX    = r"(?P<target_aircraft>.+)"
TARGET_CALLSIGN_REGEX    = r"(?P<target_callsign>.*)"
TARGET_CREW_MEMBER_REGEX = r"\((?P<target_crew_index>\d+)\)"

HUMAN_AIRCRAFT_REGEX             = rf"{CALLSIGN_REGEX}{HUMAN_AIRCRAFT_DELIM}{AIRCRAFT_REGEX}"
HUMAN_AIRCRAFT_CREW_MEMBER_REGEX = rf"{HUMAN_AIRCRAFT_REGEX}{CREW_MEMBER_REGEX}"

TARGET_HUMAN_AIRCRAFT_REGEX             = rf"{TARGET_CALLSIGN_REGEX}{HUMAN_AIRCRAFT_DELIM}{TARGET_AIRCRAFT_REGEX}"
TARGET_HUMAN_AIRCRAFT_CREW_MEMBER_REGEX = rf"{TARGET_HUMAN_AIRCRAFT_REGEX}{TARGET_CREW_MEMBER_REGEX}"
