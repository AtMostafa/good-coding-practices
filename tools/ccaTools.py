import params
import numpy as np
from matplotlib.ticker import MaxNLocator
import matplotlib as mpl
import pyaldata as pyal
from scipy.stats import wilcoxon
import pandas as pd
from sklearn.decomposition import PCA
import numpy as np
import pandas as pd
from scipy.linalg import qr, svd, inv
from scipy.interpolate import interp1d
import pyaldata as pyal
from sklearn.decomposition import PCA
from scipy.spatial import procrustes
import logging
import torch

from tools import dataTools as dt
from tools import utilityTools as utility
monkey_defs = params.monkey_defs

def get_ccs(side1df, side2df, epoch, area, n_components, use_procrustes = False): 
    #get data  
    AllData1 = dt.get_data_array(side1df, epoch, area=area, model=n_components)
    AllData2 = dt.get_data_array(side2df, epoch, area=area, model=n_components)
    _,_, min_trials, min_time,_ = np.min((AllData1.shape,AllData2.shape),axis=0)

    #get ccs
    ccs=[]
    for sessionData1,sessionData2 in zip(AllData1,AllData2):
        data1 = np.reshape(sessionData1[:,:min_trials,:min_time,:], (-1,n_components))
        data2 = np.reshape(sessionData2[:,:min_trials,:min_time,:], (-1,n_components))
        if use_procrustes:
            ccs.append(procrustes_wrapper(data1, data2))
        else:
            ccs.append(canoncorr(data1, data2))
    ccs = np.array(ccs).T 

    return ccs

def get_ccs_upper_bound(side1df, epoch, area, n_components, calc_percentile = True, use_procrustes = False):
    n_iter = params.n_iter * 10

    #get data
    AllData1 = dt.get_data_array(side1df, epoch, area=area, model=n_components)
    n_shared_trial1 = AllData1.shape[2]
    trialList1 = np.arange(n_shared_trial1)

    #get ccs
    CCsU=[]
    for sessionData in AllData1:
        r = []
        for n in range(n_iter):
            params.rng.shuffle(trialList1)
            # non-overlapping randomised trials
            trial1 = trialList1[:n_shared_trial1//2]
            trial2 = trialList1[-(n_shared_trial1//2):]
            data1 = np.reshape(sessionData[:,trial1,:,:], (-1,n_components))
            data2 = np.reshape(sessionData[:,trial2,:,:], (-1,n_components))
            if use_procrustes:
                r.append(procrustes_wrapper(data1, data2))
            else:
                r.append(canoncorr(data1, data2))
        CCsU.append(r)
    CCsU = np.array(CCsU)
    if calc_percentile:
        CCsU = np.percentile(CCsU, 99, axis=1).T

    return CCsU

def get_ccs_lower_bound_monkey(side1df, side2df, area, n_components, len_trial, calc_percentile = True, use_procrustes = False):
    n_iter = params.n_iter * 10

    #get data
    AllData1 = dt._get_data_array(side1df, epoch_L=len_trial, area=area, model=n_components)
    AllData1_ = dt._get_data_array(side2df, epoch_L=len_trial, area=area, model=n_components)
    _,_, min_trials, min_time,_ = np.min((AllData1.shape,AllData1_.shape),axis=0)

    #get ccs
    CCsL=[]
    for sessionData1,sessionData2 in zip(AllData1,AllData1_):
        r = []
        for n in range(n_iter):
            sessionData1_sh = params.rng.permutation(sessionData1,axis=0)
            sessionData2_sh = params.rng.permutation(sessionData2,axis=0)

            data1 = np.reshape(sessionData1_sh[:,:min_trials,:min_time,:], (-1,n_components))
            data2 = np.reshape(sessionData2_sh[:,:min_trials,:min_time,:], (-1,n_components))
            if use_procrustes:
                r.append(procrustes_wrapper(data1, data2))
            else:
                r.append(canoncorr(data1, data2))
        CCsL.append(r)
    CCsL = np.array(CCsL)
    if calc_percentile:
        CCsL = np.percentile(CCsL, 1, axis=1).T
    return CCsL

@utility.report
def plot_cca(ax, ax_hist, allDFs, epoch, area, n_components, dataset = 'monkey', prep=False, use_procrustes = False):

    #get data
    if dataset == 'monkey':
        animals = 'monkeys'
        defs = monkey_defs
        pairFileList = dt.get_paired_files_monkey(allDFs)
        n_animals = len(np.unique([df.monkey[0] for df in allDFs]))
    elif dataset == 'mouse':
        animals = 'mice'
        defs = mouse_defs
        pairFileList = dt.get_paired_files_mouse(allDFs)
        n_animals = len(np.unique([df.mouse[0] for df in allDFs]))
    else:
        raise ValueError('dataset must be monkey or mouse')

    pair_side1df = [allDFs[i] for i,_ in pairFileList]
    pair_side2df = [allDFs[j] for _,j in pairFileList]
    side1df = allDFs

    #get ccs
    if prep:
        len_trial = int(np.round(np.diff(defs.WINDOW_prep)/defs.BIN_SIZE))
    else:
        len_trial = int(np.round(np.diff(defs.WINDOW_exec)/defs.BIN_SIZE))
    allCCs = get_ccs(pair_side1df, pair_side2df, epoch, area, n_components, use_procrustes = use_procrustes)
    if dataset == 'monkey':
        CCsL = get_ccs_lower_bound_monkey(pair_side1df, pair_side2df, area, n_components, len_trial, use_procrustes = use_procrustes)
    else:
        CCsL = get_ccs_lower_bound_mice(pair_side1df, pair_side2df, area, n_components, len_trial, use_procrustes = use_procrustes)
    CCsU = get_ccs_upper_bound(side1df, epoch, area, n_components, use_procrustes=use_procrustes)

    # plotting
    x_ = np.arange(1,n_components+1)
    utility.shaded_errorbar(ax, x_, allCCs, color=params.colors.MainCC, marker = 'o')
    utility.shaded_errorbar(ax, x_, CCsU, color=params.colors.UpperCC, marker = '<', ls='--')
    utility.shaded_errorbar(ax, x_, CCsL, color=params.colors.LowerCC, marker = '>', ls=':')

    ax.set_ylim([-.05,1])
    ax.set_xlim([.6,n_components+.6])
    ax.set_xlabel('Neural mode')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    if use_procrustes:
        ax.set_ylabel('Procrustes correlation')
    else:
        ax.set_ylabel('Canonical correlation')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_bounds([1,n_components])
    ax.spines['left'].set_bounds([0,1])
    ax.text(x=n_components, y=1, s= f'$n={CCsL.shape[1]}$ pairs of sessions\nacross ${n_animals}$ ${animals}$', ha='right', va='top', fontsize=mpl.rcParams['xtick.labelsize'])
    
    #plot the hist
    bins = np.arange(0,1,0.05)
    ax_hist.xaxis.set_visible(False)
    ax_hist.set_facecolor('None')
    ax_hist.spines['bottom'].set_visible(False)
    ax_hist.spines['right'].set_visible(False)
    ax_hist.spines['top'].set_visible(False)
    ax_hist.spines['left'].set_bounds([0,1])
    ax_hist.set_ylim([-.05,1])
    ax_hist.hist(allCCs[:4,:].mean(axis=0), bins=bins, density=True, label=f'Across ($n={allCCs.shape[1]}$)', color=params.colors.MainCC, alpha=.8, orientation='horizontal')
    ax_hist.hist(CCsU[:4,:].mean(axis=0), bins=bins, density=True,label=f'Within ($n={CCsU.shape[1]}$)', color=params.colors.UpperCC, alpha=.8, orientation='horizontal')
    ax_hist.hist(CCsL[:4,:].mean(axis=0), bins=bins, density=True, label=f'Control ($n={CCsL.shape[1]}$)', color=params.colors.LowerCC, alpha=.8, orientation='horizontal')

    ax_hist.tick_params('y', direction='out')
    ax_hist.set_yticklabels([])
    ax_hist.legend(loc=(0,-.05))

def plot_cca_for_ex(ax, example_dfs, epoch, area, n_components, dataset = 'monkey', prep = False):

    if dataset == 'monkey':
        animals = 'monkeys'
        defs = monkey_defs
    else:
        raise ValueError('dataset must be monkey or mouse')
    
    #get data
    df1, df2 = example_dfs

    #get ccs
    if prep:
        len_trial = int(np.round(np.diff(defs.WINDOW_exec)/defs.BIN_SIZE))
    else:
        len_trial = int(np.round(np.diff(defs.WINDOW_prep)/defs.BIN_SIZE))
    allCCs = get_ccs(df1,df2, epoch, area, n_components)
    CCsL = get_ccs_lower_bound_monkey(df1,df2, area, n_components, len_trial)
    CCsU = get_ccs_upper_bound([df1,df2], epoch, area, n_components)

    # plotting
    x_ = np.arange(1,n_components+1)
    ax.plot(x_, allCCs, color=params.colors.MainCC, marker = 'o', label=f'Across ${animals}$')
    ax.plot(x_, CCsU[:,0], color=params.colors.UpperCC, marker = '<', ls='--', label=f'Within 1')
    ax.plot(x_, CCsU[:,1], marker = '<', ls='--', label=f'Within 2')
    ax.plot(x_, CCsL, color=params.colors.LowerCC, marker = '>', ls=':', label=f'Control')

    ax.set_ylim([-.05,1])
    ax.set_xlim([.6, n_components+.6])
    ax.set_xlabel('Neural mode')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    # ax.set_title(f'{defs.areas[2]} Alignment')
    ax.legend(loc=(.55,.67))
    ax.set_ylabel('Canonical correlation')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_bounds([1, n_components])
    ax.spines['left'].set_bounds([0,1])


def canoncorr(X:np.array, Y: np.array, fullReturn: bool = False) -> np.array:
    """
    Canonical Correlation Analysis (CCA)
    line-by-line port from Matlab implementation of `canoncorr`
    X,Y: (samples/observations) x (features) matrix, for both: X.shape[0] >> X.shape[1]
    fullReturn: whether all outputs should be returned or just `r` be returned (not in Matlab)
    
    returns: A,B,r,U,V 
    A,B: Canonical coefficients for X and Y
    U,V: Canonical scores for the variables X and Y
    r:   Canonical correlations
    
    Signature:
    A,B,r,U,V = canoncorr(X, Y)
    """
    n, p1 = X.shape
    p2 = Y.shape[1]
    if p1 >= n or p2 >= n:
        logging.warning('Not enough samples, might cause problems')

    # Center the variables
    X = X - np.mean(X,0)
    Y = Y - np.mean(Y,0)

    # Factor the inputs, and find a full rank set of columns if necessary
    Q1,T11,perm1 = qr(X, mode='economic', pivoting=True, check_finite=True)

    rankX = sum(np.abs(np.diagonal(T11)) > np.finfo(type((np.abs(T11[0,0])))).eps*max([n,p1]))

    if rankX == 0:
        logging.error(f'stats:canoncorr:BadData = X')
    elif rankX < p1:
        logging.warning('stats:canoncorr:NotFullRank = X')
        Q1 = Q1[:,:rankX]
        T11 = T11[:rankX,:rankX]

    Q2,T22,perm2 = qr(Y, mode='economic', pivoting=True, check_finite=True)
    rankY = sum(np.abs(np.diagonal(T22)) > np.finfo(type((np.abs(T22[0,0])))).eps*max([n,p2]))

    if rankY == 0:
        logging.error(f'stats:canoncorr:BadData = Y')
    elif rankY < p2:
        logging.warning('stats:canoncorr:NotFullRank = Y')
        Q2 = Q2[:,:rankY]
        T22 = T22[:rankY,:rankY]

    # Compute canonical coefficients and canonical correlations.  For rankX >
    # rankY, the economy-size version ignores the extra columns in L and rows
    # in D. For rankX < rankY, need to ignore extra columns in M and D
    # explicitly. Normalize A and B to give U and V unit variance.
    d = min(rankX,rankY)
    L,D,M = svd(Q1.T @ Q2, full_matrices=True, check_finite=True, lapack_driver='gesdd')
    M = M.T

    A = inv(T11) @ L[:,:d] * np.sqrt(n-1)
    B = inv(T22) @ M[:,:d] * np.sqrt(n-1)
    r = D[:d]
    # remove roundoff errs
    r[r>=1] = 1
    r[r<=0] = 0

    if not fullReturn:
        return r

    # Put coefficients back to their full size and their correct order
    A[perm1,:] = np.vstack((A, np.zeros((p1-rankX,d))))
    B[perm2,:] = np.vstack((B, np.zeros((p2-rankY,d))))
    
    # Compute the canonical variates
    U = X @ A
    V = Y @ B

    return A, B, r, U, V

def procrustes_wrapper(A: np.ndarray, B: np.ndarray, fullReturn=False):
    """Procrustes alignment wrapper based on `scipy.spatial.procrustes`.
    A, B: (samples/observations) x (features) matrix, for both: A.shape[0] >> A.shape[1]
    fullReturn: whether all outputs should be returned or just `CCs` be returned
    
    returns: U, V, CCs 
    U, V: transformed matrice from A, B
    CCs: Correlations between transfomed signals, equivalent to Canonical correlations
    """
    assert A.shape == B.shape

    U, V, _ = procrustes(A, B)
    CCs = np.array([np.corrcoef(U[:,j],V[:,j])[0,1] for j in range(A.shape[1])])

    if not fullReturn:
        return CCs
    return U, V, CCs

def get_target_id(trial):
    return int(np.round((trial.target_direction + np.pi) / (0.25*np.pi))) - 1


def VAF_pc_cc (X: np.ndarray, C: np.ndarray, A: np.ndarray) -> np.ndarray:
    """
    Calculate Variance Accounted For (VAF) for a double projection (as in from PCA --> to CCA) using the method in Gallego, NatComm, 2018
    
    Parameters
    ----------
    `X`: the data matrix, T x n with _T_ time points and _n_ neurons, and each neuron is **zero mean**.
    
    `C`: the first projection matrix, usually it is the `PCA_model.components_`, but in principle could be any projection matrix with orthogonal bases.
    
    `A` : is the CCA canonical axes, the output of the `canoncorr` function, in principle could be any projection matrix, not necessarily orthogonal.
    
    Returns
    -------
    `VAFs`: np.array with VAF for each axes of `C`, normalised between 0<VAF<1 for each axis, `sum(VAFs)` equals to total VAF.
    """
    # following the notation in Gallego 2018
    D = inv(A.T@A)@A.T@C
    E = C.T@A
    norm = lambda m:np.sum(m**2)
    
    VAFs=np.empty((C.shape[0],))
    for comp in range(1,C.shape[0]+1):
        VAF = norm(X - X @ E[:,:comp] @ D[:comp,:]) / norm(X)
        VAFs[comp-1] = 1-VAF

    VAFs = np.array([VAFs[0],*np.diff(VAFs)])
    return VAFs

def VAF_pyal(df1:pd.DataFrame, field1: str, epoch1,
               df2:pd.DataFrame, field2: str, epoch2,
               n_components:int =10) -> (np.ndarray, np.ndarray):
    """
    Measure VAF for each CCA axis, between 2 DataFrames, fields, time epochs.
    epoch1, epoch2: an instance of the `pyal.generate_epoch_fun` function.
    """
 
    df1 = pyal.restrict_to_interval(df1,epoch_fun=epoch1)
    rates_1 = np.concatenate(df1[field1].values, axis=0)
    rates_1_model = PCA(n_components=n_components, svd_solver='full').fit(rates_1)
    rates_1_C = rates_1_model.components_
    df1 = pyal.apply_dim_reduce_model(df1, rates_1_model, field1, '_pca');
    pca_1_data = np.concatenate(df1['_pca'].values, axis=0)

    
    df2 = pyal.restrict_to_interval(df2, epoch_fun=epoch2)
    rates_2 = np.concatenate(df2[field2].values, axis=0)
    rates_2_model = PCA(n_components=n_components, svd_solver='full').fit(rates_2)
    rates_2_C = rates_2_model.components_
    df2 = pyal.apply_dim_reduce_model(df2, rates_2_model, field2, '_pca');
    pca_2_data = np.concatenate(df2['_pca'].values, axis=0)
    
    
    # same number of timepoints in both matrices
    n_samples = min ([pca_1_data.shape[0], pca_2_data.shape[0]])
    pca_1_data = pca_1_data[:n_samples,:]
    pca_2_data = pca_2_data[:n_samples,:]

    A, B, *_ = canoncorr(pca_1_data, pca_2_data, fullReturn=True)
    VAFs1 = VAF_pc_cc(rates_1, rates_1_C, A)
    VAFs2 = VAF_pc_cc(rates_2, rates_2_C, B)
    
    return VAFs1, VAFs2

def VAF_pc_cc_pyal(df1:pd.DataFrame, field1: str, epoch1, target1: int,
                   df2:pd.DataFrame, field2: str, epoch2, target2: int,
                   n_components:int =10) -> (np.ndarray, np.ndarray):
    """
    Measure VAF for each CCA axis, between 2 DataFrames, fields, time epochs, and targets.
    epoch1, epoch2: an instance of the `pyal.generate_epoch_fun` function.
    """
    if "target_id" not in df1.columns:
        df1["target_id"] = df1.apply(get_target_id, axis=1)
    if "target_id" not in df2.columns:
        df2["target_id"] = df2.apply(get_target_id, axis=1)
 
    df1 = pyal.restrict_to_interval(df1,epoch_fun=epoch1)
    rates_1 = np.concatenate(df1[field1].values, axis=0)
    rates_1_model = PCA(n_components=n_components, svd_solver='full').fit(rates_1)
    rates_1_C = rates_1_model.components_
    df1 = pyal.apply_dim_reduce_model(df1, rates_1_model, field1, '_pca');

    
    df1 = pyal.select_trials(df1, df1.target_id==target1)
    pca_1_target = np.concatenate(df1['_pca'].values, axis=0)

    
    df2 = pyal.restrict_to_interval(df2, epoch_fun=epoch2)
    rates_2 = np.concatenate(df2[field2].values, axis=0)
    rates_2_model = PCA(n_components=n_components, svd_solver='full').fit(rates_2)
    rates_2_C = rates_2_model.components_
    df2 = pyal.apply_dim_reduce_model(df2, rates_2_model, field2, '_pca');
    
    df2 = pyal.select_trials(df2, df2.target_id==target2)
    pca_2_target = np.concatenate(df2['_pca'].values, axis=0)
    
    
    # same number of timepoints in both matrices
    n_samples = min ([pca_1_target.shape[0], pca_2_target.shape[0]])
    pca_1_target = pca_1_target[:n_samples,:]
    pca_2_target = pca_2_target[:n_samples,:]

    A, B, r, _, _ = canoncorr(pca_1_target, pca_2_target, fullReturn=True)
    VAFs1 = VAF_pc_cc(rates_1, rates_1_C, A)
    VAFs2 = VAF_pc_cc(rates_2, rates_2_C, B)
    
    return VAFs1, VAFs2, r

def VAF_pc_cc_pyal2(df1:pd.DataFrame, field1: str, epoch1, target1: int,
                    df2:pd.DataFrame, field2: str, epoch2, target2: int,
                    n_components:int =10, n_iter:int =20):
    """
    Identical to `VAF_pc_cc_pyal`, ...
    except that it  tries to correct for _very_ different number of units by...
    subsampling the larger population `n_iter` times and averaging over the results.
    """
    if "target_id" not in df1.columns:
        df1["target_id"] = df1.apply(get_target_id, axis=1)
    if "target_id" not in df2.columns:
        df2["target_id"] = df2.apply(get_target_id, axis=1)
 
    df1_ = pyal.restrict_to_interval(df1,epoch_fun=epoch1)
    rates_1 = np.concatenate(df1_[field1].values, axis=0)

    df2_ = pyal.restrict_to_interval(df2, epoch_fun=epoch2)
    rates_2 = np.concatenate(df2_[field2].values, axis=0)
    
    # PCA
    ## check for `n`
    n1 = rates_1.shape[1]
    n2 = rates_2.shape[1]
    n_s, n_l = min(n1, n2), max(n1, n2)
    
    if n1 >= n2:
        array1Bigger = True
    else:
        array1Bigger = False
    diffTooBig = (abs(n1-n2)/min(n1,n2) >= 2) or (abs(n1-n2) > 100)  # boolean

    rng = np.random.default_rng(12345)
    VAFs1, VAFs2, R = [], [], []
    if diffTooBig:
#         print(f'correcting for numbesr of units: {n1, n2}')
        for i in range(n_iter):
            idx = rng.choice(n_l, n_s)
            array_new = rates_1 if array1Bigger else rates_2
            array_new = array_new[:,idx]
            array_new_model = PCA(n_components=n_components, svd_solver='full').fit(array_new)
            
            if array1Bigger:
                PCA_model = PCA(n_components=n_components, svd_solver='full').fit(rates_2)
            else:
                PCA_model = PCA(n_components=n_components, svd_solver='full').fit(rates_1)

            rates_1_model = array_new_model if array1Bigger else PCA_model
            rates_1_C = rates_1_model.components_
            df1__ = pyal.select_trials(df1_, df1_.target_id==target1)
            rates_1_target = np.concatenate(df1__[field1].values, axis=0)
            pca_1_target = rates_1_model.transform(rates_1_target[:,idx]) if array1Bigger else rates_1_model.transform(rates_1_target)

            rates_2_model = PCA_model if array1Bigger else array_new_model
            rates_2_C = rates_2_model.components_
            df2__ = pyal.select_trials(df2_, df2_.target_id==target2)
            rates_2_target = np.concatenate(df2__[field2].values, axis=0)
            pca_2_target = rates_2_model.transform(rates_2_target) if array1Bigger else rates_2_model.transform(rates_2_target[:,idx])

            # same number of timepoints in both matrices
            n_samples = min ([pca_1_target.shape[0], pca_2_target.shape[0]])
            pca_1_target = pca_1_target[:n_samples,:]
            pca_2_target = pca_2_target[:n_samples,:]

            A, B, r, _, _ = canoncorr(pca_1_target, pca_2_target, fullReturn=True)
            V1 = VAF_pc_cc(array_new if array1Bigger else rates_1, rates_1_C, A)
            V2 = VAF_pc_cc(rates_2 if array1Bigger else array_new, rates_2_C, B)
            VAFs1.append(V1)
            VAFs2.append(V2)
            R.append(r)
            
        VAFs1 = np.mean(np.array(VAFs1), axis=0)
        VAFs2 = np.mean(np.array(VAFs2), axis=0)
        R = np.mean(np.array(R), axis=0)
    else:
        VAFs1,VAFs2,R = VAF_pc_cc_pyal(df1, field1, epoch1, target1,
                                       df2, field2, epoch2, target2, n_components)

    return VAFs1, VAFs2, R
