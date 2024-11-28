from app.llm.schemas.chat_schema import GraphState
from app.llm.workflow.base_node import BaseNode
from app.llm.prompts.presearch_prompt import PRESEARCH_SYS_MESSAGE
from app.llm.schemas.chat_schema import LLMPreSearchResult
from app.llm.schemas.chat_schema import FlightSearch
from app.llm.schemas.chat_schema import LLMPreSearchResult
from app.llm.schemas.chat_schema import FlightSearch, LLMIataResult
from app.common import flight_validator
from app.configs import log
from app.common.utilis import current_date, current_day
from app.llm.prompts.iata_code_validator_prompt import (
    IATA_CODE_VALIDATION_SYS_MESSAGE_SOURCE_DESTINATION,
    IATA_CODE_VALIDATION_SYS_MESSAGE_SOURCE,
    IATA_CODE_VALIDATION_SYS_MESSAGE_DESTINATION
)


class PreSearchNode(BaseNode):
    def execute(self, gs: GraphState):
        agent = super().create_agent(PRESEARCH_SYS_MESSAGE, LLMPreSearchResult, "chat_history")
        result: LLMPreSearchResult = agent.invoke({
            "current_date": current_date(),
            "current_day": current_day(),
            "chat_history": self.get_user_chat_history(gs)
        })
        
        gs.result.reply_message = result.reply_message
        log.debug(f'Get reply message: {result.reply_message} from LLM for threadId: {gs.user_details.thread_id}')
        
        flight_validator.replace_null_or_unknown_with_none(result.flight_search)
        
        if not result.flight_search.source_code or not result.flight_search.destination_code:
            self.__handle_iata_code_validation(result)

        self.__update_state_from_llm_result(gs, result)

        if not result.reply_message and self.__custom_validation(gs):
            gs.should_continue = True

    def __handle_iata_code_validation(self, result: LLMPreSearchResult):       
        if (result.flight_search.source and result.flight_search.destination and 
            not result.flight_search.source_code and not result.flight_search.destination_code
        ):
            agent = super().create_agent(IATA_CODE_VALIDATION_SYS_MESSAGE_SOURCE_DESTINATION, LLMIataResult)
            iata_result: LLMIataResult = agent.invoke({
                "source": result.flight_search.source,
                "destination": result.flight_search.destination
            })            
            
            result.flight_search.source_code = iata_result.source_iata_code
            result.flight_search.destination_code = iata_result.destination_iata_code
        
        elif result.flight_search.source and not result.flight_search.source_code:
            agent = super().create_agent(IATA_CODE_VALIDATION_SYS_MESSAGE_SOURCE, LLMIataResult)
            iata_result_source: LLMIataResult = agent.invoke({
                "source": result.flight_search.source
            })

            result.flight_search.source_code = iata_result_source.source_iata_code
        
        elif result.flight_search.destination and not result.flight_search.destination_code:
            agent = super().create_agent(IATA_CODE_VALIDATION_SYS_MESSAGE_DESTINATION, LLMIataResult)
            iata_result_destination: LLMIataResult = agent.invoke({
                "destination": result.flight_search.destination
            })

            result.flight_search.destination_code = iata_result_destination.destination_iata_code

    def __update_state_from_llm_result(self, gs: GraphState, result: LLMPreSearchResult):
        if result.flight_search:
            asc = gs.state.flight_search.model_dump() if gs.state.flight_search else {}
            asc.update({key: value for key, value in result.flight_search.model_dump().items() if value})
            gs.state.flight_search = FlightSearch(**asc)

    def __custom_validation(self, gs: GraphState):
        flight_validations_message = self.__flight_validations(gs)
        if flight_validations_message:    
            gs.result.reply_message = flight_validations_message
            return False
        else:
            return True
        
    def __flight_validations(self, gs: GraphState):
        thread_id = gs.user_details.thread_id
        departure_date = gs.state.flight_search.departure_date
        adults = gs.state.flight_search.adults
        source = gs.state.flight_search.source
        children = gs.state.flight_search.children
        infants = gs.state.flight_search.infants
        destination = gs.state.flight_search.destination

        validation_message = flight_validator.validate_required_fields(source, destination, departure_date, adults)
        
        if validation_message:
            return super().rephrase_validation_message(validation_message, thread_id)

        validation_message = flight_validator.validate_source_destination(source, destination)
        if validation_message:
            return super().rephrase_validation_message(validation_message, thread_id)

        validation_message = flight_validator.validate_source_destination_codes(gs.state.flight_search.source_code, 
                                                                                gs.state.flight_search.destination_code)
        if validation_message:
            return super().rephrase_validation_message(validation_message, thread_id)

        validation_message = flight_validator.validate_departure_date(departure_date, current_date())
        if validation_message:
            return super().rephrase_validation_message(validation_message, thread_id)
        
        validation_message = flight_validator.validate_return_date(gs.state.flight_search.return_date, departure_date)
        if validation_message:
            return super().rephrase_validation_message(validation_message, thread_id)
        
        validation_message = flight_validator.validate_max_passengers(adults, children, infants)
        if validation_message:
            return super().rephrase_validation_message(validation_message, thread_id)

        validation_message = flight_validator.negative_passenger_check(adults, children, infants)
        if validation_message:
            return super().rephrase_validation_message(validation_message, thread_id)
        
        return None
