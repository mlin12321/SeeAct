import asyncio
import os
from seeact.agent import SeeActAgent
import argparse
import toml
import json
from aioconsole import ainput, aprint
from concurrent.futures import ProcessPoolExecutor, as_completed

# Create a SeeAct agent for a single task, and run that task to completion
async def run_agent(config_file, task_id, web_task, website, website_name):

    agent = SeeActAgent(model="gpt-4o", config_path=config_file, task_id=task_id, default_task=web_task, 
                        default_website=website, default_website_name=website_name)

    await agent.start(headless=True) # start without direct website monitoring
    while not agent.complete_flag:
        prediction_dict = await agent.predict()
        await agent.execute(prediction_dict)
    await agent.stop()

# Gather all SeeAct agents and excute at the same time
async def gather_agents(agents_to_run):
    await asyncio.gather(*agents_to_run)

# Start all the SeeAct agents
# Basically only exists because asyncio.gather doesn't work with non-async functions
def execute_agents(agents_to_run):
    asyncio.run(gather_agents(agents_to_run))

if __name__ == "__main__":
    # Get args
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config_file", help = "Config file for webagent")
    parser.add_argument("-np", "--num_processes", type=int, help = "Number of processes to run script over")
    args = parser.parse_args()

    # Read configs from toml (to pass into SeeAct) and tasks in json file
    with open(args.config_file, 'r') as f:
        config_toml = toml.load(f)
    with open(config_toml['experiment']['task_file_path']) as g:
        tasks_json = json.load(g)

    # TODO: Magic number to limit number of tasks being executed
    # This is to avoid running too many websites at once and triggering anti-bot detection
    tasks_set = tasks_json[:80] 
    
    # Get all task info info_to_run, for tasks that have yet to be executed, 
    # and put it inside an array
    agent_to_run = []
    for task_json in tasks_set:
        task_id = task_json['task_id']
        web_task = task_json['confirmed_task']
        website = task_json['website']
        website_name = task_json['website_name']
        path_dir = os.path.join(config_toml["basic"]["save_file_dir"], task_id)

        # Skip tasks done before (not necessary since there are checks in agent.py)
        # but this makes things cleaner
        if os.path.exists(path_dir) and not config_toml['experiment']['overwrite']:
            print(task_id + " results already exist at " + path_dir)
            continue

        # Append the list of tasks/agents to run for later
        agent_to_run.append(run_agent(config_file=args.config_file, task_id=task_id, 
                                       web_task=web_task, website=website, website_name=website_name))
        
    # Now split the list into multiple chunks for each of the proccesses to handle
    agent_execute = []
    for i in range(0, args.num_processes):
        agent_execute.append(agent_to_run[i::args.num_processes])

    # Assert agent lists do not have nontrivial intersections (redudancy, and will cause write errors)
    assert not \
        set.intersection(*[set(agent_execute_subset) for agent_execute_subset in agent_execute]), \
        "Agent executes arrays have nontrivial intersection (redudancy and will cause write errors)"
 
    # Put agents in the agent pool and execute them
    with ProcessPoolExecutor(max_workers=args.num_processes) as pool:
        for agent_execute_subset in agent_execute:
            pool.map(execute_agents, agent_execute_subset)
       
        # agent_maker = [pool.submit(execute_agents, agent_execute_subset) for agent_execute_subset in agent_execute]
        # for agent_make in as_completed(agent_maker):
        #     pass
      
    