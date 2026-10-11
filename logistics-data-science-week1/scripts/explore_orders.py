"""Explore gross positive unit demand in the public UCI Online Retail II dataset."""
import argparse
import pandas as pd


def load_daily_units(path):
    df = pd.read_excel(path, sheet_name=0)
    required = {'Invoice', 'InvoiceDate', 'Quantity'}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f'Columns missing: {sorted(missing)}')
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
    df = df.dropna(subset=['InvoiceDate', 'Quantity'])
    df = df[~df['Invoice'].astype(str).str.upper().str.startswith('C')]
    df = df[df['Quantity'] > 0]
    daily = df.set_index('InvoiceDate')['Quantity'].resample('D').sum()
    return daily.astype(float)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Path to UCI Online Retail II Excel workbook')
    args = parser.parse_args()
    daily = load_daily_units(args.input)
    print('Daily positive units (not orders):')
    print(daily.describe().to_string())
    print('Weekday average units:')
    print(daily.groupby(daily.index.day_name()).mean().round(1).to_string())


if __name__ == '__main__':
    main()
