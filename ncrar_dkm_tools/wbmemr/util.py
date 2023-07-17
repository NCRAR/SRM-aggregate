'''
Utilities for aggregating SRM files for DKM lab
'''
from pathlib import Path

import pandas as pd


def aggregate(files, columns_of_interest, output_file):
    '''
    Aggregate all subject xlsx files found in the list of files and folders

    Parameters
    ----------
    files : list of pathlib.Path
        Can be a mix of *.xlsx files and directories. If a directory is found in
        the list, it will be recursively scanned for all *.bgc files. All *.bgc
        files found will be aggregated.

    Returns
    -------
    results : pandas.DataFrame
        DataFrame containing one row per file.
    '''
    xlsx_files = []
    for filename in files:
        filename = Path(filename)
        if filename.suffix == '.xlsx':
            xlsx_files.append(filename)
        else:
            xlsx_files.extend(filename.glob('**/*.xlsx'))
    xlsx_files = set(xlsx_files)

    cols = ['Variable Name', 'Sheet']
    voi = pd.read_excel(columns_of_interest, sheet_name=0)[cols]

    voi_all = voi.query('Sheet == "Each Sheet"')['Variable Name'].values.tolist()
    voi = voi.query('Sheet != "Each Sheet"')

    results = {}
    for xlsx_file in xlsx_files:
        for sheet, sheet_voi in voi.groupby('Sheet'):
            sheet_name = sheet.split(' ')[0]
            df = pd.read_excel(xlsx_file, sheet_name=sheet_name)
            cols = voi_all + sheet_voi['Variable Name'].values.tolist()
            results.setdefault(sheet, []).append(df[cols])

    merged_results = {}
    with pd.ExcelWriter(output_file) as fh:
        for sheet, rows in results.items():
            merged = pd.concat(rows).set_index(voi_all).T
            merged.to_excel(fh, sheet_name=sheet)


if __name__ == '__main__':
    aggregate([
            r'C:\Users\bburan\projects\consulting\NCRAR\ncrar-dkm-tools\data\wbmemr\300.xlsx',
            r'C:\Users\bburan\projects\consulting\NCRAR\ncrar-dkm-tools\data\wbmemr\301.xlsx',
        ],
        r'C:\Users\bburan\projects\consulting\NCRAR\ncrar-dkm-tools\data\wbmemr\WB Variables of interest.xlsx',
        r'C:\Users\bburan\projects\consulting\NCRAR\ncrar-dkm-tools\data\wbmemr\example_output.xlsx',
    )
