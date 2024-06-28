import asyncio
import os
from seeact.agent import SeeActAgent
import argparse
import toml
import json
from aioconsole import ainput, aprint

# Setup your API Key here, or pass through environment
# os.environ["OPENAI_API_KEY"] = "Your API KEY Here"
# os.environ["GEMINI_API_KEY"] = "Your API KEY Here"

async def run_agent(config_file, task_id, web_task, website, website_name):

    # print(50 * "++")
    # print("Next Website?")
    # permission = None 
    # while permission != "Continue":
    #     permission = await ainput('Type Continue to continue: ')
    #     permission = permission.strip()
    # print(50 * "==")

    agent = SeeActAgent(model="gpt-4o", config_path=config_file, task_id=task_id, default_task=web_task, 
                        default_website=website, default_website_name=website_name)

    await agent.start(headless=True) # start without direct website monitoring
    while not agent.complete_flag:
        prediction_dict = await agent.predict()
        await agent.execute(prediction_dict)
    await agent.stop()

async def main(args, tasks_json):
    agent_execute = []

    for task_json in tasks_json:
        task_id = task_json['task_id']
        web_task = task_json['confirmed_task']
        website = task_json['website']
        website_name = task_json['website_name']
        path_dir = os.path.join(config_toml["basic"]["save_file_dir"], task_id)

        if os.path.exists(path_dir) and not config_toml['experiment']['overwrite']:
            print(task_id + " results already exist at " + path_dir)
            continue

        agent_execute.append(run_agent(config_file=args.config_file, task_id=task_id, 
                                       web_task=web_task, website=website, website_name=website_name))
        
    await asyncio.gather(*agent_execute)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config_file", help = "Config file for webagent")
    args = parser.parse_args()

    with open(args.config_file, 'r') as f:
        config_toml = toml.load(f)
    with open(config_toml['experiment']['task_file_path']) as g:
        tasks_json = json.load(g)

    tasks_set = tasks_json[:10]

    asyncio.run(main(args, tasks_set))
    