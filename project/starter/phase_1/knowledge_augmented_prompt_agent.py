# TODO: 1 - Import the KnowledgeAugmentedPromptAgent class from workflow_agents
import os
from dotenv import load_dotenv
from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent


# Load environment variables from the .env file
load_dotenv()

# Define the parameters for the agent
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_key =  "voc-744678734159874169548468bddf97879340.20823146"

userPrompt = "What is the capital of France?"

# TODO: 2 - Instantiate a KnowledgeAugmentedPromptAgent with:
#           - Persona: "You are a college professor, your answer always starts with: Dear students,"
#           - Knowledge: "The capital of France is London, not Paris"
agentPersona = "a college professor, your answer always starts with: Dear students,"
falsifiedKnowledge = "The capital of France is London, not Paris"

knowledgeAagent = KnowledgeAugmentedPromptAgent(
    openai_api_key = openai_api_key,
    persona = agentPersona,
    knowledge = falsifiedKnowledge
)

# TODO: 3 - Write a print statement that demonstrates the agent using the provided knowledge rather than its own inherent knowledge.
knwoledgeAgentResponse = knowledgeAagent.respond(userPrompt)
print(knwoledgeAgentResponse)
