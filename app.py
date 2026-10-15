
import os
import certifi
import requests
import streamlit as st

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

# ==========================================
# CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Agentic Chat Assistant",
    page_icon="🤖",
    layout="wide"
)

os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")

# ==========================================
# VALIDATE API KEYS
# ==========================================
missing_keys = [
    name for name, value in {
        "GROQ_API_KEY": GROQ_API_KEY,
        "TAVILY_API_KEY": TAVILY_API_KEY,
        "WEATHERSTACK_API_KEY": WEATHERSTACK_API_KEY,
    }.items()
    if not value
]

# ==========================================
# WEATHER TOOL
# ==========================================
@tool
def get_weather_data(city: str) -> str:
    """Fetch current weather information for a city."""
    if not WEATHERSTACK_API_KEY:
        return "WeatherStack API key is missing."

    url = "https://api.weatherstack.com/current"

    try:
        response = requests.get(
            url,
            params={
                "access_key": WEATHERSTACK_API_KEY,
                "query": city
            },
            timeout=15
        )
        response.raise_for_status()
        data = response.json()

        if "current" not in data:
            return (
                "Could not fetch weather data: "
                + str(data.get("error", {}).get("info", "Unknown API error"))
            )

        current = data["current"]
        location = data.get("location", {})

        return (
            f"City: {location.get('name', city)}\n"
            f"Country: {location.get('country', 'Unknown')}\n"
            f"Temperature: {current['temperature']}°C\n"
            f"Weather: {current['weather_descriptions'][0]}\n"
            f"Humidity: {current['humidity']}%\n"
            f"Wind Speed: {current['wind_speed']} km/h"
        )

    except requests.RequestException as exc:
        return f"Weather request failed: {exc}"


# ==========================================
# BUILD AGENT
# ==========================================
@st.cache_resource
def create_agent():
    if missing_keys:
        raise ValueError(
            "Missing API keys in .env: " + ", ".join(missing_keys)
        )

    search_tool = TavilySearchResults(max_results=3)

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
        api_key=GROQ_API_KEY
    )

    tools = [search_tool, get_weather_data]

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

    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=6
    )


# ==========================================
# STREAMLIT STYLING
# ==========================================
st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 2.4rem;
    font-weight: 700;
}
.subtitle {
    text-align: center;
    color: #808495;
    margin-bottom: 25px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.title("🤖 Agent Controls")
    st.markdown("---")
    st.subheader("Available Tools")
    st.markdown("""
    🔍 **Tavily Search**  
    Search the web for current information.

    🌦️ **WeatherStack**  
    Retrieve current weather information.

    🧠 **Groq LLM**  
    Reason about questions and choose tools.
    """)
    st.markdown("---")

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption("Built with LangChain + Streamlit")

# ==========================================
# HEADER
# ==========================================
st.markdown(
    '<div class="main-title">🤖 Agentic Chat Assistant</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">'
    'Search the web, check weather, and ask questions.'
    '</div>',
    unsafe_allow_html=True
)

# ==========================================
# CHAT HISTORY
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# EXAMPLE PROMPTS
# ==========================================
if not st.session_state.messages:
    st.subheader("Try asking")

    col1, col2, col3 = st.columns(3)

    if col1.button("🇮🇳 Capital of India", use_container_width=True):
        st.session_state.pending_prompt = (
            "Find the capital of India."
        )
        st.rerun()

    if col2.button("🌦️ Hyderabad Weather", use_container_width=True):
        st.session_state.pending_prompt = (
            "Find the current weather in Hyderabad, India."
        )
        st.rerun()

    if col3.button("🔍 Search + Weather", use_container_width=True):
        st.session_state.pending_prompt = (
            "Find the capital of India and then find its current weather."
        )
        st.rerun()

# ==========================================
# USER INPUT
# ==========================================
user_input = st.chat_input("Ask me anything...")

if "pending_prompt" in st.session_state:
    user_input = st.session_state.pop("pending_prompt")

# ==========================================
# PROCESS QUESTION
# ==========================================
if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Agent is thinking and using tools..."):
                agent_executor = create_agent()
                result = agent_executor.invoke({
                    "input": user_input
                })
                answer = result.get(
                    "output",
                    "The agent did not return an answer."
                )

            st.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as exc:
            st.error("The agent encountered an error.")
            st.code(str(exc))
