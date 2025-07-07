from dotenv import load_dotenv
from agents import Agent, Runner  , OpenAIChatCompletionsModel, set_tracing_disabled , function_tool
from openai import AsyncOpenAI
from agents.run import  RunConfig
import os
load_dotenv()

set_tracing_disabled(True)
client = AsyncOpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

config = RunConfig(
    model=model,
    model_provider=client,

)

@function_tool
def add(a:int,b:int) ->int:
    print(f"Adding {a} and {b}")
    return a + b

@function_tool
def sub(a:int,b:int) ->int:
    print(f"subtraction: {a} and {b}")
    return a - b

@function_tool
def Multiple(a:int,b:int) ->int:
    print(f"Multiplication:{a} and {b}")
    return a * b

@function_tool
def divide(a:int,b:int)->int:
    print(f"Division:{a} and {b}")
    return a / b

agent= Agent(
    name= "calculater_Agent",
    model= model ,
    instructions="you are a helpful assistant.Answer questions to the best of your ability. You have the following tools: add ,sub ,Multiple, divide",
    tools=[add ,sub , Multiple , divide]
    
)
while True:
    user_input = input("Enter your input (or type 'exit' to quit): ")
    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("Goodbye!")
        break  # end the loop

    result = Runner.run_sync(
    agent, user_input , run_config=config

    )
    print(result.final_output)