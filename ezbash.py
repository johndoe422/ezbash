import sys
import subprocess
import os
import platform
import shutil
import re

SYSTEM_PROMPT = (
    "You are a Linux command generator. Respond with ONLY the single bash command required "
    "to accomplish the task. Do not include explanations, quotes, or markdown formatting."
)

LLM_COMMAND = "llm '{task}' --extract -s '{system_prompt}'"
CONTEXT_FILE = os.path.join(os.path.dirname(__file__), "context.txt")

def detect_context():
    """Auto-detects minimal system context and returns as a compact one-liner."""
    # Detect OS and package manager
    os_info = ""
    try:
        with open("/etc/os-release") as f:
            data = f.read()
            if "Ubuntu" in data:
                os_info = "ubuntu" + re.search(r'VERSION_ID="([^"]+)"', data).group(1)
                pm = "apt"
                init = "systemd"
            elif "Red Hat" in data or "CentOS" in data or "Fedora" in data:
                os_info = "rhel"
                pm = "dnf"
                init = "systemd"
            elif "Alpine" in data:
                os_info = "alpine"
                pm = "apk"
                init = "busybox"
            elif "Arch" in data:
                os_info = "arch"
                pm = "pacman"
                init = "systemd"
            else:
                os_info = platform.system().lower()
                pm = "apt"
                init = "systemd"
    except:
        os_info = platform.system().lower()
        pm = "apt"
        init = "systemd"

    # Detect sudo availability
    sudo = "true" if shutil.which("sudo") else "false"
    # Shell
    shell = os.path.basename(os.environ.get("SHELL", "bash"))
    # Architecture
    arch = platform.machine()
    
    context_line = f"os={os_info} pm={pm} init={init} shell={shell} sudo={sudo} arch={arch} noninteractive=true"
    return context_line

def get_context():
    """Loads or creates context.txt"""
    if not os.path.exists(CONTEXT_FILE):
        print("Preparing for the first run...")
        context_line = detect_context()
        with open(CONTEXT_FILE, "w") as f:
            f.write(context_line + "\n")
    else:
        with open(CONTEXT_FILE) as f:
            context_line = f.read().strip()
    return context_line

def run_llm_command(task):
    context = get_context()
    print("Generating Command...")
    full_task = f"Context: {context}  Task: {task}"

    command_to_run = LLM_COMMAND.format(
        task=full_task,
        system_prompt=SYSTEM_PROMPT
    )

    try:
        result = subprocess.run(command_to_run, shell=True, capture_output=True, text=True, check=True)
        generated_command = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"\nError during LLM call: {e.stderr.strip()}")
        return

    if not generated_command:
        print("Failed to generate a command. Please refine your request.")
        return

    print(f"✅ Generated Command:\n   {generated_command}")
    
    review = input("Execute this command? (Y/n): ").lower()
    
    if review in ('y', ''):
        os.system(generated_command)
    else:
        print("\nExecution cancelled by user.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: run 'Your natural language command here'")
        sys.exit(1)

    user_task = " ".join(sys.argv[1:])
    run_llm_command(user_task)
