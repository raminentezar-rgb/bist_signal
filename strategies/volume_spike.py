# strategies/volume_spike.py

import pandas as pd

def detect_volume_spike(df, multiplier=2):

    volume = df['Volume'].squeeze()

    avg_volume = volume.rolling(20).mean()

    spike = volume.iloc[-1] > avg_volume.iloc[-1] * multiplier

    return bool(spike) if spike else spike