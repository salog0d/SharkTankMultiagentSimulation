from typing import Optional
from langchain_openai import AzureChatOpenAI
from src.core.settings import settings


class LLM:

    @staticmethod
    def instance() -> AzureChatOpenAI:
        """
        Returns an async AzureChatOpenAI instance.
        Compatible with LangChain 1.x and LangGraph 1.x
        """
        return AzureChatOpenAI(
            azure_deployment=settings.azure_deployment,
            api_version=settings.azure_api_version,
            api_key=settings.azure_api_key,
            azure_endpoint=settings.azure_endpoint,
            temperature=0,
            max_tokens=2048,
        )

    
    @staticmethod
    async def generate(prompt: str) -> str:

        llm = LLM.instance()
        resp = await llm.ainvoke(prompt)

        if hasattr(resp, "content") and resp.content:
            return resp.content

        return str(resp)
    


