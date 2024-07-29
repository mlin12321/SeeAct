import argparse
import asyncio
import glob
import os
import shutil 
import json

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--input_pattern", type=str, required=True)
    args.add_argument("--output_dir", type=str, required=True)
    args = args.parse_args()

    # Store ids related to playwright traces and the processed ids
    playwright_ids = [] 
    processed_ids = []

    # Dirs related to playwright traces and processed screenshots
    playwright_traces = os.path.join(args.input_pattern, "playwright_traces/*")
    processed_steps = os.path.join(args.input_pattern, "processed_steps/*")

    # Collect and append the ids of all playwright traces
    for trace_file in glob.glob(playwright_traces):
        trace_id = trace_file.split("/")[-1].split(".")[0]
        # print(trace_file)
        playwright_ids.append(int(trace_id))

    # Process all unprocessed datapoints 
    # i.e., all actions that yet to have an processed screenshot
    for processed_step in glob.glob(processed_steps):
        # print(trace_file)
        process_id = processed_step.split("/")[-1].split("_")[-1]
        processed_ids.append(int(process_id))

    playwright_ids.sort()
    processed_ids.sort()

    print(args.input_pattern)

    # Id of the last stable playwright trace
    # (i.e. trace_to_image was able to generate a screenshot)
    last_processed_id = processed_ids[0]
    
    # Iterate all elements and process / copy them 
    for playwright_id in playwright_ids:

        # For playwright ids that have not been processed...
        if playwright_id not in processed_ids:
            miss_step_dir = os.path.join(args.input_pattern, "processed_steps", f"step_{playwright_id}", "snapshots")
            process_step_dir = os.path.join(args.input_pattern, "processed_steps", f"step_{last_processed_id}", "snapshots")

            if not os.path.exists(miss_step_dir):
                os.makedirs(miss_step_dir)

            # print("HEADERS IN CONTENT JSON ARE:")

            # print(process_content_json[0].keys())
            # print("HEADERS IN SCREENSHOT JSON ARE:")
            # print(process_screenshot_json[0].keys())

            snapshot_files = os.listdir(process_step_dir)
            
            # Remove nont-interesting actions from the process_step_dir
            # This is mostly irrevelant except for the fact that my data files aren't super consistent
            # So this catches most of the problem files
            if "Page.screenshot_before.mhtml" in snapshot_files:
                snapshot_files.remove("Page.screenshot_before.mhtml")
            if "Page.screenshot_after.mhtml" in snapshot_files:
                snapshot_files.remove("Page.screenshot_after.mhtml")
            if len(snapshot_files) >= 4 and "Page.evaluate_after.mhtml" in snapshot_files:
                snapshot_files.remove("Page.evaluate_before.mhtml")
                snapshot_files.remove("Page.evaluate_after.mhtml")

            snapshot_files.sort()

            html_copy = None
            # Sorting should mean x_after.mhtml comes before x_before.mhtml in snapshots
            # Want after html if playwright_id less than because if processed_id is greater than playwright_id,
            # the after html would be the input of the current playwright
            # Conversely other way around as well.
            if playwright_id < last_processed_id:
                # "X_before.mhtml"
                html_copy = snapshot_files[1]
                # print(f"Playwright_id < last_processed_id, html copy is {html_copy}")
            else:
                # "X_after.mhtml"
                html_copy = snapshot_files[0]
                # print(f"Playwright_id >= last_processed_id, html copy is {html_copy}")

            # Get action id from target of interest
            act_id = html_copy.split("_")[0]
            new_content_json = {}
            new_screenshot_json = {}

            process_content_path = os.path.join(args.input_pattern, "processed_steps", f"step_{last_processed_id}", "content.json")
            process_screenshot_path = os.path.join(args.input_pattern, "processed_steps", f"step_{last_processed_id}", "screenshot.json")
            with open(process_content_path) as f:
                process_content_json = json.load(f)
            with open(process_screenshot_path) as f:
                process_screenshot_json = json.load(f)

            for i in range(len(process_content_json)):
                if process_content_json[i]['action_uid'] == act_id:
                    # print(f"ACT ID FOUND, act id is {act_id} and found id is {process_content_json[i]['action_uid']}")
                    new_content_json = process_content_json[i]
                    new_screenshot_json = process_screenshot_json[i]

                    break
      
            new_content_json['action_uid'] = None
            new_content_json['action'] = None
            new_screenshot_json['action_uid'] = None
            new_screenshot_json['action'] = None

            if playwright_id < last_processed_id:
                new_content_json['after'] = new_content_json['before'] 
                new_screenshot_json['after'] = new_screenshot_json['before'] 
            else:
                new_content_json['before'] = new_content_json['after'] 
                new_screenshot_json['before'] = new_screenshot_json['after'] 

            new_content_path = os.path.join(args.input_pattern, "processed_steps", f"step_{playwright_id}", "content.json")
            new_screenshot_path = os.path.join(args.input_pattern, "processed_steps", f"step_{playwright_id}", "screenshot.json")
            with open(new_content_path, 'w') as f:
                json.dump(new_content_json, f)
            with open(new_screenshot_path, 'w') as f:
                json.dump(new_screenshot_json, f)

            shutil.copyfile(
                os.path.join(process_step_dir, html_copy),
                os.path.join(miss_step_dir, "inaction_before.mhtml")
            ) 

            shutil.copyfile(
                os.path.join(process_step_dir, html_copy),
                os.path.join(miss_step_dir, "inaction_after.mhtml")
            )

            # if not os.path.exists(os.path.join(args.input_pattern, "unmarked_screenshots", f"unmarked_screen_{playwright_id}.png")):
            #     unmark_screen_path = os.path.join(args.input_pattern, "unmarked_screenshots", f"unmarked_screen_{playwright_id}.png")
            #     print(f"{unmark_screen_path} already exists")
            #     shutil.copyfile(
            #         os.path.join(args.input_pattern, "unmarked_screenshots", f"unmarked_screen_{last_processed_id}.png"), 
            #         os.path.join(args.input_pattern, "unmarked_screenshots", f"unmarked_screen_{playwright_id}.png")
            #     )

            processed_ids.append(playwright_id)
        # Else move up the processed in counter
        else:
            last_processed_id = playwright_id

        # # Add a last screenshot
        # if playwright_id == playwright_ids[-1] and \
        #     not os.path.exists(os.path.join(args.input_pattern, "unmarked_screenshots", f"unmarked_screen_{playwright_id + 1}.png")):

        #     shutil.copyfile(
        #         os.path.join(args.input_pattern, "unmarked_screenshots", f"unmarked_screen_{last_processed_id}.png"), 
        #         os.path.join(args.input_pattern, "unmarked_screenshots", f"unmarked_screen_{playwright_id + 1}.png")
        #     )