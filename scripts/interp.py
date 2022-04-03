from matplotlib import markers
import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate
import os, glob
from pathlib import Path

def interpolate(tac_dir, method = 'linear'):
    """ This function interpolates all the readings inside the tac_dir folder, which are supposed to be csv. Additionally, it creates another folder called upsampled_plots where it saves a comparisation of both plots, the original and the upsampled one. 

    Args:
        tac_dir (str): The dir where are all the csv, relative path to the script call.
        method (str, optional): The method to upsample the readings. Defaults to 'linear'.

    Returns:
        dict : A dictionary of all the upsampled DataFrames
    """
        
    tac_path = tac_dir
    fig, axes = plt.subplots(nrows=1, ncols=2)
    interpolations = {}
    os.chmod(tac_dir, 0o777)
    Path(tac_dir+'/upsampled_plots').mkdir(mode = 0o777, parents=True, exist_ok=True)

    # Open all files in the clean tac directory
    for filename in glob.glob(os.path.join(tac_path, '*.csv')):
        with open(os.path.join(os.getcwd(), filename), 'r') as tac:
            axes[0].cla()
            axes[1].cla()
            axes[0].set_title('30 minute plot')
            axes[1].set_title('1 second plot')
            
            df = pd.read_csv(tac)
            df.index = pd.to_datetime(df['timestamp'], unit='s')
            df = df.drop(columns=['timestamp'])
            dt = (df.index[-1] - df.index[0])
            print("number of hours between start and end", dt.total_seconds()/3600 +1 )
            print('Shape', df.shape)
            # print(df.head(5))
            
            ### Plotting original vs upsampled
            df.plot(ax=axes[0], marker = 'o', label = 'Original plot. 30 min freq')
            # Upsample the TAC readings to second invervals. 
            upsampled = df.resample('s')
            interp = upsampled.interpolate(method=method)
            interp.plot(ax=axes[1], marker='x', label = 'Upsampled plot. 1 seg freq')
            
            path = tac_dir+ '/upsampled_plots/'+str(filename[-19:-4])+'.png' # -19 to -4 is the filename, without the extension file (.csv)
            plt.savefig(path)
            
            # Store in the dict the df interpolated.
            interpolations[filename[-19:-13]] = interp
    
    return interpolations

        
interpolate('../data/clean_tac')
