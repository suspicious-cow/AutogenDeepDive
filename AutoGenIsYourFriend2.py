"""
This tutorial will show how to use Microsoft Autogen to create multiple AI agents to create a team to help with just about anything.
Microsoft Autogen is a framework for creating AI agents to take on various personas and become a team to help the user.
Full documentation and many more samples can be found at the Autogen GitHub page: https://github.com/microsoft/autogen/tree/main#readme 

In this initial document, we will take their first example in the documentation and break it down to show how it all works. In other files,
we will show how to use this framework to create a more complex team of agents to help with various tasks.

*** Install Autogen ***
Before you can do anything you need to make sure to have autogen intstalled for python. You can do this by running the following command in your terminal:
pip install pyautogen

*** Setting Environment Variables ***
Before you can use Autogen, you need to set two system environment variables. I've included the formats and some guidance on just using the OpenAI API directly or through Azure OpenAI.
See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints

# Connecting to OpenAI API directly
OAI_CONFIG_LIST  
[{"model": "<model name i.e. gpt-4, gpt-4-32k, etc.>", "api_key": "<generated api key (I suggest you generate a new one that can be revoked if it is compromised)>"}]
NOTE:this is in JSON format as required by the config_list_from_json function shown later

OPENAI_API_KEY
<same api key used in OAI_CONFIG_LIST>


# Connecting to Azure OpenAI API
OAI_CONFIG_LIST
[{"model": "<name of your deployment (aka engine) NOT the actual model name, i.e. mycooldeployment NOT gpt-4>", "api_key": "<api key>", "api_base": "< example: https://blah-canada.openai.azure.com/>", "api_type": "azure", "api_version": "< have to use 'show code' in the Azure OpenAI Studio chat playground to get this info> "}]

OPENAI_API_KEY
<same api key used in OAI_CONFIG_LIST>

"""
# import the autogen library elements we need
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

# get our config information from our OAI_CONFIG_LIST environment variable
config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

"""
Before we move on, take a minute to appreciate the fact that the code you ran previously is all you need to create a fully functional AI agent that can interact with a user.
In just four lines of code you have a fully functional chat bot that can interact with a user and do just about anything you want. But wait! there's more!
I'm not sure about you, but I want to do more than just chat with a bot. I want to be able to do things like plot a chart, or get the weather, or do anything without me if possible.
Also, I'd like to have some artifacts afterward that I can use to share with others. This is where the power of Autogen really shines.
Let's make those changes!
"""

"""
Now let's make a couple of changes: 
First, let's modify the user proxy prompt to save the code and the plot image to our working folder. Since we don't want to interact, we will also tell the agent to not show the plot image.
Second, we need to tell the user proxy that we don't want to interact with the user. Just do the work and save the artifacts. This is accomplished by adding two settings: max_consecutive_auto_reply to 0 and human_input_mode to NEVER. See the changes we made below. 
"""

assistant = AssistantAgent("assistant", llm_config={"config_list": config_list})

user_proxy = UserProxyAgent("user_proxy", llm_config={"config_list": config_list}, code_execution_config={"work_dir": "coding"}, human_input_mode="NEVER")

user_proxy.initiate_chat(assistant, message="Plot a chart of NVDA and TESLA stock price change YTD. Then save the code and the plot image to my working folder. Don't show me the plot image just save it.")

