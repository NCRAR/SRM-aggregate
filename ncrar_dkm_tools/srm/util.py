'''
Utilities for aggregating SRM files for DKM lab
'''
import datetime as dt
import json
from pathlib import Path
import re

import pandas as pd


# Filename pattern expected of SRM files.
p_filename = re.compile(r'PCO(?P<subject>\d{3})_(?P<visit>\d{3})_\d{3}_(?P<condition>\w+)(?P<date>(_\d{2}){6})')


def parse_filename(filename):
    '''
    Parse subject, visit, condition and date out of filename

    Parameters
    ----------
    filename : {str, pathlib.Path}
        Filename to parse.

    Returns
    -------
    info : dict
        Dictionary with filename information as values. Date will be converted
        to a Python datetime object.
    '''
    filename = Path(filename)
    file_info = p_filename.match(filename.stem).groupdict()
    file_info['date'] = dt.datetime.strptime(file_info['date'], '_%y_%m_%d_%H_%M_%S')
    return file_info


def load_file(filename):
    '''
    Load header and data from file

    Parameters
    ----------
    filename : {str, pathlib.Path}
        Filename to parse.

    Returns
    -------
    header : dict
        Header information stored at top of file.
    data : pd.DataFrame
        Data in file.
    '''
    filename = Path(filename)
    with filename.open() as fh:
        header = json.loads(fh.readline())
        data = pd.read_csv(fh, sep='|', header=None, index_col=0)
    return header, data


def _aggregate_file(filename):
    file_info = parse_filename(filename)
    _, data = load_file(filename)
    n_re = len(re.findall('True', filename.read_text()))
    n_pd = data.loc[:, 5].sum()
    file_info['averaged_tmr'] = 10 - data.loc[:, 5].sum()
    return file_info


def aggregate(files):
    '''
    Aggregate all *.bgc files found in the list of files and folders

    Parameters
    ----------
    files : list of pathlib.Path
        Can be a mix of *.bcg files and directories. If a directory is found in
        the list, it will be recursively scanned for all *.bgc files. All *.bgc
        files found will be aggregated.

    Returns
    -------
    results : pandas.DataFrame
        DataFrame containing one row per file.
    results_mean : pandas.DataFrame
        DataFrame with TMR averaged across subject, visit and condition.
    errors : list
        List of errors when attempting to process *.bgc files
    '''
    bgc_files = []
    for filename in files:
        if filename.suffix == '.bgc':
            bgc_files.append(filename)
        else:
            bgc_files.extend(filename.glob('**/*.bgc'))
    bgc_files = set(bgc_files)

    results = []
    errors = []
    for bgc_file in bgc_files:
        try:
            results.append(_aggregate_file(bgc_file))
        except Exception as e:
            mesg = f'Error processing {bgc_file.stem}: {e}'
            errors.append(mesg)
    results = pd.DataFrame(results) \
        .sort_values(['subject', 'visit']) \
        .reset_index(drop=True)

    grouping = ['subject', 'visit', 'condition']
    results_mean = results.groupby(grouping)['averaged_tmr'] \
        .agg(['mean', 'size']) \
        .reset_index()
    return results, results_mean, errors
