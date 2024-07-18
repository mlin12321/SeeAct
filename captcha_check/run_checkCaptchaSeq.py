import asyncio
import os
from seeact.agent import SeeActAgent
import argparse
import toml
import json
from aioconsole import ainput, aprint
from seeact.demo_utils.ranking_model import CrossEncoder, find_topk
import torch 
import random 
import math

# Setup your API Key here, or pass through environment
# os.environ["OPENAI_API_KEY"] = "Your API KEY Here"
# os.environ["GEMINI_API_KEY"] = "Your API KEY Here"

async def run_agent(config_file, task_id, web_task, website, website_name, ranking_model = None):

    agent = SeeActAgent(model="gpt-4o", config_path=config_file, task_id=task_id, default_task=web_task, 
                        default_website=website, default_website_name=website_name, ranking_model=ranking_model)

    await agent.start(headless=True) # start without direct website monitoring
    while not agent.complete_flag:
        prediction_dict = await agent.predict()
        await agent.execute(prediction_dict)
        sleepInt = random.randint(1, 2)
        await asyncio.sleep(sleepInt) 
    await agent.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config_file", help = "Config file for webagent")
    parser.add_argument("-n", "--num_tasks", type=int, help = "Number of tasks to run from config file")
    args = parser.parse_args()

    with open(args.config_file) as f:
        config_toml = toml.load(f)
    with open(config_toml['experiment']['website_list_path']) as g:
        websites_text = g.read()

    website_list = websites_text.split("\n")
   
    # print(website_list)
    input_websites = [website_str.split(",") for website_str in website_list]
    input_full_names = [input_website[0].strip() for input_website in input_websites]
    input_full_urls = ["https://" + input_website[2].strip() + "/" for input_website in input_websites]
 

    input_names = input_full_names
    input_urls = input_full_urls
    
    task_count = 0

    for website_name, web_url in zip(input_names, input_urls):
        task_id = website_name.replace(" ", "_")
        web_task = "Explore the website to see all of its features"
        website = web_url
        website_name = website_name
        path_dir = os.path.join(config_toml["basic"]["save_file_dir"], task_id)

        if os.path.exists(path_dir) and not config_toml['experiment']['overwrite']:
            print(task_id + " results already exist at " + path_dir)
            continue

        # Break after args.num_tasks tasks have been run
        if args.num_tasks is not None and args.num_tasks > 0 and task_count >= args.num_tasks:
            break

        asyncio.run(run_agent(config_file=args.config_file, task_id=task_id, 
                                    web_task=web_task, website=website, website_name=website_name))
        
        task_count += 1


            