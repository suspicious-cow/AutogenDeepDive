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


""" 
Ingest our config information from our OAI_CONFIG_LIST environment variable
Technically, you can also set config_list directly as a list, for example, config_list = [{'model': 'gpt-4', 'api_key': '<your OpenAI API key here>'},]  
But that would expose your API key in the code, which is not a good idea.

At this point you are probably wondering why we had to create two environment variables when only one is referenced in the code.
This is because the OPENAI_API_KEY is used by the autogen under the hood in various places and is required to be set or the code will not run. Give it a try to see what I mean. 
"""
config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")




assistant = AssistantAgent("assistant", llm_config={"config_list": config_list})
user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding"})
user_proxy.initiate_chat(assistant, message="Plot a chart of NVDA and TESLA stock price change YTD.")
# This initiates an automated chat between the two agents to solve the task