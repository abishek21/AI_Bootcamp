
import os
from openai import AzureOpenAI
import autogen
from autogen import AssistantAgent, UserProxyAgent
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

subscription_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")
model = os.getenv("AZURE_OPENAI_MODEL")

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=azure_endpoint,
    api_key=subscription_key,
)

llm_config = {
    "model": model,  # or your deployed Azure OpenAI model name
    "api_type": "azure",
    "api_key": subscription_key,
    "azure_endpoint": azure_endpoint,
    "api_version": api_version,
}

assistant = AssistantAgent("assistant", llm_config=llm_config)

user_proxy = UserProxyAgent(
    "user_proxy", code_execution_config={"executor": autogen.coding.LocalCommandLineCodeExecutor(work_dir="coding")}, 
    llm_config=llm_config
)

# Start the chat
user_proxy.initiate_chat(
    assistant,
    message="Plot a chart of MSFT stock price change YTD.",
)