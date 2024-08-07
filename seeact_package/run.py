import asyncio
import os
from seeact.agent import SeeActAgent
import argparse
import toml
import json
from aioconsole import ainput, aprint
from seeact.demo_utils.ranking_model import CrossEncoder, find_topk
import torch 
from collections import defaultdict

# Setup your API Key here, or pass through environment
# os.environ["OPENAI_API_KEY"] = "Your API KEY Here"
# os.environ["GEMINI_API_KEY"] = "Your API KEY Here"

async def run_agent(config_file, task_id, web_task, website, website_name, ranking_model = None):

    agent = SeeActAgent(model="gpt-4o", config_path=config_file, task_id=task_id, default_task=web_task, 
                        default_website=website, default_website_name=website_name, ranking_model=ranking_model)

    # Return 0 if good, 1 if bad
    error_code = await agent.start(headless=True) # start without direct website monitoring
    if not error_code:
        while not agent.complete_flag:
            print(website)
            prediction_dict = await agent.predict()
            await agent.execute(prediction_dict)
        await agent.stop()

async def main(agent_execute):        
    await asyncio.gather(*agent_execute)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config_file", help = "Config file for webagent")
    parser.add_argument("-n", "--num_tasks", type=int, help = "Number of tasks to run from config file")
    args = parser.parse_args()

    with open(args.config_file) as f:
        config_toml = toml.load(f)
    with open(config_toml['experiment']['task_file_path']) as g:
        task_json = json.load(g)

    ranker_path = None
    try:
        ranker_path = config_toml["basic"]["ranker_path"]
        if not os.path.exists(ranker_path):
            ranker_path = None
    except:
        pass

    ranking_model = None
    if ranker_path: #TODO: CHANGE THIS
        ranking_model = CrossEncoder(ranker_path, device=torch.device("cuda" if torch.cuda.is_available() else "cpu"),
                                    num_labels=1, max_length=512, )
        
        print("Ranker model initialized..., path " + ranker_path)

    else:
        print("Ranker model not initialized")

    # Create tasks set such that websites alternate, e.g. no two urls are next to each other
    tasks_set = []
    tasks_dict = defaultdict(list)
    for task in task_json:
        tasks_dict[task['website']].append(task)
    while not all(value == [] for value in tasks_dict.values()):
        for task_key in tasks_dict:
            if len(tasks_dict[task_key]) > 0:
                tasks_set.append(tasks_dict[task_key].pop(0))
            else: 
                continue
        
    agent_execute = []

    i = 0
    for task_json in tasks_set:
        task_id = task_json['task_id']
        web_task = task_json['confirmed_task']
        website = task_json['website']
        website_name = task_json['website_name']
        path_dir = os.path.join(config_toml["basic"]["save_file_dir"], website_name, task_id)

        if os.path.exists(path_dir) and not config_toml['experiment']['overwrite']:
            print(task_id + " results already exist at " + path_dir)
            continue

        # Break after args.num_tasks tasks have been run
        if args.num_tasks is not None and args.num_tasks > 0 and len(agent_execute) >= args.num_tasks:
            break

        agent_execute.append(run_agent(config_file=args.config_file, task_id=task_id, 
                                       web_task=web_task, website=website, website_name=website_name, ranking_model=ranking_model))
        
    print("==" * 25 + f"Number of tasks to execute: {len(agent_execute)}" + "==" * 25) 

    asyncio.run(main(agent_execute))
    