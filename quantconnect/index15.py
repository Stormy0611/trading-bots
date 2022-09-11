import subprocess
import strategy.config as config
import json
import random
import datetime

profit = 0
profit_pre = 0

# while int(datetime.datetime.today().strftime("%H%m")) != 0:
#     pass


while True:
    try:
        out = open("log.txt", "w")
        subprocess.call('lean cloud backtest --push strategy15', stdout=out)
        out.close()
        try:
            out = open("log.txt", "r")
            lines = out.readlines()
            for line in lines:
                if "Net Profit" in line and '%' in line and '$' not in line:
                    # print(line)
                    i = 0
                    while not ('0' <= line[i] <= '9'):
                        i += 1
                    j = i
                    while line[j] != '%':
                        j += 1
                    profit = float(line[i:j - 1])
                    print("Net Profit:", profit)
                    break
            out.close()
            file = open("strategy15/config.py", "r")
            lines = file.readlines()
            config = {}
            for line in lines:
                list = line.split("=")
                try:
                    config[list[0]] = int(list[1])
                except:
                    config[list[0]] = float(list[1])
            file.close()
            # print(config)
            if profit - profit_pre > 0:
                print(profit_pre, " >>>> ", profit)
                print(config)
                lines = []
                for key in config.keys():
                    lines.append(key + "=" + str(config[key]) + "\n")
                # print(lines)
                file = open("config15.py", "w")
                file.writelines(lines)
                file.close()
                profit_pre = profit
            config['VOL_MA'] = random.randint(30, 50)
            config['VWMA_FASTEST'] = random.randint(10, 30)
            config['VWMA_FAST'] = random.randint(40, 60)
            config['VWMA_SLOW'] = random.randint(80, 120)
            config['VWMA_SLOWEST'] = random.randint(180, 220)
            config['VOL_OSC_SHORT'] = random.randint(20, 30)
            config['VOL_OSC_LONG'] = random.randint(40, 60)
            config['PGO_LB_LENGTH'] = random.randint(80, 100)
            config['TSI_LONG'] = random.randint(15, 35)
            config['TSI_SHORT'] = random.randint(10, 15)
            config['TSI_SIGNAL'] = random.randint(10, 15)
            config['RVGI_LENGTH'] = random.randint(15, 25)
            config['STC_LENGTH'] = random.randint(10, 15)
            config['STC_FAST'] = random.randint(20, 30)
            config['STC_SLOW'] = random.randint(40, 60)
            config['STC_AAA'] = random.uniform(0.3, 0.8)
            config['KRI_LENGTH'] = random.randint(20, 35)
            config['VWAP_LENGTH'] = random.randint(20, 30)
            lines = []
            for key in config.keys():
                lines.append(key + "=" + str(config[key]) + "\n")
            # print(lines)
            file = open("strategy15/config.py", "w")
            file.writelines(lines)
            file.close()
        except Exception as err:
            print(err)
    except Exception as err:
        print(err)

