#*********************************************************************************************
# FILE   NAME:    main.py
# PROJ   NAME:    uOttaHack 7 - deepcode-challenge
# DESCRIPTION:    The main orchestrator to run the tasks sequentially
#
# HOW TO USE:     $ python main.py
#
#
# Contributors:
# - Zechen Zhou     zzhou186@uottawa.ca
# - Benjamin Sam    bsam079@uottawa.ca
#
#
# REVISION HISTORY
# YYYY/MMM/DD     Author                       Comments
# 2025 JAN 18     Zechen Zhou, Benjamin Sam    creation
#
#
#
#*********************************************************************************************

import subprocess

def run_parse_store():
    print("###########################")
    print("Running parse_store.py ...\n")
    subprocess.run(["python", "parse_store.py"], check=True)

def run_enrich_data():
    print("###########################")
    print("Running enrich_data.py ...\n")
    subprocess.run(["python", "enrich_data.py"], check=True)


if __name__ == "__main__":

    print("###############################################")
    print("Starting the breach data processing pipeline...\n")

    # Step 1: Parse and store data
    # run_parse_store()

    # Step 2: Enrich stored data
    # run_enrich_data()