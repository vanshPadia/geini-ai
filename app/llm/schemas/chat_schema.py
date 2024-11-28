from pydantic import BaseModel, Field
from typing import Optional, Any, Literal
from app.llm.schemas.enums import (
    TripWay,
    FlightStop,
    TimePeriod,
    FlightClass
)
from app.llm.schemas.refinement_schema import FlightRefinement


class FlightSearch(BaseModel):
    source: Optional[str] = Field(default=None, description="Source airport or city")
    destination: Optional[str] = Field(default=None, description="Destination airport or city")
    adults: Optional[int] = Field(default=None, description="Number of adult passengers")
    departure_date: Optional[str] = Field(default=None, description="Flight departure date")
    
    # Additional Flight Search
    children: Optional[int] = Field(default=None, description="Number of child passengers (aged 2-11)")
    infants: Optional[int] = Field(default=None, description="Number of infant passengers (under 2 years old)")
    return_date: Optional[str] = Field(default=None, description="Return date for a round-trip flight, if applicable")
    source_code: Optional[str] = Field(default=None, description="IATA code for the source airport")
    destination_code: Optional[str] = Field(default=None, description="IATA code for the destination airport")



class FlightPreferences(BaseModel):
    trip_way: Optional[TripWay] = Field(default=None, description="Type of trip (round-trip, one-way, multi-city)") #duplicate of flight_search.returnDate
    flight_stop: Optional[FlightStop] = Field(default=None, description="Type of flight stop (nonstop, onestop, multi)") #We need to update refinement.Stopover Details? or should we add one more field in allowed_layover
    departure_time: Optional[TimePeriod] = Field(default=None, description="Preferred time for departure") # can we define departure and arrival time range in refinement? same for below
    arrival_time: Optional[TimePeriod] = Field(default=None, description="Preferred time for arrival")
    flight_class: Optional[FlightClass] = Field(default=None, description="Preferred flight class (economy, premium_economy, business_class, first_class)") #integration.classType
    preferred_airlines: Optional[str] = Field(default=None, description="Preferred airlines for flight class") #refinement.operating_airline_name


class GenieState(BaseModel):
    flight_search: Optional[FlightSearch] = None


class UserDetails(BaseModel):
    user_id: int
    thread_id: int


class ChatResult(BaseModel):
    reply_message: Optional[str] = None
    message_category: Optional[str] = None
    thread_label: Optional[str] = None
    options: Optional[Any] = None
    hotels: Optional[Any] = None
    flights: Optional[Any] = None


class ChatHistory(BaseModel):
    human_message: Optional[str] = None
    ai_message: Optional[str] = None


class SelectedPreferences(BaseModel):
    airline_name: Optional[str] = Field(default=None, description="Name of the airline preferred by the user.")
    food_preferences: Optional[str] = Field(default=None, description="User's preferred food choice during the flight.")
    seat_preferences: Optional[str] = Field(default=None, description="User's preferred seat type (e.g., window, aisle, etc.).")
    allow_layovers: Optional[bool] = Field(default=None, description="Whether the user allows layovers during the flight.")


class TripHistory(BaseModel):
    id: int = None
    status: str = None
    state: FlightSearch = None
    selected_preferences: SelectedPreferences = None

    
class GraphState(BaseModel):
    message: str
    user_details: Optional[UserDetails] = None
    state: Optional[GenieState] = None
    flight_preferences: Optional[FlightPreferences] = None
    chat_history: Optional[list[ChatHistory]] = None
    flight_refinement: Optional[FlightRefinement] = None
    trip_history: Optional[list[TripHistory]] = None
    result: Optional[ChatResult] = None
    should_continue: Optional[bool] = False


class LLMPreSearchResult(BaseModel):
    reply_message: Optional[str] = Field(default=None, description="Reply message or follow-up questions to user")
    flight_search: Optional[FlightSearch] = Field(default=None, description="Flight details provided by the user, such as source, destination, number of passengers, travel date, number of children, infants, or return date for a round-trip flight")


class LLMManagerResult(BaseModel):
    message_category: Optional[Literal['GREETINGS', 'TRAVEL', 'IRRELEVANT']] = Field(default=None, description="Category of the user message: GREETINGS, TRAVEL, or IRRELEVANT")
    reply_message: Optional[str] = Field(default=None, description="Follow-up question or response to the user")


class LLMValidationResult(BaseModel):
    message: Optional[str] = Field(default=None, description="Rephrased validation error message")


class LLMIataResult(BaseModel):
    source_iata_code: Optional[str] = Field(default=None, description="The IATA code of the source airport")
    destination_iata_code: Optional[str] = Field(default=None, description="The IATA code of the destination airport")
