"""
cleaning.py - Traffic Violations Insight System
"""
import pandas as pd
import numpy as np


def load_data(filepath):
    print("⏳ Loading data...")
    df = pd.read_csv(filepath, low_memory=False)
    print(f"✅ Loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df


def clean_datetime(df):
    print("📅 Cleaning date and time...")

    df['Date Of Stop'] = pd.to_datetime(
        df['Date Of Stop'], infer_datetime_format=True, errors='coerce'
    )
    df['Time Of Stop'] = (
        df['Time Of Stop'].astype(str).str.strip()
        .str.replace(r'\.', ':', regex=True)
    )
    df['Hour']      = pd.to_datetime(df['Time Of Stop'],
                        format='%H:%M:%S', errors='coerce').dt.hour
    df['Month']     = df['Date Of Stop'].dt.month
    df['DayOfWeek'] = df['Date Of Stop'].dt.day_name()
    df['Year_Stop'] = df['Date Of Stop'].dt.year

    def time_bucket(hour):
        if pd.isna(hour):    return 'Unknown'
        if 5  <= hour < 12:  return 'Morning'
        if 12 <= hour < 17:  return 'Afternoon'
        if 17 <= hour < 21:  return 'Evening'
        return 'Night'

    df['TimeOfDay'] = df['Hour'].apply(time_bucket)
    print("✅ Date and time cleaned.")
    return df


def clean_boolean_columns(df):
    print("⚠️  Cleaning boolean columns...")

    bool_cols = [
        'Accident', 'Belts', 'Personal Injury', 'Property Damage',
        'Fatal', 'Commercial License', 'HAZMAT', 'Commercial Vehicle',
        'Alcohol', 'Work Zone', 'Search Conducted', 'Contributed To Accident'
    ]
    yes_values = {'yes', 'y', 'true', '1'}

    for col in bool_cols:
        if col in df.columns:
            df[col] = (
                df[col].astype(str).str.strip().str.lower()
                .map(lambda x: True if x in yes_values else False)
            )
    print("✅ Boolean columns cleaned.")
    return df


def clean_coordinates(df):
    print("🌎 Cleaning coordinates...")

    df['Latitude']  = pd.to_numeric(df['Latitude'],  errors='coerce')
    df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')

    df.loc[df['Latitude']  == 0, 'Latitude']  = np.nan
    df.loc[df['Longitude'] == 0, 'Longitude'] = np.nan
    df.loc[~df['Latitude'].between(24, 50),     'Latitude']  = np.nan
    df.loc[~df['Longitude'].between(-125, -65), 'Longitude'] = np.nan

    print("✅ Coordinates cleaned.")
    return df


def clean_categoricals(df):
    print("🏷️  Cleaning categorical columns...")

    # Gender
    df['Gender'] = df['Gender'].astype(str).str.strip().str.upper()
    df['Gender'] = df['Gender'].replace({'U':'Unknown','NAN':'Unknown','':'Unknown'})
    df.loc[~df['Gender'].isin(['M','F','Unknown']), 'Gender'] = 'Unknown'

    # Race
    df['Race'] = df['Race'].astype(str).str.strip().str.upper()
    df['Race'] = df['Race'].replace({'NAN':'Unknown','':'Unknown'})

    # State columns — exact names from your CSV
    for col in ['State', 'Driver State', 'DL State']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.upper()
            df.loc[df[col] == 'XX', col] = 'Unknown'

    # Agency
    df['Agency'] = df['Agency'].astype(str).str.strip().str.upper()

    # Violation Type
    df['Violation Type'] = (
        df['Violation Type'].astype(str).str.strip().str.title()
    )

    # Search columns
    for col in ['Search Disposition', 'Search Outcome',
                'Search Reason', 'Search Type', 'Search Arrest Reason',
                'Search Reason For Stop']:
        if col in df.columns:
            df[col] = (
                df[col].astype(str).str.strip()
                .replace({'nan':'Not Applicable',
                          'NaN':'Not Applicable',
                          '':   'Not Applicable'})
            )

    print("✅ Categorical columns cleaned.")
    return df


def clean_vehicle_columns(df):
    print("🚗 Cleaning vehicle columns...")

    make_map = {
        'CHEV':'CHEVROLET','CHEVY':'CHEVROLET','TOYT':'TOYOTA',
        'TOYOT':'TOYOTA',  'HOND':'HONDA',     'NISS':'NISSAN',
        'HYUN':'HYUNDAI',  'DODG':'DODGE',     'VOLK':'VOLKSWAGEN',
        'MERZ':'MERCEDES', 'LEXS':'LEXUS',     'INFI':'INFINITI',
        'ACUR':'ACURA',    'SUBA':'SUBARU',    'MAZD':'MAZDA',
        'MITS':'MITSUBISHI','BUIC':'BUICK',    'CADI':'CADILLAC',
        'LINC':'LINCOLN',  'PONT':'PONTIAC',   'OLDS':'OLDSMOBILE',
        'VOLV':'VOLVO',    'PORS':'PORSCHE',
    }
    color_map = {
        'BLK':'BLACK','WHI':'WHITE','WHT':'WHITE','BLU':'BLUE',
        'GRY':'GRAY', 'GRA':'GRAY','SIL':'SILVER','GRN':'GREEN',
        'YEL':'YELLOW','ORG':'ORANGE','GLD':'GOLD','PNK':'PINK',
        'PRP':'PURPLE','MAR':'MAROON','BGE':'BEIGE',
        'BRO':'BROWN','BRN':'BROWN',
    }

    df['Make']  = df['Make'].astype(str).str.strip().str.upper().replace(make_map)
    df['Color'] = df['Color'].astype(str).str.strip().str.upper().replace(color_map)
    df['Model'] = df['Model'].astype(str).str.strip().str.upper()
    df['Year']  = pd.to_numeric(df['Year'], errors='coerce')
    df.loc[~df['Year'].between(1960, 2025), 'Year'] = np.nan

    print("✅ Vehicle columns cleaned.")
    return df


def engineer_features(df):
    print("⚙️  Engineering features...")

    def categorize(desc):
        desc = str(desc).lower()
        if 'speed'     in desc: return 'Speeding'
        if 'license'   in desc: return 'License'
        if 'registr'   in desc: return 'Registration'
        if 'alcohol'   in desc or 'dui' in desc: return 'DUI/Alcohol'
        if 'belt'      in desc: return 'Seatbelt'
        if 'stop sign' in desc or 'red light' in desc: return 'Traffic Signal'
        if 'insurance' in desc: return 'Insurance'
        if 'equipment' in desc: return 'Equipment'
        return 'Other'

    df['ViolationCategory'] = df['Description'].apply(categorize)

    sev_cols = [c for c in
                ['Accident','Personal Injury','Property Damage','Fatal']
                if c in df.columns]
    df['SeverityScore'] = sum(df[c].astype(int) for c in sev_cols)

    print("✅ Features engineered.")
    return df


def clean_all(filepath, save_path):
    """Master pipeline — cleans and saves the dataset."""
    df = load_data(filepath)
    df = clean_datetime(df)
    df = clean_boolean_columns(df)
    df = clean_coordinates(df)
    df = clean_categoricals(df)
    df = clean_vehicle_columns(df)
    df = engineer_features(df)

    df.to_csv(save_path, index=False)
    print(f"\n🎉 Done! Saved → {save_path}")
    print(f"   Final shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df