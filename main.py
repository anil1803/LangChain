from typing import List

from dotenv import load_dotenv

load_dotenv()

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch
from tavily import TavilyClient
from pydantic import BaseModel, Field

tavily = TavilyClient()

class Source(BaseModel):
    """Schema for the source used by agent"""
    url: str = Field(description="The URL of the source")
class AgentResponse(BaseModel):
    """Schema for the agent response"""
    answer: str = Field(description="The content of the response")
    sources: List[Source] = Field(default_factory=list, description="List of sources used to generate the answer")

@tool
def search(query: str) -> str:
    """
    Tool that search over internate
    Args:
        query (str): The search query
    Returns:
        str: The search results

    """
    print(f"Searching for: {query}")
    return tavily.search(query=query)

def main():
    print("Hello from langchain-course!")

    llm = ChatOpenAI(model="gpt-5", temperature=0)
    ##llm = ChatOllama(model="gemma3:12b", temperature=0)
    ##tool = [search]
    tool = [TavilySearch()]
    ##agent = create_agent(model=llm, tools=tool)
    agent = create_agent(model=llm, tools=tool, response_format=AgentResponse)
    response = agent.invoke({"messages": [HumanMessage(content="search for 3 job posting for an ai engineer using langchain in the bay area on linkedin and list their details")]}) 
    print(f"Agent response: {response}")

    
if __name__ == "__main__":
    main()
