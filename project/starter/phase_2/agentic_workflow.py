# agentic_workflow.py

# TODO: 1 - Import the following agents: ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent from the workflow_agents.base_agents module

import os
from dotenv import load_dotenv
from workflow_agents.base_agents import ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent


# TODO: 2 - Load the OpenAI key into a variable called openai_api_key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# load the product spec
# TODO: 3 - Load the product spec document Product-Spec-Email-Router.txt into a variable called product_spec
with open('Product-Spec-Email-Router.txt', 'r') as f:
    prodSpecContent = f.read()

# Instantiate all the agents

# Action Planning Agent
knowledge_action_planning = (
    """
    Each Development Plan has strictly predefined hierarchy.
    Each Development Plan consists of stories features.
    Features are decomposed into user stories.
    User stories are decomposed into engineering tasks.
    
    Stories are defined from a product spec by identifying a persona, an action, and a desired outcome for each story. Each story represents a specific functionality of the product described in the specification. 
    Features are defined by grouping related user stories. 
    Tasks are defined for each story and represent the engineering work required to develop the product.  
    The final development plan must contain all features, their corresponding user stories, and the engineering tasks for each story.
    
    The Development Plan fis created based on the product specification. 
    
    The plan must follow the strictly below STEPS:
    1. **DEFINE User Stories** based on product specification. 
    2. **FORMULATE Features**. 
    3. **CREATE Engineering Tasks**.
    The plan must contain ALL STEPS ABOVE.
     
    """
)
# TODO: 4 - Instantiate an action_planning_agent using the 'knowledge_action_planning'
action_planning_agent = ActionPlanningAgent(
    openai_api_key = openai_api_key,
    knowledge = knowledge_action_planning
)

# Product Manager - Knowledge Augmented Prompt Agent
persona_product_manager = """
                            You are a Product Manager, you are responsible for defining the user stories for a product.
                            You reformulate and augment the attached Development Plan with the user stories.
                            Users stories are defined following the instructions from user query and based on the attached product specification.
                            
                            Output format:
                            Return ONLY PLAN AUGMENTED with user stories. Plan must preserve REQUIRED HIERARCHY.
                          """

knowledge_product_manager = (
    f"""
    Each Development Plan has strictly predefined hierarchy.
    Each Development Plan consists of stories features.
    Features are decomposed into user stories.
    User stories are decomposed into engineering tasks.
    
    Stories are defined by writing sentences with a persona, an action, and a desired outcome. 
    The sentences always start with: 'As a...' 
    Write several stories for required to deliver the product specified by the specification outlined below, 
    where the personas are the different users of the specified product. 
    
    Utilize ONLY below product specification for defining user stories:
    
    ****Product specification****
    {prodSpecContent}
    *****************************
    
    """
    # TODO: 5 - Complete this knowledge string by appending the product_spec loaded in TODO 3
)

#knowledge_product_manager += prodSpecContent

# TODO: 6 - Instantiate a product_manager_knowledge_agent using 'persona_product_manager' and the completed 'knowledge_product_manager'
product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key = openai_api_key,
    persona = persona_product_manager,
    knowledge = knowledge_product_manager
)


# Product Manager - Evaluation Agent
# TODO: 7 - Define the persona and evaluation criteria for a Product Manager evaluation agent and instantiate it as product_manager_evaluation_agent.
# TODO: This agent will evaluate the product_manager_knowledge_agent.
# The evaluation_criteria should specify the expected structure for user stories (e.g., "As a [type of user], I want [an action or feature] so that [benefit/value].").

pmEvalPersona = """
        You are an helpful Expert evaluation agent that checks the answers and outputs of other worker agents 
        - especially for Product Manager agents.
      """


pmEvalCriteria = """
                    The answer should be stories that follow the following structure: 
                    As a [type of user], I want [an action or feature] so that [benefit/value]."
                 """

product_manager_evaluation_agent = EvaluationAgent(
    openai_api_key = openai_api_key,
    persona = pmEvalPersona,
    evaluation_criteria = pmEvalCriteria,
    worker_agent = product_manager_knowledge_agent,
    max_interactions = 5
)

# Program Manager - Knowledge Augmented Prompt Agent
persona_program_manager = """
                             You are a Program Manager, you are responsible for defining the features for a product.
                             You reformulate and augment the attached Development Plan with the features.
                             Features are defined by grouping related user stories into cohesive groups.
                             Features are defined following the instructions from user query and based on the attached product specification.
                             
                             Output format:
                             Return ONLY AUGMENTED PLAN with features. Plan must preserve REQUIRED HIERARCHY.
                          """

knowledge_program_manager = """
                              Features of a product are defined by organizing similar user stories into cohesive groups.
                              Each Development Plan has strictly predefined hierarchy.
                              Each Development Plan consists of stories features.
                              Features are decomposed into user stories.
                              User stories are decomposed into engineering tasks.
                              """
# Instantiate a program_manager_knowledge_agent using 'persona_program_manager' and 'knowledge_program_manager'

# (This is a necessary step before TODO 8. Students should add the instantiation code here.)
program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona = persona_program_manager,
    knowledge = knowledge_program_manager
)

# Program Manager - Evaluation Agent
persona_program_manager_eval = "You are an evaluation agent that checks the answers of other worker agents."

# TODO: 8 - Instantiate a program_manager_evaluation_agent using 'persona_program_manager_eval' and the evaluation criteria below.
#                      "The answer should be product features that follow the following structure: " \
#                      "Feature Name: A clear, concise title that identifies the capability\n" \
#                      "Description: A brief explanation of what the feature does and its purpose\n" \
#                      "Key Functionality: The specific capabilities or actions the feature provides\n" \
#                      "User Benefit: How this feature creates value for the user"
# For the 'agent_to_evaluate' parameter, refer to the provided solution code's pattern.

programManagerEvalCriteria = """
    The answer should be product features that follow the following structure: 
    Feature Name: A clear, concise title that identifies the capability\n
    Description: A brief explanation of what the feature does and its purpose\n
    Key Functionality: The specific capabilities or actions the feature provides\n"
    User Benefit: How this feature creates value for the user.
    """

program_manager_evaluation_agent = EvaluationAgent(
    openai_api_key = openai_api_key,
    persona = persona_program_manager_eval,
    evaluation_criteria = programManagerEvalCriteria,
    worker_agent = program_manager_knowledge_agent,
    max_interactions = 5
)


# Development Engineer - Knowledge Augmented Prompt Agent
persona_dev_engineer = """
                        You are a Development Engineer, you are responsible for defining the development tasks for a product. 
                        You reformulate and augment the attached Development Plan with the development tasks.
                        Tasks are defined following the instructions from user query and based on the attached product specification.
                        
                        Output format:
                        Return ONLY PLAN AUGMENTED with development tasks. Plan must preserve REQUIRED HIERARCHY.
                        """

knowledge_dev_engineer = """Development tasks are defined by identifying what needs to be built to implement each user story.
                            Each Development Plan has strictly predefined hierarchy.
                            Each Development Plan consists of stories features.
                            Features are decomposed into user stories.
                            User stories are decomposed into engineering tasks.
                         """

# Instantiate a development_engineer_knowledge_agent using 'persona_dev_engineer' and 'knowledge_dev_engineer'
# (This is a necessary step before TODO 9. Students should add the instantiation code here.)

development_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key = openai_api_key,
    persona = persona_dev_engineer,
    knowledge = knowledge_dev_engineer
)

# Development Engineer - Evaluation Agent
persona_dev_engineer_eval = "You are an evaluation agent that checks the answers of other worker agents."
# TODO: 9 - Instantiate a development_engineer_evaluation_agent using 'persona_dev_engineer_eval' and the evaluation criteria below.
#                      "The answer should be tasks following this exact structure: " \
#                      "Task ID: A unique identifier for tracking purposes\n" \
#                      "Task Title: Brief description of the specific development work\n" \
#                      "Related User Story: Reference to the parent user story\n" \
#                      "Description: Detailed explanation of the technical work required\n" \
#                      "Acceptance Criteria: Specific requirements that must be met for completion\n" \
#                      "Estimated Effort: Time or complexity estimation\n" \
#                      "Dependencies: Any tasks that must be completed first"
# For the 'agent_to_evaluate' parameter, refer to the provided solution code's pattern.

dataEngEvalCriteria = """
    The answer should be tasks following this exact structure: 
    Task ID: A unique identifier for tracking purposes\n
    Task Title: Brief description of the specific development work\n
    Related User Story: Reference to the parent user story\n
    Description: Detailed explanation of the technical work required\n
    Acceptance Criteria: Specific requirements that must be met for completion\n
    Estimated Effort: Time or complexity estimation\n
    Dependencies: Any tasks that must be completed first
    """

development_engineer_evaluation_agent = EvaluationAgent(
    openai_api_key = openai_api_key,
    persona = persona_dev_engineer_eval,
    evaluation_criteria = dataEngEvalCriteria ,
    worker_agent = development_engineer_knowledge_agent,
    max_interactions = 5
)


# Job function persona support functions
# TODO: 11 - Define the support functions for the routes of the routing agent (e.g., product_manager_support_function, program_manager_support_function, development_engineer_support_function).
# Each support function should:
#   1. Take the input query (e.g., a step from the action plan).
#   2. Get a response from the respective Knowledge Augmented Prompt Agent.
#   3. Have the response evaluated by the corresponding Evaluation Agent.
#   4. Return the final validated response.

def product_manager_support_function(query):
    response = product_manager_knowledge_agent.respond(query)
    evaluation_result = product_manager_evaluation_agent.evaluate(response)
    return evaluation_result['final_response']

def program_manager_support_function(query):
    response = program_manager_knowledge_agent.respond(query)
    evaluation_result = program_manager_evaluation_agent.evaluate(response)
    return evaluation_result['final_response']

def development_engineer_support_function(query):
    response = development_engineer_knowledge_agent.respond(query)
    evaluation_result = development_engineer_evaluation_agent.evaluate(response)
    return evaluation_result['final_response']

# Routing Agent
# TODO: 10 - Instantiate a routing_agent. You will need to define a list of agent dictionaries (routes) for Product Manager, Program Manager, and Development Engineer. Each dictionary should contain 'name', 'description', and 'func' (linking to a support function). Assign this list to the routing_agent's 'agents' attribute.
agentRoutingConfiguration = [
    {
        "name": "Product Manager",
        "description": "Defines only User Stories.",
        "func": product_manager_support_function
    },
    {
        "name": "Program Manager",
        "description": "Formulates only Features.",
        "func": program_manager_support_function
    },
    {
        "name": "Development Engineer",
        "description": "Creates ONLY Engineering Tasks.",
        "func": development_engineer_support_function
    }
]

routing_agent = RoutingAgent(openai_api_key = openai_api_key, agents = agentRoutingConfiguration)


# Run the workflow

print("\n*** Workflow execution started ***\n")
# Workflow Prompt
# ****
workflow_prompt = f"""
                        What would the development tasks for the product?
                   """
# ****
print(f"Task to complete in this workflow, workflow prompt = {workflow_prompt}")

print("\nDefining workflow steps from the workflow prompt")
# TODO: 12 - Implement the workflow.
#   1. Use the 'action_planning_agent' to extract steps from the 'workflow_prompt'.
#   2. Initialize an empty list to store 'completed_steps'.
#   3. Loop through the extracted workflow steps:
#      a. For each step, use the 'routing_agent' to route the step to the appropriate support function.
#      b. Append the result to 'completed_steps'.
#      c. Print information about the step being executed and its result.
#   4. After the loop, print the final output of the workflow (the last completed step).


plannedWorkflowSteps = action_planning_agent.extract_steps_from_prompt(workflow_prompt)
completed_steps = []
plannedWorkflowPlan = " \n".join(plannedWorkflowSteps)
completed_steps.append(f"""
                        STEP DESC: DRAFT PLAN for user request: {workflow_prompt} 
                        STEP OUTCOME: {plannedWorkflowPlan} 
                        """
                       )

print("*********GENERATED PLAN _ BEGIN*********\n")
print(plannedWorkflowSteps)
print("\n*********GENERATED PLAN - END*********")


#plannedWorkflowSteps = []
currentPlan = "Development Plan is EMPTY and requires to be EXTENDED"
for i, step in enumerate(plannedWorkflowSteps):
    print(f"****Workflow Step Execution - BEGIN - Step {i + 1}: {step} ****")
    iterationPrompt = f"""
                       Current task: {step}
                       **************************************************************************************
                       Current plan: {currentPlan}
                       **************************************************************************************
                       """

    stepOutcome = routing_agent.route(iterationPrompt)
    completed_steps.append(f"""
                        STEP DESC: {step} 
                        STEP OUTCOME: {stepOutcome} 
                        """
                       )
    currentPlan = stepOutcome

    print(f"****Workflow Step Execution - RESULT BEGIN - Step {i + 1}: {step} ****\n {stepOutcome}\n")
    print(f"****Workflow Step Execution - RESULT END - Step {i + 1}: {step}")

print("****WORKFLOW EXECUTION ACCOMPLISHED****")

# Print the last completed step, which is the final output of the plan
if completed_steps:
    print("****WORKFLOW OUTPUT****")
    print(completed_steps[-1])



