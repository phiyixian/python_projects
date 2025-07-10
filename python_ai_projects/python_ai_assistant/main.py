#langchain allow us to build AI application
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from sympy import symbols, integrate, pi, sympify

#allow us to built AI agents
#AI agents can access to tools if compared to chatbots
from langgraph.prebuilt import create_react_agent

#load info from .env
from dotenv import load_dotenv

#for weather tool
import os
import requests

#use streamlit to display chat
import streamlit as st
st.title("My first AI Assistant")

load_dotenv()


@tool 
def calculator(expression: str) -> str:
    """Evaluate basic math expression"""
    print("Calculator tool called")
    try:
        result = eval(expression)
        return f"The result is {result}"
    except:
        return "Invalid math expression"

@tool
def dictionary(word: str) -> str:
    """Provide a simple definition of common words"""
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)

    if response.status_code != 200:
        return "Definition not found."
    
    data = response.json()
    try:
        definition = data[0]['meanings'][0]['definitions'][0]['definition']
        return f"The meaning of {word} is: {definition}"
    except(KeyError, IndexError):
        return "Definition not found"
    
@tool
def get_weather(city: str) -> str:
    """Provides real-time weather for a given city"""
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "Weather API key not found."
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return "Weather data not found"
    
    data = response.json()
    try:
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        return f"The weather in {city} is {desc} with {temp}°C."
    except (KeyError, IndexError):
        return "Error processing weather data"

def main():
    #higher temperature means higher randomness
    model = ChatOpenAI(temperature=0)

    #tools the agent can use
    tools = [calculator, dictionary, get_weather]
    agent_executor = create_react_agent(model, tools)

    print("Welcome! I'm your AI assistant. Type 'quit' to exit.")
    print("You can ask me anything or just chat with me.")

    ### Run in Terminal ###
    # while True:
    #     #strip removes any white spaces and go to next line
    #     user_input = input("\nYou: ").strip()

    #     if user_input == "quit":
    #         break

    #     print("\nAssistant: ", end="")
    #     for chunk in agent_executor.stream(
    #         {"messages": [HumanMessage(content=user_input)]}
    #     ):
    #         #chunks are part of response from agent, below checks for this
    #         if "agent" in chunk and "messages" in chunk["agent"]:
    #             for message in chunk["agent"]["messages"]:
    #                 print(message.content, end="")

    #     print()

    ### Run in StreamLit ###
    user_input = st.text_input("Ask me anything")

    if st.button("Submit"):
        if user_input:
            st.write("Assistant is thinking...")
            response = ""

            for chunk in agent_aexecutor.stream({"messages": [HumanMessage(content=user_input)]}):
                if "agent" in chunk and "messages" in chunk["agent"]:
                    for message in chunk["agent"]["messages"]:
                        response += message.content

            st.write(response)

if __name__ == "__main__":
    main()
