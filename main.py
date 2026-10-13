import os
import certifi
import requests

from dotenv import load_dotenv

from langchain_openai import ChatGroq
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults


from langchain.agents import (create_react_agent, AgentExecutor)

from langchain_core.prompts import PromptTemplate

# ==========================================
# LOAD ENV VARIABLES
# ==========================================
os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")

# ==========================================
# SEARCH TOOL
# ==========================================

search_tool = TavilySearchResults(max_results=2)

# ==========================================
# WEATHER TOOL
# ==========================================

@tool
def get_weather_data(city: str) -> str:
    """
    Fetch current weather information for a city.
    """

    url = (
        f"https://api.weatherstack.com/current?"
        f"access_key={WEATHERSTACK_API_KEY}&query={city}"
    )

    response = requests.get(url)

    data = response.json()

    if "current" not in data:
        return f"Could not fetch weather data for {city}"

    return (
        f"City: {city}\n"
        f"Temperature: {data['current']['temperature']}°C\n"
        f"Weather: {data['current']['weather_descriptions'][0]}\n"
        f"Humidity: {data['current']['humidity']}%"
    )

# ==========================================
# LLM
# ==========================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=GROQ_API_KEY
)

# ==========================================
# PROMPT
# ==========================================

prompt = PromptTemplate.from_template("""
You are a helpful AI assistant with access to tools.

Answer the user's question accurately. Use tools when needed.
For current information, use web search. For weather questions,
use the weather tool.

You have access to these tools:

{tools}

Use this format:

Question: the user's question
Thought: think about what to do
Action: one of [{tool_names}]
Action Input: the input for the tool
Observation: the tool's result
... (repeat Thought/Action/Action Input/Observation as needed)
Thought: I now know the final answer
Final Answer: the final response to the user

Question: {input}
Thought:{agent_scratchpad}
""")

# ==========================================
# TOOLS
# ==========================================

tools = [
    search_tool,
    get_weather_data
]

# ==========================================
# CREATE AGENT
# ==========================================

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# ==========================================
# EXECUTOR
# ==========================================

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=(
        "Invalid format. Follow the required format: "
        "Thought, Action, Action Input, or Final Answer."
    ),
    max_iterations=10,
    max_execution_time=90,
    early_stopping_method="force"
)

# ==========================================
# RUN
# ==========================================

response = agent_executor.invoke({
    "input": (
        "Find the capital of India"
        "and then find its current weather."
    )
})

print("\n========================")
print("FINAL OUTPUT")
print("========================\n")

print(response["output"])