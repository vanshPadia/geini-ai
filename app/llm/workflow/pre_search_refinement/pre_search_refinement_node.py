from app.llm.schemas.chat_schema import GraphState, FlightPreferences, TripHistory, SelectedPreferences
from app.llm.workflow.base_node import BaseNode
from app.llm.prompts.pre_search_refinement_prompt import PRESEARCH_REFINEMENT_SYS_MESSAGE
from app.llm.prompts.trip_preferences_prompt import TRIP_PREFERENCES_SYS_MESSAGE
from app.llm.schemas.refinement_schema import FlightRefinement
from app.configs import log
from app.llm.workflow.pre_search_refinement.pre_search_refinement_helper import get_filtered_schema, populate_null_fields
from app.llm.schemas.enums import FlightStop
from app.llm.schemas.pre_search_schema import TripPreferences


class PreSearchRefinementNode(BaseNode):
    def execute(self, gs: GraphState):
        refinement = self.__extract_refinement_from_chat_history(gs)

        refine_preferences: FlightRefinement = self.__extract_refinement_from_preferences(gs.flight_preferences)
        populate_null_fields(refinement, refine_preferences)

        refine_trip_history: FlightRefinement = self.__extract_refinement_from_trip_history(gs.trip_history, 
                                                    gs.state.flight_search.source, gs.state.flight_search.destination)
        populate_null_fields(refinement, refine_trip_history)

        gs.flight_refinement = refinement

        log.debug(f'Populated refinement: {refinement} from refine_preferences: {refine_preferences} and refine_trip_history: {refine_trip_history} for threadId: {gs.user_details.thread_id}')

    def __extract_refinement_from_chat_history(self, gs: GraphState):
        agent = super().create_agent(PRESEARCH_REFINEMENT_SYS_MESSAGE, FlightRefinement, "chat_history")
        result: FlightRefinement = agent.invoke({
            "chat_history": self.get_user_chat_history(gs),
            "flight_refinement_schema": get_filtered_schema(FlightRefinement)
        })

        return result

    def __extract_refinement_from_preferences(self, preferences: FlightPreferences):
        if preferences:
            refinement = FlightRefinement()

            if preferences.flight_stop:
                refinement.allow_layovers = preferences.flight_stop.value != FlightStop.NON_STOP.value
            if preferences.departure_time:
                refinement.preferred_departure_time = preferences.departure_time.value
            if preferences.arrival_time:
                refinement.preferred_arrival_time = preferences.arrival_time.value
            if preferences.preferred_airlines:
                refinement.operating_airline_name = preferences.preferred_airlines
            if preferences.flight_class:
                refinement.cabin_class_marketing_name = preferences.flight_class.value
            return refinement
        
    def __extract_refinement_from_trip_history(self, trip_history: list[TripHistory], new_source: str, new_destination: str):
        if trip_history:
            input_data = []
            for trip in trip_history:
                trip_preferences = TripPreferences(
                    source=trip.state.source,
                    destination=trip.state.destination,
                    selected_preferences=SelectedPreferences(
                        airline_name=trip.selected_preferences.airline_name,
                        food_preferences=trip.selected_preferences.food_preferences,
                        seat_preferences=trip.selected_preferences.seat_preferences,
                        allow_layovers=trip.selected_preferences.allow_layovers,
                    ),
                )
                input_data.append(trip_preferences.model_dump_json())

            agent = super().create_agent(TRIP_PREFERENCES_SYS_MESSAGE, SelectedPreferences, "trip_preferences")
            result: SelectedPreferences = agent.invoke({
                "trip_preferences": input_data,
                "selected_preferences_schema": get_filtered_schema(SelectedPreferences),
                "new_source": new_source,
                "new_destination": new_destination
            })

            refinement = FlightRefinement(
                allow_layovers=result.allow_layovers,
                operating_airline_name=result.airline_name,
                cabin_seat_type_description=result.seat_preferences
                # TODO: Pending to set 'food_preferences' in refinement
            )
            
            return refinement


