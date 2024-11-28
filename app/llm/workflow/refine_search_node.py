from app.llm.schemas.chat_schema import GraphState
from app.llm.workflow.base_node import BaseNode


class RefineSearchNode(BaseNode):
    def execute(self, gs: GraphState):
        gs.should_continue = True

        self.__prepare_reply_message(gs)

        flight_search_result = gs.result.flights
        offers = flight_search_result["data"]["offers"]

        total_flights = len(offers)

        gs.result.flights = {
            "total_flights": total_flights,
            "best_flight": offers[0],
            "cheapest_flight": offers[1 if total_flights > 1 else 0],
            "fastest_flight": offers[2 if total_flights > 2 else 0]
        }

    def __prepare_reply_message(self, gs: GraphState):
        filtered_refinement = {key: value for key, value in gs.flight_refinement.model_dump().items() if value is not None}

        gs.result.reply_message = (
            f"Refinement is currently in progress. "
            f"Below are some flight options for your search: {gs.state.flight_search.model_dump()} and refinement: {filtered_refinement}"
        )