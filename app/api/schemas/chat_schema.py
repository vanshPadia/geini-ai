from typing import Any, Optional
from pydantic import BaseModel

from app.llm.schemas.chat_schema import ChatResult, GenieState, UserDetails, ChatHistory, TripHistory
from app.llm.schemas.chat_schema import FlightPreferences

class ChatRequestPayload(BaseModel):
    message: str
    user_details: UserDetails
    state: Optional[GenieState] = None
    flight_preferences: Optional[FlightPreferences] = None
    chat_history: Optional[list[ChatHistory]] = None
    trip_history: Optional[list[TripHistory]] = None


class ChatResponse(BaseModel):
    state: GenieState
    result: ChatResult
    