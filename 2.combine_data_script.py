# Script to combine all signals into one

import os
import pandas as pd
from random import randint

DATA_PATH = "D:\\University of Essex\\data science\\Assignment_final\\CE888-Nurses2\\data\\Stress_dataset"
SAVE_PATH = "D:\\University of Essex\\data science\\Assignment_final\\CE888-Nurses2\\processed_data2"
#os.mkdir(SAVE_PATH)

final_columns = {
    'ACC': ['id', 'X', 'Y', 'Z', 'datetime'],
    'EDA': ['id', 'EDA', 'datetime'],
    'HR': ['id', 'HR', 'datetime'],
    'TEMP': ['id', 'TEMP', 'datetime'],
}

names = {
    'ACC.csv': ['X', 'Y', 'Z'],
    'EDA.csv': ['EDA'],
    'HR.csv': ['HR'],
    'TEMP.csv': ['TEMP'],
}

desired_signals = ['ACC.csv', 'EDA.csv', 'HR.csv', 'TEMP.csv']

acc = pd.DataFrame(columns=final_columns['ACC'])
eda = pd.DataFrame(columns=final_columns['EDA'])
hr = pd.DataFrame(columns=final_columns['HR'])
temp = pd.DataFrame(columns=final_columns['TEMP'])


def generate_random_number(length):
    return int(''.join([str(randint(0,10)) for _ in range(length)]))

def process_df(df, sub_file,file):
    start_timestamp = df.iloc[0,0]
    sample_rate = df.iloc[1,0]
    new_df = pd.DataFrame(df.iloc[2:].values, columns=df.columns)
    new_df['id'] = file[-2:]
    new_df['datetime'] = [(start_timestamp + i/sample_rate) for i in range(len(new_df))]
    return new_df

for file in os.listdir(DATA_PATH):
    print(f'Processing {file}')
    for sub_file in os.listdir(os.path.join(DATA_PATH, file)):
        if not sub_file.endswith(".zip"):
            for signal in os.listdir(os.path.join(DATA_PATH, file, sub_file)):
                if signal in desired_signals:
                    df = pd.read_csv(os.path.join(DATA_PATH, file, sub_file, signal), names=names[signal], header=None)
                    if not df.empty:
                        if signal == 'ACC.csv':
                            acc = pd.concat([acc, process_df(df, sub_file,file)])             
                        if signal == 'EDA.csv':
                            eda = pd.concat([eda, process_df(df, sub_file,file)])
                        if signal == 'HR.csv':
                            hr = pd.concat([hr, process_df(df, sub_file,file)])
                        if signal == 'TEMP.csv':
                            temp = pd.concat([temp, process_df(df, sub_file,file)])

print('Saving Data in csv....')
acc.to_csv(os.path.join(SAVE_PATH, 'combined_acc.csv'), index=False)
eda.to_csv(os.path.join(SAVE_PATH, 'combined_eda.csv'), index=False)
hr.to_csv(os.path.join(SAVE_PATH, 'combined_hr.csv'), index=False)
temp.to_csv(os.path.join(SAVE_PATH, 'combined_temp.csv'), index=False)


def saveInParquet():
    os.mkdir(PARQUET_FILE_STORAGE)

    print('Saving data in parquet....')

    acc.to_parquet(os.path.join(PARQUET_FILE_STORAGE, 'combined_acc.parquet'), index=False)
    eda.to_parquet(os.path.join(PARQUET_FILE_STORAGE, 'combined_eda.parquet'), index=False)
    hr.to_parquet(os.path.join(PARQUET_FILE_STORAGE, 'combined_hr.parquet'), index=False)
    temp.to_parquet(os.path.join(PARQUET_FILE_STORAGE, 'combined_temp.parquet'), index=False)

if __name__ == '__main__':
    PARQUET_FILE_STORAGE = 'processed_data_parquet'
    saveInParquet()