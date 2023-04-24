import pandas as pd
import os
import multiprocessing
from functools import partial

COMBINED_DATA_PATH = "D:\\University of Essex\\data science\\Assignment_final\\CE888-Nurses2\\processed_data2"
COMBINED_DATA_PATH_PARQUET = "processed_data_parquet"
SAVE_PATH = "D:\\University of Essex\\data science\\Assignment_final\\CE888-Nurses2\\output"

print("Reading data ...")

acc, eda, hr, temp = None, None, None, None

signals = ['acc', 'eda', 'hr', 'temp']
columns=['X', 'Y', 'Z', 'EDA', 'HR', 'TEMP', 'id', 'datetime']

def read_parallel(signal):
    df = pd.read_parquet(os.path.join(COMBINED_DATA_PATH_PARQUET, f"combined_{signal}.parquet"))
    print(signal)
    print(df.shape)
    print([signal, df])
    return [signal, df]



def merge_parallel(id, acc, eda, hr, temp):
    print(f"Processing {id} with file: {acc}")
    print(f"Processing {id} with file: {eda}")
    print(f"Processing {id} with file: {hr}")
    print(f"Processing {id} with file: {temp}")
    df = pd.DataFrame(columns=columns)
    if acc is not None:
        acc_id = acc[acc['id'] == id].drop(['id'], axis=1)
        df = acc_id
    if eda is not None:
        eda_id = eda[eda['id'] == id].drop(['id'], axis=1)
        if not df.empty:
            df = pd.merge(df, eda_id, on='datetime', how='outer')
        else:
            df = eda_id
    if hr is not None:
        hr_id = hr[hr['id'] == id].drop(['id'], axis=1)
        if not df.empty:
            df = pd.merge(df, hr_id, on='datetime', how='outer')
        else:
            df = hr_id
    if temp is not None:
        temp_id = temp[temp['id'] == id].drop(['id'], axis=1)
        if not df.empty:
            df = pd.merge(df, temp_id, on='datetime', how='outer')
        else:
            df = temp_id
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)
    df['id'] = id
    return df

if __name__ == '__main__':

    results = []
    print('reading..')
    for signal in signals:
        results.append(read_parallel(signal))

    
    # pool = multiprocessing.Pool(len(signals))
    # results = pool.map(read_parallel, signals)
    print(results)
    print('readinng completed...')
    # pool.close()
    # pool.join()
    for i in results:
        if i[0] == 'acc':
            acc = i[1]
        if i[0] == 'eda':
            eda = i[1]
        if i[0] == 'hr':
            hr = i[1]
        if i[0] == 'temp':
            temp = i[1]

    # Merge data
    print('Merging Data ...')
    ids = eda['id'].unique()
    # pool = multiprocessing.Pool(len(ids))
    # merge_partial = partial(merge_parallel, acc=acc, eda=eda, hr=hr, temp=temp)

    dfLists = []

    for id in ids:
        dfLists.append(merge_parallel(id, acc=acc, eda=eda, hr=hr, temp=temp))
    # results = pool.map(merge_partial, ids)
    # pool.close()
    # pool.join()

    new_df = pd.concat(dfLists, ignore_index=True)

    print("Saving data ...")
    new_df.to_csv(os.path.join(SAVE_PATH, "merged_data.csv"), index=False)

    print("Saving data in parquet....")
    new_df.to_parquet(os.path.join(SAVE_PATH, "merged_data_parquet.parquet"), index=False)