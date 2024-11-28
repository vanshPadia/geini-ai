from app.llm.integration.integration_service import search_flights
from app.llm.schemas.chat_schema import GraphState
from app.llm.workflow.base_node import BaseNode
from app.configs import log


class SearchNode(BaseNode):
    def execute(self, gs: GraphState):
        source = gs.state.flight_search.source
        destination = gs.state.flight_search.destination

        search_results = search_flights(gs.state, gs.user_details.thread_id)
        
        if search_results and len(search_results["data"]["offers"]) > 0:
            origin_city_name = search_results['data']['offers'][0]['slices'][0]['origin']['city_name']
            origin_iata_code = search_results['data']['offers'][0]['slices'][0]['origin']['iata_city_code']
            destination_city_name = search_results['data']['offers'][0]['slices'][0]['destination']['city_name']
            destination_iata_code = search_results['data']['offers'][0]['slices'][0]['destination']['iata_city_code']

            if source.lower() == origin_city_name.lower() and destination.lower() == destination_city_name.lower():
                gs.should_continue = True
                gs.result.flights = search_results
                gs.result.hotels = None
            else:
                log.debug(f"Confirming source: {source}, originCityName: {origin_city_name}, destination: {destination} and destinationCityName: {destination_city_name} with user for threadId: {gs.user_details.thread_id}")
                message = f"Could you confirm if the source city is {origin_city_name}({origin_iata_code})and the destination city is {destination_city_name}({destination_iata_code})?"
                gs.result.reply_message = super().rephrase_validation_message(message, gs.user_details.thread_id)
        else:
            log.debug(f"No flights found for threadId: {gs.user_details.thread_id}")
            gs.result.reply_message = "No flights were found. Please try selecting different dates or locations"
