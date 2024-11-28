from enum import Enum, auto

class MessageCatergory(Enum):
    GREETINGS = "GREETINGS"
    IRRELEVANT = "IRRELEVANT"
    TRAVEL = "TRAVEL"


class GenieNodes(Enum):
    MANAGER_NODE = "manager_node"
    PRE_SEARCH_NODE = "pre_search_node"
    PRE_SEARCH_REFINEMENT_NODE = "pre_search_refinement_node"
    SEARCH_NODE = "search_node"
    REFINE_SEARCH_NODE = "refine_search_node"  

    
class TripWay(Enum):
    ROUND_TRIP = "ROUND_TRIP"
    ONE_WAY = "ONE_WAY"
    MULTI_CITY = "MULTI_CITY"    
    
   
class FlightStop(Enum): 
    NON_STOP = "NON_STOP"
    ONE_STOP = "ONE_STOP"
    MULTI_STOP = "MULTI_STOP" 

  
class TimePeriod(Enum):
    MORNING = "MORNING"
    AFTERNOON = "AFTERNOON"
    EVENING = "EVENING"   


class FlightClass(Enum):
    ECONOMY = "ECONOMY"
    PREMIUM_ECONOMY = "PREMIUM_ECONOMY"
    BUSINESS_CLASS = "BUSINESS_CLASS"
    FIRST_CLASS = "FIRST_CLASS" 


class PassengerType(str, Enum):
    ADULT = "adult"
    CHILD = "child"
    INFANT_WITHOUT_SEAT = "infant_without_seat" 