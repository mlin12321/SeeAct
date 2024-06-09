import json

def load_gen_tasks():
    with open('data/gen_web_tasks.json') as f:
        gen_tasks = json.load(f)

    # Problematic non-successes or tasks I had issue with
    filter_twitter = [("Twitter", 14), ("Twitter", 16), ("Twitter", 17), ("Twitter", 20)]
    #filter_netflix = [] Do not consider this because it requires paid account
    #filter_apple_music = [] Do not consider this because it requires paid account
    filter_ebay = [("eBay", 15)]
    filter_glassdoor = [("Glassdoor", 18), ("Glassdoor", 19)]

    

    # Filter out tasks in demo sheet
    filter = filter_twitter + filter_ebay + filter_glassdoor

    # Return filtered tasks
    filtered_gen_tasks = []
    for gen_task in gen_tasks:
        if not (gen_task["website_name"], int(gen_task["task_number"])) in filter and gen_task["website_name"] not in ["Netflix", "Apple Music"]:
            filtered_gen_tasks.append(gen_task)
        
    return filtered_gen_tasks

if __name__ == "__main__":
    filtered_gen_task = load_gen_tasks()
    baby_sample = filtered_gen_task[0]
    # with open('data/gen_filtered_web_tasks.json', 'w') as f:
    #     json.dump(filtered_gen_task, f)

    with open('data/baby_sample.json', 'w') as f:
        json.dump(baby_sample, f)