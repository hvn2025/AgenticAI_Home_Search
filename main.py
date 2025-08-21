from property_search_tool import PropertySearchTool
property_search_tool = PropertySearchTool()
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

load_dotenv()
import os
from langchain_cohere import ChatCohere
# from langchain_community.chat_models import ChatCohere
# Initialize language model
os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")
llm = ChatCohere(model="command-a-03-2025")

property_searcher_agent = Agent(
    role='Expert Property Sale Listings Searcher',
    goal='Find properties for sale that precisely match the user\'s criteria, including geographic location.',
    backstory='You are a highly skilled AI specializing in real estate sale listings. Your main task is to accurately interpret user requests, extract precise geographic coordinates (latitude, longitude, and radius), and find relevant properties for sale by efficiently utilizing search tools. You are meticulous and focus on delivering accurate and concise results.',
    verbose=True, # Set to True to see the agent's thought process
    allow_delegation=False, # For this simple agent, no delegation needed yet
    tools=[property_search_tool], # Register the custom tool with the agent
    llm=llm, # Explicitly pass the Gemini LLM instance here
    memory=True
)

search_task = Task(
    description=(
        "Search for real estate properties FOR SALE based on the following user request:\n"
        "User Request: '{user_property_query}'\n\n"
        "IMPORTANT: You MUST extract the precise latitude, longitude, and a search radius (in miles) from the user's request. "
        "If the user provides an address or city, you must infer or ask for these coordinates and radius. "
        "Also extract optional details like min_price, max_price, beds, baths, and property_type. "
        "Use the 'Property Sale Listings Search Tool' to find the listings. "
        "Present the top 3 relevant properties found in a clear, concise list, including their address, "
        "price, number of bedrooms/bathrooms, property type, and current status (e.g., 'Active')."
    ),
    expected_output=(
        "A clear list of the top 3 properties for sale found, including their address, "
        "price, number of bedrooms/bathrooms, property type, and status. "
        "If no properties are found, state that clearly."
    ),
    agent=property_searcher_agent,
    verbose=True
)



#result = real_estate_crew.kickoff(inputs={'user_property_query': user_query})

def run_real_estate_crew(user_property_query: str) -> str:
    """
    Assembles and runs the real estate search crew with a given user query.
    Returns the final output from the agent.
    """
    real_estate_crew = Crew(
    agents=[property_searcher_agent],
    tasks=[search_task],
    process=Process.sequential, # Tasks are executed one after another
    verbose=True # Higher verbosity for more detailed output from the crew
    )
    # Note: CrewAI re-initializes agents and tasks within kickoff if not done globally
    # For a Streamlit app, it's often cleaner to define agents/tasks outside this function
    # if they don't change per run, but this structure works.
    print(user_property_query)
    result = real_estate_crew.kickoff(inputs={'user_property_query': user_property_query})

    return result

# --- Original direct execution block (only runs if main.py is executed directly) ---
if __name__ == "__main__":
    user_query = input(
        "What kind of home for sale are you looking for, or what school information do you need? "
        "Examples:\n"
        "- 'a 3-bedroom house in Austin, TX, under $400k'\n"
        "- 'a condo for sale in zip code 78704 with 2 baths'\n"
        "- 'Show me public elementary school ratings in Austin, TX'\n"
        "- 'What are the best high schools near latitude 30.26, longitude -97.74?'\n"
    )
    print("### Initiating Real Estate Assistant ###")
    final_output = run_real_estate_crew(user_query)
    print("\n### Real Estate Assistant Completed ###")
    print(final_output)