from app.llm.schemas.chat_schema import GraphState
from app.llm.workflow.base_node import BaseNode
from app.llm.schemas.chat_schema import GraphState
from app.llm.workflow.base_node import BaseNode
from app.llm.prompts.manager_prompt import MANAGER_SYS_MESSAGE

from app.llm.workflow.base_node import BaseNode
from langchain_core.messages import HumanMessage, AIMessage
from app.llm.schemas.chat_schema import LLMManagerResult
from app.llm.schemas.enums import MessageCatergory
from app.common.errors import GenieBadException
from app.common.utilis import current_date, current_day

class ManagerNode(BaseNode):
    def execute(self, gs: GraphState):
        chat_history = []
        if gs.chat_history:
            chat_history = [HumanMessage(content=gs.chat_history[-1].human_message),
                            AIMessage(content=gs.chat_history[-1].ai_message if gs.chat_history[-1].ai_message else '')
                           ] if gs.chat_history else []

        chat_history.append(HumanMessage(content=gs.message))
        
        agent = super().create_agent(MANAGER_SYS_MESSAGE, LLMManagerResult, "chat_history")
        result: LLMManagerResult = agent.invoke({
            "current_date": current_date(),
            "current_day": current_day(),
            "chat_history": chat_history
        })
        
        gs.result.message_category = result.message_category

        if MessageCatergory.TRAVEL.value in result.message_category:
            gs.should_continue = True
        elif MessageCatergory.IRRELEVANT.value in result.message_category:
            raise GenieBadException(result.reply_message)
        else:
            gs.result.reply_message = result.reply_message

