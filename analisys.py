import matplotlib.pyplot as plt
import pandas as pd
import os

DATA_PATH='./data'
OUTPUT_PATH_BASE = './img'

OUTPUT_PATH_Z= OUTPUT_PATH_BASE + '/z_plot'
OUTPUT_PATH_H= OUTPUT_PATH_BASE + '/hdiff'
OUTPUT_PATH_W= OUTPUT_PATH_BASE + '/wdiff'

COLUMNS=['dMain','Z in mm','Z in M','alarm flag','Hdiff','Wdiff']

directory = os.fsencode(DATA_PATH)
    
for file in os.listdir(directory):
    filename = os.fsdecode(os.path.join(directory,file))
    df = pd.read_csv(filename,names=COLUMNS,sep=',')

    out_dir= os.fsencode(OUTPUT_PATH_Z)
    outputname = os.fsdecode(os.path.join(out_dir,file))
    df['Z in mm'].plot()
    plt.savefig(outputname+ 'z_plot.png')
    plt.clf()

    out_dir= os.fsencode(OUTPUT_PATH_W)
    outputname = os.fsdecode(os.path.join(out_dir,file))
    df[df['Wdiff'] != -100]['Wdiff'].plot()
    plt.savefig(outputname+ 'W_diff.png')
    plt.clf()

    out_dir= os.fsencode(OUTPUT_PATH_H)
    outputname = os.fsdecode(os.path.join(out_dir,file))
    df[df['Hdiff']!= -100]['Hdiff'].plot()
    plt.savefig(outputname+ 'H_diff.png')
    plt.clf()


