import asyncio
import os
from seeact_captcha.agent import SeeActAgent
import argparse
import toml
import json
from aioconsole import ainput, aprint
from seeact_captcha.demo_utils.ranking_model import CrossEncoder, find_topk
import torch 
import random 
import math

# Setup your API Key here, or pass through environment
# os.environ["OPENAI_API_KEY"] = "Your API KEY Here"
# os.environ["GEMINI_API_KEY"] = "Your API KEY Here"

async def run_agent(config_file, task_id, web_task, website, website_name, cat, ranking_model = None):

    agent = SeeActAgent(config_path=config_file, task_id=task_id, default_task=web_task, 
                        default_website=website, default_website_name=website_name, ranking_model=ranking_model, cat=cat)

    # Return 0 if good, 1 if bad
    error_code = await agent.start(headless=True) # start without direct website monitoring (headless=True)
    if not error_code:
        while not agent.complete_flag:
            try: 
                print(f"PASS TEST 0 - {website}")
                print(website)
                prediction_dict = await agent.predict()
                print(f"PASS TEST 1 - {website}")
                await agent.execute(prediction_dict)
                print(f"PASS TEST 2 - {website}")
                await asyncio.sleep(2) 
                print(f"PASS TEST 3 - {website}")

            except:
                pass
        
        await agent.stop()

        print(f"FINISHED PASS ON {website}")

async def main(agent_execute):        
    await asyncio.gather(*agent_execute)

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
    # input_full_names = [input_website[0].strip().replace(" ", "_") for input_website in input_websites]
    # input_cats = [input_website[1].strip().replace(" ", "_") for input_website in input_websites]
    # input_full_urls = ["https://" + input_website[2].strip() + "/" for input_website in input_websites]
 

    print(len(input_websites))

    tasks_per_set = 10
    steps = math.ceil(len(input_websites) / tasks_per_set)
    for i in range(steps):
        input_sites = input_websites[i * tasks_per_set: (i + 1) * tasks_per_set ] 
 
        agent_execute = []

        print(f"===PASS {i}===")
        
    
        for site_info in input_sites:
            # print(site_info)
            task_id = site_info[0].strip().replace(" ", "_") #Site name
            web_task = "Explore the website to see all of its features"
            input_cat = site_info[1].strip().replace(" ", "_") #input category url
            website_url = "https://" + site_info[2].strip().replace(" ", "_") + "/" #Site url
            website_name = task_id
            path_dir = os.path.join(config_toml["basic"]["save_file_dir"], input_cat, task_id)
            if os.path.exists(path_dir) and not config_toml['experiment']['overwrite']:
                print(task_id + " results already exist at " + path_dir)
                continue

            # Break after args.num_tasks tasks have been run
            if args.num_tasks is not None and args.num_tasks > 0 and len(agent_execute) >= args.num_tasks:
                break

            agent_execute.append(run_agent(config_file=args.config_file, task_id=task_id, 
                                        web_task=web_task, website=website_url, website_name=website_name, cat=input_cat))

        # print(len(agent_execute)) 

        asyncio.run(main(agent_execute))
        