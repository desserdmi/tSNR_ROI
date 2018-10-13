# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from nipype.interfaces.utility import Function

def roi_mean(roi_file, data_file, roi_labels=None, out_file="mean_tsnr.tsv"):
    """
    Calculate Mean of datafile for given ROI.
    
    Parameters
    ---------
    roi_file: str
        Filename of Atlas/Roi_File (nifti)
    data_file: str
        Filename of data to calculate mean
    roi_labesl: list of int
        Select label of roi_file (default: 1)

    out_file: str
        Filename to write tsv-formatted output to        

    Return
    ------
    float: mean of roi
    float: std of roi
    """    
    import pdb
    import numpy as np
    import nibabel as nib
    from os.path import abspath
    from nilearn import datasets
    dataset_cort = datasets.fetch_atlas_harvard_oxford('cort-maxprob-thr25-2mm')
    
    print("Calculationg Means")
    print(data_file)
    print(roi_file)
    data = nib.load(data_file).get_data()
    roi = nib.load(roi_file).get_data()
    
    if (data.shape != roi.shape):
        raise ValueError("Image-shapes do not match")

    if roi_labels is None:
        roi_labels = np.unique(roi)
    
    mean_vals = []
    for roi_label in roi_labels: 
        mean_vals.append([roi_label, np.mean(data[roi==roi_label]), np.std(data[roi==roi_label])])
    
    print(mean_vals)
    
    
    fname = abspath(out_file)
    np.savetxt(fname,mean_vals, delimiter='\t')
    
    
    return  fname
    

roi_mean_interface = Function(function=roi_mean, input_names=["roi_file", "data_file","roi_label", "output_filename"], output_names=["out_file"])