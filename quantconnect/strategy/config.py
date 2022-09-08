import json
import random


SMMA_SLOW_LENGTH = 300
SMMA_FAST_LENGTH = 100
SMMA_FASTEST_LENGTH = 50

DONCHIAN_PERIOD = 10

VOLATILITY_PERIOD = 100

TDI_RSI = 11
BAND_LENGTH = 31
FAST_MA_ON_RSI = 1
SLOW_MA_ON_RSI = 9

VOLUME_MA_LENGTH = 40

TEMA_PERIOD = 55
EMA_PERIOD = 60
CANDLE_SIZE_FACTOR = 1.1

SHORT_ALMA_LENGTH = 5
LONG_ALMA_LENGTH = 21
FAST_OFFSET = 0.75
FAST_SIGMA = 4
TREND_OFFSET = 0.75
TREND_SIGMA = 4
SIGNAL_OFFSET = 0.85
SIGNAL_SIGMA = 6


def set_from_file():
    try:
        config_file = open("config.json", "r")
        config = json.load(config_file)
        config_file.close()
        variables = globals()
        variables['SMMA_SLOW_LENGTH'] = config['SMMA_SLOW_LENGTH']
        variables['SMMA_FAST_LENGTH'] = config['SMMA_FAST_LENGTH']
        variables['SMMA_FASTEST_LENGTH'] = config['SMMA_FASTEST_LENGTH']
        variables['DONCHIAN_PERIOD'] = config['DONCHIAN_PERIOD']
        variables['VOLATILITY_PERIOD'] = config['VOLATILITY_PERIOD']
        variables['TDI_RSI'] = config['TDI_RSI']
        variables['BAND_LENGTH'] = config['BAND_LENGTH']
        variables['FAST_MA_ON_RSI'] = config['FAST_MA_ON_RSI']
        variables['SLOW_MA_ON_RSI'] = config['SLOW_MA_ON_RSI']
        variables['VOLUME_MA_LENGTH'] = config['VOLUME_MA_LENGTH']
        variables['TEMA_PERIOD'] = config['TEMA_PERIOD']
        variables['EMA_PERIOD'] = config['EMA_PERIOD']
        variables['CANDLE_SIZE_FACTOR'] = config['CANDLE_SIZE_FACTOR']
        variables['SHORT_ALMA_LENGTH'] = config['SHORT_ALMA_LENGTH']
        variables['LONG_ALMA_LENGTH'] = config['LONG_ALMA_LENGTH']
        variables['FAST_OFFSET'] = config['FAST_OFFSET']
        variables['FAST_SIGMA'] = config['FAST_SIGMA']
        variables['TREND_OFFSET'] = config['TREND_OFFSET']
        variables['TREND_SIGMA'] = config['TREND_SIGMA']
        variables['SIGNAL_OFFSET'] = config['SIGNAL_OFFSET']
        variables['SIGNAL_SIGMA'] = config['SIGNAL_SIGMA']
    except Exception as err:
        print(err)


def save_to_file():
    config = {}
    variables = globals()
    config['SMMA_SLOW_LENGTH'] = variables['SMMA_SLOW_LENGTH']
    config['SMMA_FAST_LENGTH'] = variables['SMMA_FAST_LENGTH']
    config['SMMA_FASTEST_LENGTH'] = variables['SMMA_FASTEST_LENGTH']
    config['DONCHIAN_PERIOD'] = variables['DONCHIAN_PERIOD']
    config['VOLATILITY_PERIOD'] = variables['VOLATILITY_PERIOD']
    config['TDI_RSI'] = variables['TDI_RSI']
    config['BAND_LENGTH'] = variables['BAND_LENGTH']
    config['FAST_MA_ON_RSI'] = variables['FAST_MA_ON_RSI']
    config['SLOW_MA_ON_RSI'] = variables['SLOW_MA_ON_RSI']
    config['VOLUME_MA_LENGTH'] = variables['VOLUME_MA_LENGTH']
    config['TEMA_PERIOD'] = variables['TEMA_PERIOD']
    config['EMA_PERIOD'] = variables['EMA_PERIOD']
    config['CANDLE_SIZE_FACTOR'] = variables['CANDLE_SIZE_FACTOR']
    config['SHORT_ALMA_LENGTH'] = variables['SHORT_ALMA_LENGTH']
    config['LONG_ALMA_LENGTH'] = variables['LONG_ALMA_LENGTH']
    config['FAST_OFFSET'] = variables['FAST_OFFSET']
    config['FAST_SIGMA'] = variables['FAST_SIGMA']
    config['TREND_OFFSET'] = variables['TREND_OFFSET']
    config['TREND_SIGMA'] = variables['TREND_SIGMA']
    config['SIGNAL_OFFSET'] = variables['SIGNAL_OFFSET']
    config['SIGNAL_SIGMA'] = variables['SIGNAL_SIGMA']
    try:
        config_file = open("config.json", "w")
        json.dump(config, config_file)
        config_file.close()
    except Exception as err:
        print(err)


def randomize():
    variables = globals()
    variables['SMMA_SLOW_LENGTH'] = random.randint(280, 320)
    variables['SMMA_FAST_LENGTH'] = random.randint(80, 120)
    variables['SMMA_FASTEST_LENGTH'] = random.randint(30, 70)
    variables['DONCHIAN_PERIOD'] = random.randint(5, 20)
    variables['VOLATILITY_PERIOD'] = random.randint(80, 120)
    variables['TDI_RSI'] = random.randint(8, 13)
    variables['BAND_LENGTH'] = random.randint(25, 35)
    variables['FAST_MA_ON_RSI'] = random.randint(1, 5)
    variables['SLOW_MA_ON_RSI'] = random.randint(5, 10)
    variables['VOLUME_MA_LENGTH'] = random.randint(20, 60)
    variables['TEMA_PERIOD'] = random.randint(45, 65)
    variables['EMA_PERIOD'] = random.randint(50, 70)
    variables['CANDLE_SIZE_FACTOR'] = random.uniform(0.8, 1.5)
    variables['SHORT_ALMA_LENGTH'] = random.randint(3, 7)
    variables['LONG_ALMA_LENGTH'] = random.randint(18, 25)
    variables['FAST_OFFSET'] = random.uniform(0.25, 1)
    variables['FAST_SIGMA'] = random.randint(2, 6)
    variables['TREND_OFFSET'] = random.uniform(0.25, 1)
    variables['TREND_SIGMA'] = random.randint(2, 6)
    variables['SIGNAL_OFFSET'] = random.uniform(0.35, 1)
    variables['SIGNAL_SIGMA'] = random.randint(4, 8)


if __name__ == '__main__':
    set_from_file()
    save_to_file()
