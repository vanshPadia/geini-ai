from app.api.schemas.chat_schema import ChatRequestPayload, ChatResponse
from app.llm.schemas.chat_schema import (
    GenieState,
    FlightSearch,
    ChatResult
)
from app.llm.schemas.enums import MessageCatergory
from app.llm.workflow import init_workflow
from app.configs import log, LANGFUSE_USER_NAME, ENABLED_LANGFUSE_METRICS
from langfuse.callback import CallbackHandler


workflow = init_workflow()

def chat_with_ai(payload: ChatRequestPayload):
    log.debug(f'Start: chat_with_ai for userId: {payload.user_details.user_id} and threadId: {payload.user_details.thread_id} with payload: {payload}')

    configs = {
        "configurable": {
            "thread_id": payload.user_details.thread_id,
        },
        "callbacks": [CallbackHandler(user_id=LANGFUSE_USER_NAME)]
    }
    if not ENABLED_LANGFUSE_METRICS:
        configs.pop("callbacks", None)

    workflow_output = workflow.invoke(
        {
            "message": payload.message,
            "user_details": payload.user_details,
            "state": GenieState(flight_search=FlightSearch()),
            "flight_preferences": payload.flight_preferences,
            "chat_history": payload.chat_history, #Thread's chat history in ascending order by created date - oldest to newest messages
            "trip_history": payload.trip_history,
            "result": ChatResult(),
        },
        configs
    )

    response = __prepare_chat_response(workflow_output)

    log.debug(f'End: chat_with_ai for userId: {payload.user_details.user_id} and threadId: {payload.user_details.thread_id} with response: {response}')
    return response


def __prepare_chat_response(workflow_output):
    workflow_output_dict = dict(workflow_output)

    result: ChatResult = workflow_output_dict["result"]
    state: GenieState = workflow_output_dict["state"]

    state = GenieState(flight_search=state.flight_search)

    thread_label = None
    if MessageCatergory.TRAVEL.value in result.message_category and state.flight_search.source_code and state.flight_search.destination_code:
        thread_label = f'{state.flight_search.source_code} to {state.flight_search.destination_code}'

    result = ChatResult(reply_message=result.reply_message, 
                        message_category=result.message_category,
                        thread_label=thread_label, 
                        options=result.options, 
                        flights=result.flights, 
                        hotels=result.hotels)

    return ChatResponse(state=state, result=result)
