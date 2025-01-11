import pathlib, pickle
import numpy as np
import pandas as pd
import pyaldata as pyal
from sklearn.decomposition import PCA
from typing import Callable
import params
import os
import numpy as np
import pyaldata as pyal
import pandas as pd
from sklearn.decomposition import PCA
import pickle
from collections import Counter
from tools import utilityTools as utility

monkey_defs = params.monkey_defs

rng = params.rng

def summary(df):
    "prints a summary of monkey task datasets"
    print(df.monkey[0], df.date[0], '  ')
    time_sig = pyal.get_time_varying_fields(df)
    print(f'time signals:{time_sig}  ')
    for sig in time_sig:
        print(f'{sig} units: {df[sig][0].shape[1]}  ') if 'spike' in sig else 0
    try:
        print(f'tasks in file: {np.unique(df.task)}, epochs: {np.unique(df.epoch)}  ')
    except:
        print(f'tasks in file: {np.unique(df.task)}  ')
    try:
        print(f'Baseline trials: {np.sum(df.epoch=="BL")}  ')
    except:
        pass
    
    print('\n---\n')

def load_pyal_data(path: pathlib.Path) -> pd.DataFrame:
    """
    Loads pyal_data files. If it's a *.mat file, it is loaded, gets pickled and returned.
    If the pickle already exists, the pickle gets loaded instead of the *.mat file.
    
    Parameters
    ----------
    `path`: path to a *.mat file (or a *.p file).
    
    Returns
    -------
    `out`: a pyaldata pd.DataFrame
    """
    def load_pickle(pickle_path):
        with pickle_path.open('rb') as f:
            out = pickle.load(f)
            assert isinstance(out, pd.DataFrame), f'wrong data in pickle {pickle_path}'
        return out

    if isinstance(path, str):
        path = pathlib.Path(path)
    
    assert path.is_file(), f'path is not to a file: {path}'
    
    if path.suffix == '.p':
        return load_pickle(path)
    elif path.suffix == '.mat':
        pickle_path = path.with_suffix('.p')
        if pickle_path.exists():
            return load_pickle(pickle_path)
        else:
            df = pyal.mat2dataframe(path, shift_idx_fields=True)
            with open(pickle_path, 'wb') as f:
                pickle.dump(df, f)
            return df
    else:
        raise NameError(f'wrong file suffix: {path}')



def get_data_array(data_list: list[pd.DataFrame], epoch: Callable =None , area: str ='M1', model: Callable =None, n_components:int = 10) -> np.ndarray:
    """
    Applies the `model` to the `data_list` and return a data matrix of the shape: sessions x targets x trials x time x modes
    with the minimum number of trials and timepoints shared across all the datasets/targets.
    
    Parameters
    ----------
    `data_list`: list of pd.dataFrame datasets from pyalData (could also be a single dataset)
    `epoch`: an epoch function of the type `pyal.generate_epoch_fun()`
    `area`: area, either: 'M1', or 'S1', or 'PMd', ...
    `model`: a model that implements `.fit()`, `.transform()` and `n_components`. By default: `PCA(10)`. If it's an integer: `PCA(integer)`.
    `n_components`: use `model`, this is for backward compatibility
    
    Returns
    -------
    `AllData`: np.ndarray

    Signature
    -------
    AllData = get_data_array(data_list, execution_epoch, area='M1', model=10)
    all_data = np.reshape(AllData, (-1,10))
    """
    if isinstance(data_list, pd.DataFrame):
        data_list = [data_list]
    if model is None:
        model = PCA(n_components=n_components, svd_solver='full')
    elif isinstance(model, int):
        model = PCA(n_components=model, svd_solver='full')
    
    field = f'{area}_rates'
    n_shared_trial = np.inf
    target_ids = np.unique(data_list[0].target_id)
    for df in data_list:
        for target in target_ids:
            df_ = pyal.select_trials(df, df.target_id== target)
            n_shared_trial = np.min((df_.shape[0], n_shared_trial))

    n_shared_trial = int(n_shared_trial)

    # finding the number of timepoints
    if epoch is not None:
        df_ = pyal.restrict_to_interval(data_list[0],epoch_fun=epoch)
    n_timepoints = int(df_[field][0].shape[0])

    # pre-allocating the data matrix
    AllData = np.empty((len(data_list), len(target_ids), n_shared_trial, n_timepoints, model.n_components))

    rng = np.random.default_rng(12345)
    for session, df in enumerate(data_list):
        df_ = pyal.restrict_to_interval(df, epoch_fun=epoch) if epoch is not None else df
        rates = np.concatenate(df_[field].values, axis=0)
        rates_model = model.fit(rates)
        df_ = pyal.apply_dim_reduce_model(df_, rates_model, field, '_pca');

        for targetIdx,target in enumerate(target_ids):
            df__ = pyal.select_trials(df_, df_.target_id==target)
            all_id = df__.trial_id.to_numpy()
            # to guarantee shuffled ids
            while ((all_id_sh := rng.permutation(all_id)) == all_id).all():
                continue
            all_id = all_id_sh
            # select the right number of trials to each target
            df__ = pyal.select_trials(df__, lambda trial: trial.trial_id in all_id[:n_shared_trial])
            for trial, trial_rates in enumerate(df__._pca):
                AllData[session,targetIdx,trial, :, :] = trial_rates

    return AllData

def add_history(data:np.ndarray, n_hist:int) -> np.ndarray:
    """
    Adds history to the columns of `data`, by stacking `n_hist` previous time bins

    Parameters
    ----------
    `data`: the data matrix, T x n with _T_ time points and _n_ neurons/components/features.
    
    `n_hist` : number of time rows to be added.
    
    Returns
    -------
    An array of _T_  x _(n x n_hist+1)_

    """
    out = np.hstack([np.roll(data, shift, axis=0) for shift in range(n_hist+1)])
    out[:n_hist,data.shape[1]:] = 0
    return out

def add_history_to_data_array(allData, n_hist):
    """
    applies `add_history` to each trial

    Parameters
    ----------
    `allData`: the data matrix coming from `dt.add_history`
    
    `n_hist` : number of time rows to be added.
    
    Returns
    -------
    Similar to the output of `dt.get_data_array`, with extra PC columns.
    """
    assert allData.ndim == 5, 'Wrong input size'
    newShape = list(allData.shape)
    newShape[-1] *= (n_hist+1)
    
    out = np.empty(newShape)
    for session,sessionData in enumerate(allData):
        for target,targetData in enumerate(sessionData):
            for trial,trialData in enumerate(targetData):
                out[session,target,trial,:,:] = add_history(trialData, n_hist)
    return out


def _get_data_array(data_list: list[pd.DataFrame], epoch_L: int =None , area: str ='M1', model=None) -> np.ndarray:
    "Similar to `get_data_array` only returns an epoch of length `epoch_L` randomly chosen along each trial"
    if isinstance(data_list, pd.DataFrame):
        data_list = [data_list]
    if isinstance(model, int):
        model = PCA(n_components=model, svd_solver='full')
    
    field = f'{area}_rates'
    n_shared_trial = np.inf
    target_ids = np.unique(data_list[0].target_id)
    for df in data_list:
        for target in target_ids:
            df_ = pyal.select_trials(df, df.target_id== target)
            n_shared_trial = np.min((df_.shape[0], n_shared_trial))

    n_shared_trial = int(n_shared_trial)

    # finding the number of timepoints
    n_timepoints = int(df_[field][0].shape[0])
    # n_timepoints = int(df_[field][0].shape[0])
    if epoch_L is None:
        epoch_L = n_timepoints
    else:
        assert epoch_L < n_timepoints, 'Epoch longer than data'
    
    # pre-allocating the data matrix
    AllData = np.zeros((len(data_list), len(target_ids), n_shared_trial, epoch_L, model.n_components))

    for session, df in enumerate(data_list):
        rates = np.concatenate(df[field].values, axis=0)
        rates_model = model.fit(rates)
        df_ = pyal.apply_dim_reduce_model(df, rates_model, field, '_pca');

        for targetIdx,target in enumerate(target_ids):
            df__ = pyal.select_trials(df_, df_.target_id==target)
            all_id = df__.trial_id.to_numpy()
            # to guarantee shuffled ids
            rng.shuffle(all_id)
            # select the right number of trials to each target
            df__ = pyal.select_trials(df__, lambda trial: trial.trial_id in all_id[:n_shared_trial])
            for trial, trial_rates in enumerate(df__._pca):
                time_idx = rng.integers(trial_rates.shape[0]-epoch_L)
                trial_data = trial_rates[time_idx:time_idx+epoch_L,:]
                AllData[session,targetIdx,trial, :, :] = trial_data

    return AllData

def get_data_array_and_pos(data_list: list[pd.DataFrame], epoch , area: str ='M1', n_components: int =10, normalize_pos = False) -> np.ndarray:
    """
    Applies PCA to the data and return a data matrix of the shape: sessions x targets x  trials x time x PCs
    with the minimum number of trials and timepoints shared across all the datasets/targets.
    
    Parameters
    ----------
    `data_list`: list of pd.dataFrame datasets from pyal-data
    `epoch`: an epoch function of the type `pyal.generate_epoch_fun`
    `area`: area, either: 'M1', or 'S1', or 'PMd'

    Returns
    -------
    `AllData`: np.array

    Signature
    -------
    AllData = get_data_array(data_list, execution_epoch, area='M1', n_components=10)
    all_data = np.reshape(AllData, (-1,10))
    """
    def normal_mov(df: pd.DataFrame, field:str ='hTrjB') -> pd.DataFrame:
        """
        normalises based on 99th percentile for the magnitude of the movement
        """
        df = df.copy()
        magnitude = np.percentile(np.abs(np.concatenate(df[field]).flatten()), 99)
        df[field] = [pos/magnitude for pos in df[field]]
        return df

    field = f'{area}_rates'
    n_shared_trial = np.inf
    target_ids = np.unique(data_list[0].target_id)
    n_targets = len(target_ids)
    for df in data_list:
        for target in range(n_targets):
            df_ = pyal.select_trials(df, df.target_id == target)
            n_shared_trial = np.min((df_.shape[0], n_shared_trial))

    n_shared_trial = int(n_shared_trial)

    # finding the number of timepoints
    df_ = pyal.restrict_to_interval(df_,epoch_fun=epoch)
    n_timepoints = int(df_[field][0].shape[0])
    n_outputs = df_.pos[0].shape[1]

    # pre-allocating the data matrix
    AllData = np.empty((len(data_list), n_targets, n_shared_trial, n_timepoints, n_components))
    AllVel  = np.empty((len(data_list), n_targets, n_shared_trial, n_timepoints, n_outputs))
    for session, df in enumerate(data_list):
        df_ = pyal.restrict_to_interval(df, epoch_fun=epoch)
        pos_mean = np.nanmean(pyal.concat_trials(df, 'pos'), axis=0)
        df_.pos = [pos - pos_mean for pos in df_.pos]
        if normalize_pos:
            df_ = normal_mov(df_,'pos')

        rates = np.concatenate(df_[field].values, axis=0)
        rates_model = PCA(n_components=n_components, svd_solver='full').fit(rates)
        df_ = pyal.apply_dim_reduce_model(df_, rates_model, field, '_pca')
        
        for target in range(n_targets):
            df__ = pyal.select_trials(df_, df_.target_id==target)
            all_id = df__.trial_id.to_numpy()
            rng.shuffle(all_id)
            # select the right number of trials to each target
            df__ = pyal.select_trials(df__, lambda trial: trial.trial_id in all_id[:n_shared_trial])
            for trial, (trial_rates,trial_vel) in enumerate(zip(df__._pca, df__.pos)):
                AllData[session,target,trial, :, :] = trial_rates
                AllVel[session,target,trial, :, :] = trial_vel

    return AllData, AllVel

def get_full_monkey_data(data_list):
    full_list_MCx = []
    for animal, sessionList in data_list[monkey_defs.areas[2]].items():
        if 'Mr' in animal:
            continue  # to remove MrT
        full_list_MCx.append((animal,sessionList))
    full_list_MCx = [(animal,session) for animal,sessions in full_list_MCx for session in set(sessions)]
    # load the DFs
    allDFs_MCx = []
    for animal, session in full_list_MCx:
        path = params.root/animal/session
        allDFs_MCx.append(monkey_defs.prep_general(load_pyal_data(path)))

    return full_list_MCx, allDFs_MCx

def get_example_monkey_data(epoch = None):
    raster_example = monkey_defs.raster_example
    raster_example_df = []
    for session in raster_example:
        path = params.root/session.split('_')[0]/session
        df = monkey_defs.prep_general(load_pyal_data(path))
        if epoch is not None:
            df = pyal.restrict_to_interval(df, epoch_fun=epoch)
        raster_example_df.append(df)
    return raster_example_df

## general
def get_paired_files_monkey(allDFs):
    pairFileList = []
    for I, df1 in enumerate(allDFs):
        for J, df2 in enumerate(allDFs):
            animal1 = df1.monkey[0]
            animal2 = df2.monkey[0]
            if J<=I or animal1 == animal2: continue  # to repetitions
            if 'Chewie' in animal1 and 'Chewie' in animal2: continue 
            pairFileList.append((I,J))
    return pairFileList
