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
        subprocess.call('lean cloud backtest --push strategy13', stdout=out)
        out.close()
        try:
            out = open("log.txt", "r")
            lines = out.readlines()
            for line in lines:
                if "Net Profit" in line and '%' in line and '$' not in line:
                # if 'Win Rate' in line and '%' in line:
                    # print(line)
                    i = 0
                    while not ('0' <= line[i] <= '9'):
                        i += 1
                    j = i
                    while line[j] != '%':
                        j += 1
                    profit = float(line[i:j - 1])
                    # print("Net Profit:", profit)
                    # print("Win Rate", profit)
                    break
            out.close()
            file = open("strategy13/config.py", "r")
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
                file = open("config13.py", "w")
                file.writelines(lines)
                file.close()
                # print(config.SMMA_SLOW_LENGTH)
                # print(config.SMMA_FAST_LENGTH)
                # print(config.SMMA_FASTEST_LENGTH)
                #
                # print(config.DONCHIAN_PERIOD)
                #
                # print(config.VOLATILITY_PERIOD)
                #
                # print(config.TDI_RSI)
                # print(config.BAND_LENGTH)
                # print(config.FAST_MA_ON_RSI)
                # print(config.SLOW_MA_ON_RSI)
                #
                # print(config.VOLUME_MA_LENGTH)
                #
                # print(config.TEMA_PERIOD)
                # print(config.EMA_PERIOD)
                # print(config.CANDLE_SIZE_FACTOR)
                #
                # print(config.SHORT_ALMA_LENGTH)
                # print(config.LONG_ALMA_LENGTH)
                # print(config.FAST_OFFSET)
                # print(config.FAST_SIGMA)
                # print(config.TREND_OFFSET)
                # print(config.TREND_SIGMA)
                # print(config.SIGNAL_OFFSET)
                # print(config.SIGNAL_SIGMA)
                profit_pre = profit
            config['SMMA_SLOW_LENGTH'] = random.randint(280, 320)
            config['SMMA_FAST_LENGTH'] = random.randint(80, 120)
            config['SMMA_FASTEST_LENGTH'] = random.randint(30, 70)
            config['DONCHIAN_PERIOD'] = random.randint(5, 20)
            config['VOLATILITY_PERIOD'] = random.randint(80, 120)
            config['TDI_RSI'] = random.randint(8, 13)
            config['BAND_LENGTH'] = random.randint(25, 35)
            config['FAST_MA_ON_RSI'] = random.randint(1, 5)
            config['SLOW_MA_ON_RSI'] = random.randint(5, 10)
            config['VOLUME_MA_LENGTH'] = random.randint(20, 60)
            config['TEMA_PERIOD'] = random.randint(45, 65)
            config['EMA_PERIOD'] = random.randint(50, 70)
            config['CANDLE_SIZE_FACTOR'] = random.uniform(0.8, 1.5)
            config['SHORT_ALMA_LENGTH'] = random.randint(3, 7)
            config['LONG_ALMA_LENGTH'] = random.randint(18, 25)
            config['FAST_OFFSET'] = random.uniform(0.25, 1)
            config['FAST_SIGMA'] = random.randint(2, 6)
            config['TREND_OFFSET'] = random.uniform(0.25, 1)
            config['TREND_SIGMA'] = random.randint(2, 6)
            config['SIGNAL_OFFSET'] = random.uniform(0.35, 1)
            config['SIGNAL_SIGMA'] = random.randint(4, 8)
            lines = []
            for key in config.keys():
                lines.append(key + "=" + str(config[key]) + "\n")
            # print(lines)
            file = open("strategy13/config.py", "w")
            file.writelines(lines)
            file.close()
        except Exception as err:
            print(err)
    except Exception as err:
        print(err)

