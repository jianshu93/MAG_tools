import os, subprocess, sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import subprocess


def fastANI_heatmap(input_file_path, output_directory_path):

	input_file = input_file_path
	data = input_file
	df = pd.read_table(data, delimiter="\t", header=None, index_col=0, skiprows=1)

	print(df.columns)
	df.columns = list_of_file_paths
	df.index = list_of_file_paths
	print(df.columns)
	print (df.shape)
	mask = np.zeros_like(df, dtype=np.bool)
	mask[np.triu_indices_from(mask)] = True
	mask[np.diag_indices_from(mask)] = False

    # Set up the matplotlib figure
	f, ax = plt.subplots(figsize=(7, 6))
    # Generate a custom diverging colormap
	cmap = sns.diverging_palette(220, 10, as_cmap=True)
    # Draw the heatmap with the mask and correct aspect ratio
	##sns_plot = sns.heatmap(df, mask=mask, cmap=cmap, linewidths=.5, cbar_kws={"shrink": .5})
	sns_plot_with_cluster = sns.clustermap(df,cmap=cmap)
	##fig = sns_plot.get_figure()
	##fig.savefig("heatmap_all_new.pdf")
	plt.savefig('heatmap_with_Seaborn_clustermap_python.pdf',
            dpi=150, figsize=(7,6))

def main():
	inputpath = sys.argv[1] # input directory of files
	outputpath = sys.argv[2] # output directory path
	fastANI_visualization = fastANI_heatmap(inputpath,outputpath)

if __name__ == "__main__":
	main()