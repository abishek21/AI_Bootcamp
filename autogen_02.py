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

# Configuration dictionary for the LLM, used by autogen agents
llm_config = {
    "model": model,  # Name of your deployed Azure OpenAI model
    "api_type": "azure",
    "api_key": subscription_key,
    "azure_endpoint": azure_endpoint,
    "api_version": api_version,
}

# Define tasks for the financial and writing assistants
financial_tasks = [
    """What are the current stock prices of MSFT and how is the performance over the past month in terms of percentage change?"""
]

writing_tasks = [
    """Develop an engaging blog post using any information provided. After writing, output only the Python code (in a Python code block) to save the blog post as blog_post.txt""",
    """Write a funny blog about Microsoft stock. After writing, output only the Python code (in a Python code block) to save the blog post as funny_msft_blog.txt"""
]

# Create specialized assistant agents for different tasks
financial_assistant = autogen.AssistantAgent(
    name="Financial_assistant",
    llm_config=llm_config,
)
research_assistant = autogen.AssistantAgent(
    name="Researcher",
    llm_config=llm_config,
)
writer = autogen.AssistantAgent(
    name="writer",
    llm_config=llm_config,
    system_message="""
        You are a professional writer, known for
        your insightful and engaging articles.
        You transform complex concepts into compelling narratives.
        After writing the blog post save the blog in a .txt file
        """,
)

# Create a user proxy agent that can execute code and interact with assistants
user = autogen.UserProxyAgent(
    name="User",
    human_input_mode="ALWAYS",  # Allows for human input during the workflow
    # is_termination_msg can be customized to control when the conversation ends
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": "tasks",
        "use_docker": False,
    },  # Set use_docker=True if you want to run code in a Docker container for safety
)

# Initiate parallel chats with the assistants for each task
chat_results = user.initiate_chats(
    [
        {
            "recipient": financial_assistant,
            "message": financial_tasks[0],
            "clear_history": True,
            "silent": False,
            "summary_method": "last_msg",
        },
        {
            "recipient": writer,
            "message": writing_tasks[0],
            "carryover": "please ensure the blog is in a .txt file",
        },
        {
            "recipient": writer,
            "message": writing_tasks[1],
            "carryover": "please ensure the blog is in a .txt file",
        },
    ]
)