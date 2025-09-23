# AI Home Search Assistant

This project is an AI-powered home search assistant built using CrewAI and Streamlit. It leverages a team of specialized AI agents and a custom tool to find real estate properties for sale based on a user's natural language request.

## Features

  - **Natural Language Processing**: The assistant can interpret complex requests, such as "a 3-bedroom house in Austin, TX, under $400k" or a home near a specific landmark.
  - **Specialized Agent**: A dedicated `Property Searcher` agent is designed to find properties for sale that precisely match a user's criteria, including geographic location.
  - **Custom Tool Integration**: The system uses a `PropertySearchTool` that interfaces with the RentCast API to search for real-time property listings.
  - **Geographic Search**: The tool can search for properties by full address, city, state, zip code, or geographical coordinates (latitude, longitude, and radius).
  - **Interactive UI**: The Streamlit web application provides a chat-based interface where users can interact with the AI assistant and view results.

## How It Works

The core of the application is a **CrewAI** framework that orchestrates the work of the AI agents.

1.  **User Input**: A user submits a query through the Streamlit chat interface.
2.  **Agent Tasking**: The `run_real_estate_crew` function receives the user's query and assigns it as a `search_task` to the `property_searcher_agent`.
3.  **Parameter Extraction**: The `property_searcher_agent` analyzes the request to extract key parameters like location (city, state, zip code, or coordinates), number of beds and baths, and a maximum price.
4.  **Tool Execution**: The agent uses the `Property Sale Listings Search Tool` to call the RentCast API with the extracted parameters. The tool is designed to prioritize location parameters in a specific order: address, then city/state/zip, and finally latitude/longitude.
5.  **Result Formatting**: The `PropertySearchTool` processes the API's JSON response and formats the top three most relevant properties into a human-readable string.
6.  **Final Response**: The agent provides a final answer, presenting the formatted list of properties back to the user in the Streamlit chat interface.

If no properties are found, the tool returns a clear message stating that no properties match the criteria.

## Project Structure

```
├── .env                 # Environment variables for API keys
├── app.py               # Streamlit web application
├── main.py              # CrewAI agent and task definitions
├── property_search_tool.py  # Custom tool for RentCast API
└── property_search_tool.ipynb # Jupyter notebook for development and testing
```

## Setup and Installation

### Prerequisites

  - Python 3.8+
  - A `.env` file with your API keys.

### Steps

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/hvn2025/AgenticAI_Home_Search.git
    cd AgenticAI_Home_Search
    ```

2.  **Create a virtual environment** (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables**:
    Create a `.env` file in the project's root directory and add your API keys. You will need a **RentCast API key** and a **Cohere API key**.

    ```env
    RENTCAST_API_KEY="your_rentcast_api_key"
    COHERE_API_KEY="your_cohere_api_key"
    ```

5.  **Run the Streamlit application**:

    ```bash
    streamlit run app.py
    ```

    This will launch the web application in your default browser. You can then interact with the AI home search assistant directly from the web interface.
