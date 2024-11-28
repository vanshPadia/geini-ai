from langchain_openai import ChatOpenAI
from app.configs import MODEL_NAME, MODEL_TEMPERATURE


class ModelProvider:
    __open_ai_model: ChatOpenAI = ChatOpenAI(model=MODEL_NAME, temperature=MODEL_TEMPERATURE)

    @staticmethod
    def get_openai_model():
        return ModelProvider.__open_ai_model
