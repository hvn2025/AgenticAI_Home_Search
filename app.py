# ai_home_assistant_prototype/app.py

import streamlit as st
import os
from dotenv import load_dotenv

# Import the function that runs your CrewAI agent
from main import run_real_estate_crew

# Load environment variables (ensure .env is in the same directory as app.py)
load_dotenv()

# --- Streamlit App UI ---
st.set_page_config(page_title="AI Home Search Assistant", layout="centered")

st.title("🏡 AI Home Search Assistant")
st.markdown("Your personalized AI co-pilot for finding homes for sale. I remember our conversation!")

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for the user's query
if prompt := st.chat_input("What kind of home are you looking for?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare the query for the agent. CrewAI's memory handles the history internally
    # when `memory=True` is set on the agent. We just pass the latest user prompt.
    user_property_query = prompt

    with st.spinner("Thinking... AI agents are working on your request."):
        try:
            # Call the function that runs your CrewAI agent with the latest user query
            # The agent's internal memory will handle the context from previous turns.
            agent_response = run_real_estate_crew(user_property_query)

            # Add agent response to chat history
            st.session_state.messages.append({"role": "assistant", "content": agent_response})
            # Display agent response in chat message container
            with st.chat_message("assistant"):
                st.markdown(agent_response)

        except Exception as e:
            error_message = f"An error occurred during processing: {e}"
            st.session_state.messages.append({"role": "assistant", "content": f"❌ {error_message}"})
            with st.chat_message("assistant"):
                st.error(error_message)
            st.write("Please check your API keys and the query format. Ensure all services are running.")

st.markdown("---")

