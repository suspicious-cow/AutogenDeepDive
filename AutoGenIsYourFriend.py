"""
This tutorial will show how to use Microsoft Autogen to create multiple AI agents to create a team to help with just about anything.
Microsoft Autogen is a framework for creating AI agents to take on various personas and become a team to help the user.
Full documentation and many more samples can be found at the Autogen GitHub page: https://github.com/microsoft/autogen/tree/main#readme 

In this initial document, we will take their first example in the documentation and break it down to show how it all works. In other files,
we will show how to use this framework to create a more complex team of agents to help with various tasks.

*** Initial Setup ***
It is strongly recommended (but not required) that you create a virtual environment for this project. This will keep your dependencies separate from other projects and make it easier to manage. I use Anaconda for this purpose, but you can use whatever you are comfortable with. For data scientists, Anaconda is a great choice. You can download it here: https://www.anaconda.com/products/individual

After you install it just create a new environment and activate it. For example, I created an environment called autogen and activated from the Anaconda Prompt with the following commands:
conda create -n autogen python
conda activate autogen


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

*** Running the Code ***
To run any of the files from the command line, just type python <filename>.py. For example, python AutoGenIsYourFriend.py

NOTE: If you created your environment variables after you opened your terminal (which is usually the case), you will need to close and reopen your terminal for the environment variables to be available to the python interpreter.

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



"""
Now we create our agents. In this example, we are creating two agents, an assistant and a user proxy. This is the bare minimum to get started.
The assistant is the agent that will be doing the planning and the user proxy is the agent that will be running code and interacting with the user.
You can see a great graphic of how this will work here: https://github.com/microsoft/autogen/blob/main/website/static/img/chat_example.png

We begin with the assistant. We create an instance of the AssistantAgent class and give it a name. You can have as many assistants as you want, but they must have unique names so you can 
reference them later. We also pass in the config_list we created earlier. This is how the assistant knows how to connect to the OpenAI API.
"""
assistant = AssistantAgent("assistant", llm_config={"config_list": config_list})

"""
Next we create the user proxy. We create an instance of the UserProxyAgent class and give it a name. Just like AssistantAgents, you can have several user proxy agent. Its job, in this example, is to run code and interact with the user. Notice we also pass in the config_list we created earlier. This is how the user proxy knows how to connect to the OpenAI API. However, we add one more parameter, code_execution_config. Sometimes it may just run code without user interaction, for example. 
This is also how we tell the user proxy where to run the code. In this example, we are telling it to run the code in the folder called 'coding' that it will create. This is where we will put any output we indicate.
"""
user_proxy = UserProxyAgent("user_proxy", llm_config={"config_list": config_list}, code_execution_config={"work_dir": "coding"})

"""
Finally, at the end of every autogen script, we need to call the initiate_chat function on the user proxy agent. This is what starts the conversation between all the agents and gets things rolling. Notice we pass in the list of assistants we created (in this case, only one) and we give it a message to start the conversation. This message is what the user proxy will use to start the conversation with the assistant. In this case, we are telling the assistant to plot a chart of the stock price change YTD for NVDA and TESLA.
"""
user_proxy.initiate_chat(assistant, message="Plot a chart of NVDA and TESLA stock price change YTD.")

"""
Now run the code and see what happens. You will be prompted every step of the way to provide feedback, just press Enter to move on to the next step. The first thing you will see is the AssistantAgent suggesting a plan and the code to run for the plan. Then the UserProxyAgent will attempt to run the code but it won't work. The AssistantAgent is notified and it suggests a fix. The UserProxyAgent tries to run that code and this process continues until the code successfully runs. At one point it will show a graph of the stock prices that you can save if you desire. Close the graph. Type exit when done. When it is done,you should see a folder called 'coding' created in the same folder as this script that was used to create temporary files.

When you are done here you can move on to the next tutorial, AutoGenIsYourFriend2.py, where we will show how to tweak this example to make it more useful.
"""