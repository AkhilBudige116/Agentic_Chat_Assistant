# 🤖 Agentic Chat Assistant

An AI-powered conversational assistant built using **Python, Streamlit, LangChain, and Groq**. The application can answer user questions, search the web for real-time information, and retrieve current weather details using external APIs.

## ✨ Features

- **AI-Powered Chat:** Provides conversational responses using a Groq-hosted Large Language Model (LLM).
- **Live Web Search:** Uses the Tavily Search API to retrieve relevant web information.
- **Weather Information:** Retrieves current weather details using the WeatherStack API.
- **Agent-Based Workflow:** Allows the AI agent to select and use tools based on the user's query.
- **Interactive UI:** Provides a user-friendly chat interface using Streamlit.
- **Chat History:** Maintains conversation history during the application session.
- **Environment Configuration:** Stores API keys securely using environment variables.

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- Groq API
- Tavily Search API
- WeatherStack API
- Requests
- python-dotenv
- Certifi

## 📁 Project Structure

```text
Agentic_Chat_Assistant/
├── app.py
├── main.py
├── requirements.txt
├── pyproject.toml
├── .python-version
├── .gitignore
└── README.md
```

## ⚙️ Prerequisites

Before running the project, make sure you have:

- Python installed
- Git installed
- A Groq API key
- A Tavily API key
- A WeatherStack API key

Get your API keys from:

- Groq: https://console.groq.com/
- Tavily: https://app.tavily.com/
- WeatherStack: https://weatherstack.com/

## 🚀 Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/AkhilBudige116/Agentic_Chat_Assistant.git
cd Agentic_Chat_Assistant
```

### Step 2: Create a Virtual Environment

For Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If a required package is missing, install the relevant dependency and update your requirements file accordingly.

### Step 4: Configure Environment Variables

Create a `.env` file in the project root directory and add your API keys:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
WEATHERSTACK_API_KEY=your_weatherstack_api_key
```

Replace the placeholder values with your actual API keys.

**Security note:** Never upload your `.env` file or expose your API keys on GitHub. Ensure `.env` is included in `.gitignore`.

### Step 5: Run the Application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

http://localhost:8501

## 💬 Example Queries

Try asking the assistant:

- Search the web for the latest developments in Agentic AI.
- What is the current weather in Hyderabad, India?
- Explain the difference between AI agents and traditional chatbots.
- Search for recent advancements in Generative AI.
- Find information about Large Language Models and RAG.

The availability of live search and weather results depends on the configured APIs and their usage limits.

## 🔄 How It Works

1. The user enters a question in the Streamlit chat interface.
2. The LLM interprets the user's request.
3. The agent determines whether a tool is needed.
4. The Tavily tool retrieves web information, or the weather tool calls the WeatherStack API.
5. The tool returns its result to the agent.
6. The LLM generates a final response for the user.

## 🔐 Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Connects to the Groq language model |
| `TAVILY_API_KEY` | Enables web search |
| `WEATHERSTACK_API_KEY` | Enables weather lookup |

## 🐛 Troubleshooting

**Model not found (404)**

Check whether the configured model ID is available to your Groq account and update the model configuration in your application.

**Module not found**

Activate your virtual environment and install the missing dependencies.

**Web search not working**

Verify your Tavily API key and check your API usage limits.

**Weather tool not working**

Verify your WeatherStack API key and the availability of the requested weather service.

**Streamlit application not starting**

Try running:

```bash
python -m streamlit run app.py
```

## 🚀 Future Enhancements

- Integrate additional custom tools.
- Add source citations to web-search responses.
- Improve error handling and retry mechanisms.
- Add persistent conversation memory.
- Implement logging, testing, and performance monitoring.
- Explore advanced multi-agent workflows using LangGraph.

## 👨‍💻 Author

**Akhil Budige**

GitHub: https://github.com/AkhilBudige116

Project Repository: https://github.com/AkhilBudige116/Agentic_Chat_Assistant

## 📄 License

A license has not yet been specified for this project. Add a `LICENSE` file if you intend to define how others can use, modify, or distribute this software.
