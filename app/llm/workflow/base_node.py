from app.llm.schemas.chat_schema import GraphState
from abc import ABC, abstractmethod
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.configs import log
from app.common.utilis import current_time_in_ms
from app.llm.models.model_provider import ModelProvider
from langchain_core.messages import HumanMessage, AIMessage
from app.llm.prompts.flight_validation_prompt import FLIGHT_VALIDATION_SYS_MESSAGE
from app.llm.schemas.chat_schema import LLMValidationResult
from langchain_core.messages import HumanMessage


class BaseNode(ABC):
    def apply(self, gs: GraphState, node: str) -> GraphState:
        time = current_time_in_ms()

        try:
            log.info(f'Start: {node} for userId: {gs.user_details.user_id}, threadId: {gs.user_details.thread_id}')

            gs.should_continue = False
            self.execute(gs)

            log.info(f'End: {node} for userId: {gs.user_details.user_id}, threadId: {gs.user_details.thread_id} in {current_time_in_ms() - time} ms')
            return gs
        except Exception as ex:
            log.error(f"FAILED: {node} for user: {gs.user_details.user_id}, threadId: {gs.user_details.thread_id} in {current_time_in_ms() - time} ms with state: {gs} and error: {str(ex)}")
            raise ex

    def create_agent(self, prompt: str, pydantic_model: any, *placeholders: str):
        messages = [("system", prompt)]

        for placeholder in placeholders:
            messages.append(MessagesPlaceholder(variable_name=placeholder))

        prompt_template = ChatPromptTemplate.from_messages(messages)
        
        return prompt_template | ModelProvider.get_openai_model().with_structured_output(pydantic_model)

    def get_model_provider() -> ModelProvider:
        return ModelProvider

    def get_user_chat_history(self, gs):
        chat_history = []
        if gs.chat_history:
            for chat in gs.chat_history:
                chat_history.append(HumanMessage(content=chat.human_message))
                chat_history.append(
                    AIMessage(content=chat.ai_message if chat.ai_message else ''))

        chat_history.append(HumanMessage(content=gs.message))
        return chat_history

    def rephrase_validation_message(self, validation_message: str, thread_id: int):
        log.debug(f'Rephrasing validation message: {validation_message} for threadId: {thread_id}')

        agent = self.create_agent(FLIGHT_VALIDATION_SYS_MESSAGE, LLMValidationResult, "message")
        result: LLMValidationResult = agent.invoke({
            "message": [HumanMessage(content=validation_message)]
        })

        return result.message
    
    ############ Abstract methods ############
    
    @abstractmethod
    def execute(self, gs: GraphState):
        pass