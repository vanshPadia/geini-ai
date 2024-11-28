from pydantic import BaseModel
from app.llm.schemas.chat_schema import SelectedPreferences


class TripPreferences(BaseModel):
    source: str
    destination: str
    selected_preferences: SelectedPreferences
