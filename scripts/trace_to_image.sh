DATA_DIR="/local/scratch/lin.3976/SeeAct/online_results/Amazon_8"
INPUT_PAT="$DATA_DIR/playwright_traces/*"
INPUT_PAT="/local/scratch/lin.3976/SeeAct/online_results/Amazon_8/playwright_traces/*"
OUTPUT_DIR=$DATA_DIR

# python process_playwright/trace_to_image.py \
#     --input_pattern "/local/scratch/lin.3976/SeeAct/online_results/Facebook_19/playwright_traces/*" \
#     --output_dir "/local/scratch/lin.3976/SeeAct/online_results/Facebook_19"

# # "Fill" in missing images
# # Usually b/c action doesn't effect playwright so nothing is changed. Easier just to fill in post.
# python process_playwright/fill_miss_data.py \
#     --input_pattern "/local/scratch/lin.3976/SeeAct/online_results/Youtube_9" \
#     --output_dir "/local/scratch/lin.3976/SeeAct/online_results/Youtube_9"

for set in online_results/*/ ; do
    for website_set in $set*/ ; do
        for task in $website_set*/ ; do
            # Convert all traces to raw images
            # python process_playwright/trace_to_image.py \
            #     --input_pattern "/local/scratch/lin.3976/SeeAct/"$task"playwright_traces/*" \
            #     --output_dir "/local/scratch/lin.3976/SeeAct/"$task

            #"Fill" in missing images
            # Usually b/c action doesn't effect playwright so nothing is changed. Easier just to fill in post.
            python process_playwright/fill_miss_data.py \
                --input_pattern "/local/scratch/lin.3976/SeeAct/"$task \
                --output_dir "/local/scratch/lin.3976/SeeAct/"$task
        done
    done
done