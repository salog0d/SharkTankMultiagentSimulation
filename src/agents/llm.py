from src.core.settings import settings
from langchain_openai import AzureChatOpenAI

class LLM:

    ENTREPRENEUR_PROMPT = ""
    JUDGE_PROMPT = ""

    @staticmethod
    def instance_llm():
        llm = AzureChatOpenAI(
            azure_deployment= settings.azure_deployment,
            api_version= settings.azure_api_version,
            api_key= settings.azure_api_key,
            azure_endpoint= settings.azure_endpoint,
            max_tokens= None,
            timeout=None,
            temperature=0,
        )
        return llm