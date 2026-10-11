"""Time-ordered next-day unit demand forecasting demo (synthetic or UCI Excel)."""
import argparse
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from explore_orders import load_daily_units


def synthetic_daily_units():
    rng = np.random.default_rng(42)
    days = pd.date_range('2025-01-01', periods=260)
    weekly = np.where(days.dayofweek >= 5, 35, 0)
    trend = np.arange(len(days)) * 0.15
    values = np.maximum(0, np.round(160 + weekly + trend + rng.normal(0, 12, len(days))))
    return pd.Series(values, index=days, name='units')


def evaluate(daily):
    frame = daily.to_frame(name='units')
    frame['lag_1'] = frame['units'].shift(1)
    frame['lag_7'] = frame['units'].shift(7)
    frame['weekday'] = frame.index.dayofweek
    frame = frame.dropna()
    if len(frame) < 30:
        raise ValueError('Need at least 37 calendar days of demand for evaluation')
    split = int(len(frame) * .8)
    train, test = frame.iloc[:split], frame.iloc[split:]
    cols = ['lag_1', 'lag_7', 'weekday']
    model = RandomForestRegressor(n_estimators=200, random_state=42, min_samples_leaf=3)
    model.fit(train[cols], train['units'])
    predictions = model.predict(test[cols])
    model_mae = mean_absolute_error(test['units'], predictions)
    baseline_mae = mean_absolute_error(test['units'], test['lag_7'])
    print(f'Train days: {len(train)}; test days: {len(test)}')
    print(f'RandomForest MAE (daily positive units): {model_mae:.2f}')
    print(f'Seasonal naive MAE (lag 7): {baseline_mae:.2f}')
    print('Interpretation: lower MAE is better; no guaranteed improvement.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='Optional UCI Online Retail II .xlsx file')
    args = parser.parse_args()
    daily = load_daily_units(args.input) if args.input else synthetic_daily_units()
    print('Dataset:', 'UCI historical invoices' if args.input else 'SYNTHETIC demonstration')
    evaluate(daily)


if __name__ == '__main__':
    main()
