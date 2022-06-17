import os
import pandas as pd

swiss = pd.read_csv('/app/intfold/uniprot-filtered-reviewed_yes.tab.gz', sep='\t')
ec_swiss = swiss[swiss['EC number'].notnull()]

for i in range(ec_swiss.shape[0]):
    amino = ec_swiss.iloc[i]
    entry = amino['Entry']
    seq = amino['Sequence']
    ec = amino['EC number']
    os.system('python intfold.py --seq {} --entry {} --ec {}'.format(seq, entry, ec))