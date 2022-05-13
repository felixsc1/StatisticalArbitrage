from subprocess import run
from time import sleep


"""
Runs a script and restarts it after a crash.
Since there are still many unhandled exceptions possible with the bot (request timeouts etc.), this is a quick workaround.

Subprocess might not show any output (print statements...)
try this: https://stackoverflow.com/questions/4417546/constantly-print-subprocess-output-while-process-is-running/4417735#4417735

Based on https://stackoverflow.com/questions/63021166/how-to-restart-a-python-program-after-it-crashes
"""

# Path and name to the script you are trying to start
file_path = "c:/GitRepos/StatisticalArbitrage/Execution/main_execution.py"

restart_timer = 2


def start_script():
    try:
        # Use the venv python, same command that vscode runs:
        run("c:/GitRepos/StatisticalArbitrage/venv/Scripts/python.exe " +
            file_path, check=True)
    except:
        # Script crashed, lets restart it!
        handle_crash()


def handle_crash():
    print("bot crashed! restarting...")
    sleep(restart_timer)  # Restarts the script after 2 seconds
    start_script()


start_script()
