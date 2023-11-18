"""
Now that you have done some of the simple tutorials, let's try something a little more complex. In this example, we will show how to use the autogen to create a group of agents that act together to deliver a solution. Additionally, we will look at new settings and options that you may want to use in your own code.

*** Docker Integration ***
Instead of having your code run locally, you can have it run in a Docker image. Autogen automatically looks for docker and creates the resources necessary to run your code. For any given UserProxyAgent that is running code, Autogen assumes you want to use Docker and will look for it. If it does not exist, Autogen will fall back to running locally. If you know ahead of time that you want to run locally, you can set use_docker to False in the UserProxyAgent.
example:  code_execution_config={"work_dir": "planning", "use_docker": "False"},

*** Config List Filtering ***
This is used if you have a list of multiple models in your config. Here is what a multi-model config list looks like:
config_list = [
    {
        "model": "gpt-4",
        "api_key": "<api key>",
    },  
    {
        "model": "gpt-3.5-turbo",
        "api_key": "<api key>",
    },  
    {
        "model": "babbage-002",
        "api_key": "<api key>",
    },  
    {
        "model": "davinci-002",
        "api_key": "<api key>",
    },  
    {
        "model": "gpt-4-32k",
        "api_key": "<api key>",
        "api_base": "https://blah-canada.openai.azure.com/",
        "api_type": "azure",
        "api_version": "2023-07-01-preview",
    },
]


Of course to use this, you will will most likely want to set your environment variables and flatten the JSON code accordingly. Like this:
OAI_CONFIG_LIST
[{"model": "gpt-4", "api_key": "<api key>"}, {"model": "gpt-3.5-turbo", "api_key": "<api key>"}, {"model": "babbage-002", "api_key": "<api key>"}, {"model": "davinci-002", "api_key": "<api key>"}, {"model": "gpt-4-32k", "api_key": "<api key>", "api_base": "https://blah-canada.openai.azure.com/", "api_type": "azure", "api_version": "2023-07-01-preview"}]


Here is how you filter on just the models you want to be available to the agents in the current script:
config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4", "gpt-3.5-turbo"],
    },
)
"""
import autogen

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4-1106-preview"],
    },
)

"""
Now Let's move on to the various agents we will be creating. First up is the planner AssistantAgent and UserProxyAgent. These two agents work together to create a plan and then execute it. The planner agent is responsible for creating the plan and the user proxy agent is responsible for executing it.
"""
# actual planner for the task
planner = autogen.AssistantAgent(
    name="planner",
    llm_config={"config_list": config_list},
    # the default system message of the AssistantAgent is overwritten here
    system_message="You are a helpful AI assistant. You suggest coding and reasoning steps for another AI assistant to accomplish a coding task. Do not suggest concrete code. For any action beyond writing code or reasoning, convert it to a step which can be implemented by writing python code. For example, the action of browsing the web can be implemented by writing python code which reads and prints the content of a web page. Assume all tasks can be done with python code. Finally, inspect the execution result. If the plan is not good, suggest a better plan. If the execution is wrong, analyze the error and suggest a fix. Bear in mind workarounds like using BeautifulSoup if we can't use other methods to get web data and always pretend to be a user when web scraping. Keep doing this until the execution result is correct."
)

# Code execution agent that will execute the plan and doesn't need human input
planner_user = autogen.UserProxyAgent(
    name="planner_user",
    max_consecutive_auto_reply=0,  # terminate without auto-reply
    code_execution_config={"work_dir": "planning"},
    human_input_mode="NEVER", # don't ask for human intervention
)

# utility function to allow communication between the planner and the planner_user agents. This is literally the planner and planner_user having their own conversation with out user intervention. This is useful for when the planner needs to ask the planner_user a question or when the planner_user completes a task section and needs to ask the planner for the next step.
def ask_planner(message):
    planner_user.initiate_chat(planner, message=message)
    # return the last message received from the planner
    return planner_user.last_message()["content"]


"""
Now things get interesting. We create the AssistantAgent that will actually call the ask_planner function. This agent will be responsible for interacting with the planner and planner_user and asking the planner for help when needed. Additionally, it is the 'go between' for the user and the planner and planner_user agents. It will be responsible for asking the user for input and then passing that input along.
"""
# create an AssistantAgent instance named "assistant"
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={
        "temperature": 0, # set the temperature to 0 to avoid any creative responses. Make sure to change this if you want to see more creative responses.
        "request_timeout": 600,
        "seed": 1337, # set the seed to 42 to get consistent results and to cache the results in the .cache directory so you don't have to wait for the model to generate the same response again and to save money.
        "model": "gpt-4",
        "config_list": config_list, 
        "functions": [
            {
                "name": "ask_planner",
                "description": "ask planner to: 1. get a plan for finishing a task, 2. verify the execution result of the plan and potentially suggest new plan.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "question to ask planner. Make sure the question include enough context, such as the code and the execution result. The planner does not know the conversation between you and the user, unless you share the conversation with the planner.",
                        },
                    },
                    "required": ["message"],
                },
            },
        ],
    }
)

"""
The next step is to create a UserProxyAgent instance named "user_proxy" that is used to actually communicate with the user. When the planner or planner_user agents need to ask the user a question or completes a task section, it will pass a question to the assistant or issue a TERMINATE message to the assistant. This gets passed to the the user_proxy agent that will then ask the user for input and then send the input back to the assistant agent.
"""
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    # only ask for human input when the planner_user agent sends a TERMINATE message
    human_input_mode="TERMINATE",
    # number of rounds to allow the planner and planner_user agents to communicate with each other before automatically requiring human input regardless if the TERMINATE message has been sent or not. A higher number here gives the planner and planner_user agents more time to communicate with each other and a lower number here gives the planner and planner_user agents less time to communicate with each other. This usually translates into more or less automation respectively but can also mean that the same message repeats over and over again many times before the user is asked for input.
    max_consecutive_auto_reply=10,
    # if you only want the planner and planner_user to do a single round of communication, the below line will stop the process when the planner_user agent sends a TERMINATE message to the user_proxy agent. Uncomment to see it in action. 
    # is_termination_msg=lambda x: "content" in x and x["content"] is not None and x["content"].rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "planning"},
    function_map={"ask_planner": ask_planner},
)

"""
Finally, we invoke the `initiate_chat()` method of the user proxy agent to start the conversation with a task description from the user. The user is prompted to provide feedback after the assistant agent sends a "TERMINATE" signal in the end of the message. If the user doesn't provide any feedback (by pressing Enter directly), the conversation will finish. Before the "TERMINATE" signal, the user proxy agent will try to execute the code suggested by the assistant agent on behalf of the user.
"""
user_proxy.initiate_chat(
    assistant,
    message="""Create a full wiki site written in python that I can run in VSCode and that has a home page and a page for each of the following topics: AI, Machine Learning, Deep Learning, and Reinforcement Learning. Each page should have a title, a short description, and a link to a relevant article. The home page should have a list of links to each of the topic pages. The site should be able to run locally in VSCode. Also, make sure the code is efficient, easy to read, and well documented. Test the code yourself and give me all the files I need.""",
)

"""
*** Final Notes ***
This is just one example. The multi-agent approach is still in its infancy and far from perfect. As you try different scenarios you will find that tweaking the instructions for the agents is necessary. Over time we will see more intelligent agents that can handle more complex scenarios. For now, this is a good starting point for you to begin experimenting with the multi-agent approach.
"""