
# TODO: 1 - Import the KnowledgeAugmentedPromptAgent and RoutingAgent
import os
from dotenv import load_dotenv
from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent, RoutingAgent

# Load environment variables from .env file
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_key =  "voc-744678734159874169548468bddf97879340.20823146"

persona = "You are a college professor"

knowledge = "You know everything about Texas"
# TODO: 2 - Define the Texas Knowledge Augmented Prompt Agent
texasExpertAgent = KnowledgeAugmentedPromptAgent(
    openai_api_key = openai_api_key,
    persona = persona,
    knowledge = "You know everything about the history and geography of Texas and the Texas country in general."
)

knowledge = "You know everything about Europe"
# TODO: 3 - Define the Europe Knowledge Augmented Prompt Agent
europeExpertAgent = KnowledgeAugmentedPromptAgent(
    openai_api_key = openai_api_key,
    persona = persona,
    knowledge = "You know everything about the history and geography of Europe and the European continent in general."
)

persona = "You are a college math professor"
knowledge = "You know everything about math, you take prompts with numbers, extract math formulas, and show the answer without explanation"
# TODO: 4 - Define the Math Knowledge Augmented Prompt Agent
mathExpertAgent = KnowledgeAugmentedPromptAgent(
    openai_api_key = openai_api_key,
    persona = persona,
    knowledge = "You know everything about the mathematics and any of its sub-domains and at any sophistication levels."
)

routing_agent = RoutingAgent(openai_api_key, {})

agents = [
    {
        "name": "texas agent",
        "description": "Answer a question about Texas",
        "func": lambda x: texasExpertAgent.respond(x) # TODO: 5 - Call the Texas Agent to respond to prompts
    },
    {
        "name": "europe agent",
        "description": "Answer a question about Europe",
        "func": lambda x: europeExpertAgent.respond(x) # TODO: 6 - Define a function to call the Europe Agent
    },
    {
        "name": "math agent",
        "description": "When a prompt contains numbers, respond with a math formula",
        "func": lambda x: mathExpertAgent.respond(x)  # TODO: 7 - Define a function to call the Math Agent
    }
]

routing_agent.agents = agents

# TODO: 8 - Print the RoutingAgent responses to the following prompts:
#           - "Tell me about the history of Rome, Texas"
#           - "Tell me about the history of Rome, Italy"
#           - "One story takes 2 days, and there are 20 stories"

testPromptLs = [
    "Tell me about the history of Rome, Texas",
    "Tell me about the history of Rome, Italy",
    "One story takes 2 days, and there are 20 stories"
]

for testPrompt in testPromptLs:
    print(f"Test Prompt: {testPrompt}")
    response = routing_agent.route(testPrompt)
    print(f"\nFinal Response:\n{response}")
