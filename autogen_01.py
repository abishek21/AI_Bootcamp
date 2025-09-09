import os
from openai import AzureOpenAI
import autogen
from autogen import AssistantAgent, UserProxyAgent
from dotenv import load_dotenv

# Load environment variables from .env file for secure credential management
load_dotenv()

# Retrieve Azure OpenAI credentials and model info from environment variables
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")
model = os.getenv("AZURE_OPENAI_MODEL")

# Initialize the Azure OpenAI client for direct API calls (not always required for autogen, but useful for custom calls)
client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=azure_endpoint,
    api_key=subscription_key,
)

# Configuration dictionary for the LLM, used by autogen agents
llm_config = {
    "model": model,  # Name of your deployed Azure OpenAI model
    "api_type": "azure",
    "api_key": subscription_key,
    "azure_endpoint": azure_endpoint,
    "api_version": api_version,
}

# Create an assistant agent that will handle LLM-powered tasks
assistant = AssistantAgent("assistant", llm_config=llm_config)

# Create a user proxy agent that can execute code in a local directory
user_proxy = UserProxyAgent(
    "user_proxy",
    code_execution_config={
        # Use the local command line executor, with 'coding' as the working directory for generated code
        "executor": autogen.coding.LocalCommandLineCodeExecutor(work_dir="coding")
    },
    llm_config=llm_config
)
## Use Docker-based code execution for better isolation (uncomment if Docker is set up)
# with autogen.coding.DockerCommandLineCodeExecutor(work_dir="coding") as code_executor:
#     assistant = AssistantAgent("assistant", llm_config=llm_config)
#     user_proxy = UserProxyAgent(
#         "user_proxy", code_execution_config={"executor": code_executor}
#     )

#     # Start the chat
#     user_proxy.initiate_chat(
#         assistant,
#         message="Plot a chart of MSFT stock price change YTD.",
#     )

# Start the chat between the user proxy and the assistant
user_proxy.initiate_chat(
    assistant,
    message="Plot a chart of MSFT stock price change YTD and save it as a PNG file.",
)