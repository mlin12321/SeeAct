cd process_playwright
python process_trace.py \
    --input_pattern "/local/scratch/lin.3976/SeeAct/online_results/Amazon_1/playwright_traces/*" \
    --output_dir "/local/scratch/lin.3976/SeeAct/process_playwright/test"
    # --input_pattern "/local/scratch/lin.3976/SeeAct/online_results/eBay_1/playwright_traces/*" \
    # --output_dir "/local/scratch/lin.3976/SeeAct/process_playwright/test"
    # --dryrun