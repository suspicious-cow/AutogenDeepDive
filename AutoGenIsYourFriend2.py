
# import the autogen library elements we need
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

# get our config information from our OAI_CONFIG_LIST environment variable
config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

"""
Before we move on, take a minute to appreciate the fact that the code you ran previously is all you need to create a fully functional AI agent that can interact with a user.
In just four lines of code you have a fully functional chat bot that can interact with a user and do just about anything you want. But wait! There's more!
I'm not sure about you, but I want to do more than just chat with a bot. I want the agents to be able to do things like plot a chart, or get the weather, or do anything without me if possible. Also, I'd like to have some artifacts afterward that I can use to share with others. This is where the power of Autogen really shines.
Let's make those changes!
"""

"""
Now let's make a couple of changes: 
First, let's modify the user proxy prompt to save the code and the plot image to our working folder. Since we don't want to interact, we will also tell the agent to not show the plot image.
Second, we need to tell the user proxy that we don't want to interact with the user. Just do the work and save the artifacts. This is accomplished by adding human_input_mode to NEVER. See the changes we made below then run the code and see the magic happen :)

When you are done, move on to MultiAgentMadness.py for a deeper dive into the power of Autogen.
"""

assistant = AssistantAgent("assistant", llm_config={"config_list": config_list})

user_proxy = UserProxyAgent("user_proxy", llm_config={"config_list": config_list}, code_execution_config={"work_dir": "coding"}, human_input_mode="NEVER")

user_proxy.initiate_chat(assistant, message="Plot a chart of NVDA and TESLA stock price change YTD. Then save the code and the plot image to my working folder. Don't show me the plot image just save it.")

# NOTE: One technique I've found that works well to avoid the planners showing any visuals is just to put in the prompt "Don't show me any visuals, I'm blind." It seems to retain that more than other instructions for some reason.