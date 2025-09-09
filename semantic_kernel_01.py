import os
import asyncio
from typing import Annotated
import random
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.functions import kernel_function, KernelArguments
from dotenv import load_dotenv

# Load environment variables from .env file for secure credential management
load_dotenv()

# Retrieve Azure OpenAI credentials and model info from environment variables
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")
model = os.getenv("AZURE_OPENAI_MODEL")

# -------------------------------
# Support Plugins
# -------------------------------

class EmailPlugin:
    """Plugin for support ticket creation via email on behalf of the user"""

    @kernel_function(description="Creates a support ticket via email to the support team on user's behalf")
    def create_support_ticket(self,
                   issue: Annotated[str, "Description of the issue"],
                   priority: Annotated[str, "Priority level (low/medium/high)"] = "medium"):
        # Simulate sending an email for support
        print("\n--- Support Ticket Created ---")
        print(f"To: customercare@msft.com")
        print(f"Priority: {priority.upper()}")
        print(f"Issue:\n{issue}")
        print("------------------------------\n")
        return f"{priority.capitalize()} priority ticket created and emailed to customercare@msft.com - reference #ST{random.randint(1000,9999)}"

class PhoneCallPlugin:
    """Plugin for customer support calls on behalf of the user"""

    @kernel_function(description="Simulates a customer support call to the support team on user's behalf")
    def initiate_support_call(self,
                    issue: Annotated[str, "Brief issue description"]):
        # Simulate making a support call
        verification_code = f"{random.randint(1000,9999)}"
        print("\n--- Support Call Initiated ---")
        print(f"Calling: Support Team")
        print(f"Issue: {issue}")
        print(f"Verification code sent: {verification_code}")
        print("------------------------------\n")
        return {
            "status": "call_connected",
            "verification_code": verification_code,
            "next_step": "Support team will follow up with the user"
        }

# -------------------------------
# Main Async Function
# -------------------------------
async def main():
    # Clear the terminal for a clean demo experience
    os.system('cls' if os.name == 'nt' else 'clear')

    # Create a chat completion agent with Azure OpenAI and custom plugins
    agent = ChatCompletionAgent(
        service=AzureChatCompletion(
            base_url=f"{azure_endpoint}/openai/deployments/{model}/chat/completions?api-version={api_version}",
            api_key=subscription_key,
            deployment_name=model,
            api_version=api_version,
        ),
        name="SupportAgent",
        instructions="""
You are a customer support AI assistant.
- If the user wants to send an email, use create_support_ticket function and always send to customercare@msft.com on behalf of the user.
- If the user wants a call, use initiate_support_call function and always call the support team on behalf of the user.
- Do not ask for user's contact details.
- Confirm the action taken to the user.
- If user says 'bye' or 'exit', thank them and end the conversation.
""",
        plugins=[EmailPlugin(), PhoneCallPlugin()],
        arguments=KernelArguments(settings=OpenAIChatPromptExecutionSettings())
    )

    print("🛎️  Welcome to msft Support Assistant!")
    print("Type 'exit' or 'bye' to end the conversation\n")

    # Main interaction loop for the support assistant
    while True:
        user_input = input("\nHow can I assist you today?\n> ")

        if user_input.strip().lower() in ("exit", "bye"):
            print("\n👋 Thank you for using microsoft Support!")
            break

        # Get the agent's response to the user's input
        response = await agent.get_response(messages=user_input)
        print("\n🛠️  Support Response:")
        print(response.content)

# -------------------------------
# Run the script
# -------------------------------
if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
