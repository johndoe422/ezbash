import sys
import subprocess
import os

# System prompt is critical: it forces the LLM to output ONLY the command
SYSTEM_PROMPT = "You are a Linux command generator. Respond with ONLY the single bash command required to accomplish the task. Do not include explanations, quotes, or markdown formatting."

# Use the --extract flag to strip any code fences (```bash) the LLM might include
LLM_COMMAND = "llm '{task}' --extract -s '{system_prompt}'"

def run_llm_command(task):
    """Generates a command using LLM and asks user for approval before running."""
    print("💬 Generating Command...")
    
    command_to_run = LLM_COMMAND.format(
        task=task,
        system_prompt=SYSTEM_PROMPT
    )
    
    # Generate the command using the llm CLI tool
    try:
        # We use check=True to raise an error if the llm call fails
        result = subprocess.run(command_to_run, shell=True, capture_output=True, text=True, check=True)
        generated_command = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"\nError during LLM call: {e.stderr.strip()}")
        return

    if not generated_command:
        print("Failed to generate a command. Please refine your request.")
        return

    print(f"✅ Generated Command:\n   {generated_command}")
    
    # Human Review and Approval (The safety step)
    review = input("Execute this command? (Y/n): ").lower()
    
    if review == 'y' or review =='':
        # Execute the approved command using os.system
        os.system(generated_command)
    else:
        print("\nExecution cancelled by user.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: run 'Your natural language command here'")
        sys.exit(1)
        
    # Reassemble the user's task from the arguments
    user_task = " ".join(sys.argv[1:])
    run_llm_command(user_task)
