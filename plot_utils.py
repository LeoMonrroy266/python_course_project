import numpy as np
from saxs import ScatterData
import os
import matplotlib.pyplot as plt
from methods import *

def get_rg_diff(indices_light, indices_dark, rg):
    """
    Calculate the difference in radius of gyration between
    two models.

    Parameters
    ----------
    indices_light : np.array
    indices_dark : np.array
    rg : np.array

    Returns
    -------
    np.array with difference of radius in gyration
    between all model pairs.
    """
    rg_diff = [rg[m1] - rg[m2] for m1, m2 in zip(indices_light, indices_dark)]
    return rg_diff

def plotter(indices, model1, model2, scales, AF2_data, ax, q_min, q_max):
    """
    Plots the difference intensities between a set of intensities
    Parameters
    ----------
    indices : np.array
    Set of indices for the data
    same indices most correspond to the same data set in each input

    model1 : np.array
    Array with ScatterData objects

    model2 : np.array
    Array with ScatterData objects

    scales : np.array
    Array with scaling factor corresponding to each difference curve

    ax :  matplotlib.axes.Axes
    Axes object where the plots will be shown
    Returns
    -------

    """
    for i in indices:
        indices_light = model1[i]
        indices_dark = model2[i]
        light = AF2_data[indices_light]
        dark = AF2_data[indices_dark]
        diff = calc_diff(light, dark)
        diff = diff.scale_q(10)
        diff = diff.cut_q(q_min, q_max)

        scale = scales[i]

        if i == indices[-1]:
            ax.plot(diff.q, diff.i/1e5*scale/diff.q, linewidth=0.5, color='Blue', label='Theoretical')
        else:
            ax.plot(diff.q, diff.i/1e5*scale/diff.q, linewidth=0.5, color='Blue')


def plot_r2(data, save_path, save=False):
    """
    Plots a histogram showing the R² distribution for a set of difference curves,
    with possibility of saving the plot.

    Parameters
    ----------
    data : np.array
    Array with R² values for each difference curve

    save_path : str
    Path were the plot will be saved

    save : bool
    Indicates if plot should be saved or not
    default is False

    Returns
    -------

    """

    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_title('R² distribution', fontsize=16)
    ax.set_xlabel('R²', fontsize=13)
    ax.set_ylabel('Number of model pairs', fontsize=13)
    plt.hist(data, bins=50)
    if save:
        plt.savefig(f'{save_path}/histogram_R2.png', bbox_inches='tight', facecolor=(1, 1, 1))

def plot_activation_factor(data,save_path, save=False):
    """
    Plots a histogram showing the distribution of the activation factor for a set of difference curves,
    with possibility of saving the plot.

    Parameters
    ----------
    data : np.array
    Array with activation factor for each difference curve

    save_path : str
    Path were the plot will be saved

    save : bool
    Indicates if plot should be saved or not
    default is False

    Returns
    -------

    """
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_title('Activation ratio distribution', fontsize=16)
    ax.set_xlabel('Activation ratio', fontsize=13)
    ax.set_ylabel('Number of model pairs', fontsize=13)
    plt.hist(abs(data), bins=50)
    if save:
        plt.savefig(f'{save_path}/histogram_activation_factor.png', bbox_inches='tight', facecolor=(1, 1, 1))

def plot_r2_activation(r2, activation, save_path, save=False, best=False):
    """
    Plots a scatter plot of R² against the activation factor for set of data,
    with possibility of saving the plot.

    Parameters
    ----------
    r2 : np.array
    Array with R² value for each difference curve against the exp. data

    activation : np.array
    Array with activation factor for each difference curve

    save_path : str
    save : bool

    Returns
    -------
    """
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    if best:
        ax.scatter(r2[abs(activation)<1,], abs(activation[abs(activation)<1,]))
    else:
        ax.scatter(r2, abs(activation))
    ax.set_title(f'R² Vs. Yield', fontsize=15)
    ax.set_ylabel(f'Yield', fontsize=15)
    ax.set_xlabel('R²', fontsize=15)
    if save:
        plt.savefig(f'{save_path}/scatter_r2_activation.png', bbox_inches='tight', facecolor=(1, 1, 1))

def plot_rg_diff_activation(rg_diff, activation, save_path, save=False):
    """

    Parameters
    ----------
    rg_diff : np.array
    Array with difference in rg for each pair of curves

    activation : np.array
    Array with activation factor for each difference curve

    save_path :str

    save : bool

    Returns
    -------
    """
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_title(r'$\Delta$Rg Vs. Activation ratio')
    ax.set_ylabel('Activation ratio')
    ax.set_xlabel(r'$\Delta$Rg')
    ax.scatter(rg_diff, abs(activation))
    if save:
        plt.savefig(f'{save_path}/scatter_rg_activation.png', bbox_inches='tight', facecolor=(1, 1, 1))

def plot_rg_diff_r2(rg_diff, r2, save_path, save=False):
    """

    Parameters
    ----------
    rg_diff : np.array
    Array with difference in rg for each pair of curves

    r2 : np.array
    Array with R² value for each difference curve

    save_path :str

    save : bool

    Returns
    -------
    """
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_title(r'$\Delta$Rg Vs. R²')
    ax.set_ylabel('R²')
    ax.set_xlabel(r'$\Delta$Rg')
    ax.scatter(rg_diff, r2)
    if save:
        plt.savefig(f'{save_path}/scatter_rg_r2.png', bbox_inches='tight', facecolor=(1, 1, 1))