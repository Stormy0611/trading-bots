import subprocess
from strategy.config import set_from_file, save_to_file, randomize

try:
    out = open("log.txt", "w")
    subprocess.call('lean cloud backtest "strategy"', stdout=out)
    out.close()
    try:
        out = open("log.txt", "r")
        lines = out.readlines()
        for line in lines:
            print(line + "           -------------------")
    except Exception as err:
        print(err)
except Exception as err:
    print(err)

