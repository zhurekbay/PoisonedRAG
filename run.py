import os
import time

def run(test_params):
    # Get the log name for file saving within main.py
    log_file, log_name = get_log_name(test_params)

    # --- MODIFIED COMMAND ---
    # 1. Removed 'nohup' (so it runs in foreground)
    # 2. Removed '&' (so it waits for completion)
    # 3. Removed '> {log_file}' (so output prints to screen)
    cmd = f"python3 -u main.py \
        --eval_model_code {test_params['eval_model_code']}\
        --eval_dataset {test_params['eval_dataset']}\
        --split {test_params['split']}\
        --query_results_dir {test_params['query_results_dir']}\
        --model_name {test_params['model_name']}\
        --top_k {test_params['top_k']}\
        --use_truth {test_params['use_truth']}\
        --gpu_id {test_params['gpu_id']}\
        --attack_method {test_params['attack_method']}\
        --adv_per_query {test_params['adv_per_query']}\
        --score_function {test_params['score_function']}\
        --repeat_times {test_params['repeat_times']}\
        --M {test_params['M']}\
        --seed {test_params['seed']}\
        --name {log_name}"
        
    print(f"[-] Starting attack on {test_params['eval_dataset']} with {test_params['model_name']}...")
    print(f"[-] Executing command: {cmd}\n")
    
    # Execute the command locally
    os.system(cmd)


def get_log_name(test_params):
    # Generate a log file name (folder structure)
    os.makedirs(f"logs/{test_params['query_results_dir']}_logs", exist_ok=True)

    if test_params['use_truth']:
        log_name = f"{test_params['eval_dataset']}-{test_params['eval_model_code']}-{test_params['model_name']}-Truth--M{test_params['M']}x{test_params['repeat_times']}"
    else:
        log_name = f"{test_params['eval_dataset']}-{test_params['eval_model_code']}-{test_params['model_name']}-Top{test_params['top_k']}--M{test_params['M']}x{test_params['repeat_times']}"
    
    if test_params['attack_method'] != None:
        log_name += f"-adv-{test_params['attack_method']}-{test_params['score_function']}-{test_params['adv_per_query']}-{test_params['top_k']}"

    if test_params['note'] != None:
        log_name = test_params['note']
    
    return f"logs/{test_params['query_results_dir']}_logs/{log_name}.txt", log_name


# --- CONFIGURATION ---
test_params = {
    # beir_info
    'eval_model_code': "contriever",
    'eval_dataset': "nq",
    'split': "test",
    'query_results_dir': 'main',

    # LLM setting
    # CHANGED: Use gpt-3.5-turbo for cheaper/faster testing. 
    # Change back to 'gpt-4-0613' if you have the budget/access.
    'model_name': 'gpt-3.5-turbo', 
    'use_truth': False,
    'top_k': 5,
    'gpu_id': 0,

    # attack
    'attack_method': 'LM_targeted',
    'adv_per_query': 5,
    'score_function': 'dot',
    'repeat_times': 10,
    'M': 10,
    'seed': 12,

    'note': None
}

# --- EXECUTION LOOP ---
# We only run 'nq' (Natural Questions) to start. 
# Running multiple at once on 16GB RAM is risky.
target_datasets = ['nq'] 
# target_datasets = ['nq', 'hotpotqa', 'msmarco'] # Uncomment this later if NQ works

for dataset in target_datasets:
    test_params['eval_dataset'] = dataset
    run(test_params)
    print(f"\n[+] Finished {dataset}. Sleeping for 5 seconds...\n")
    time.sleep(5)