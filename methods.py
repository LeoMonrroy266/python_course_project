"""
Module that contains handy functions
"""
import numpy as np
from saxs import ScatterData
from scipy import optimize
from sklearn.metrics import r2_score

def calc_diff(light, dark):
    """
    Function that calculates the
    difference scattering between two data sets

    Parameters
    ----------
    light : ScatterData
    dark : ScatterData

    Returns
    -------
    ScatterData object with difference data as intensity and
    same q-range as input.
    """
    diff_vector = light.i - dark.i
    error_vector = (light.error + dark.error)/2
    diff_scatter = ScatterData()
    diff_scatter.set_data(diff_vector, light.q, error_vector)
    return diff_scatter

def buffer_sub(data, buffer, q, factor=1):
    """
    Subtracts the buffer from a run and
    creates and ScatterData object from new vector

    Parameters
    ----------
    data : np.array
    buffer : np.array
    q: np.array
    factor : int

    Returns
    -------
    A ScatterData object that has the buffer subtracted intensities
    and specified q-range
    """

    buff_subbed_data = data - (buffer*factor)
    new_data = ScatterData()
    new_data.set_data(q, buff_subbed_data)
    return new_data

def chi_square(v1, v2, v1_error):
    """
    Chi² minimization used to find scaling factor
    between two scattering curves

    Parameters
    ----------
    v1 : np.array
    v2 : np.array
    v1_error : np.array

    Returns
    -------
    The optimal scaling factor when minimizing chi²
    """
    calc_factor = lambda x: np.nansum(((v1 - (v2 * x)) / v1_error) ** 2)
    minimum = optimize.fmin(func=calc_factor, x0=20, retall=True)
    return minimum

def interpolate(q_target, data):
    i = np.interp(q_target, data.q, data.i)
    interpolated_curve = ScatterData()
    interpolated_curve.set_data(i, q_target)
    return interpolated_curve

def SSE(v1, v2, initial_guess):
    """
    Calculates the scaling factor between
    two scattering curves using the SSE.

    Parameters
    ----------
    v1 : np.array
    v2 : np.array
    initial_guess : int

    Returns
    -------
    The scaling factor as well as the value of the SSE
    when the factor is applied.

    """
    calc_factor = lambda x: np.nansum((v1 - (v2 * x)) ** 2)
    answer = optimize.fmin(func=calc_factor, x0=initial_guess, full_output=True, disp=False)
    minimum = answer[0]
    fopt = answer[1]
    return minimum, fopt

def calc_r2(v1,fit):
    r2 = r2_score(v1, fit)
    return r2

