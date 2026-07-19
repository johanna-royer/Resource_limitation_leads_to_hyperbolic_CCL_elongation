
def hyperbolic_function(S, l, S_G, L_mu):
    """
    Returns the function output of a hyperbolic growth function

    Parameters
    ----------
    S : numpy.ndarray 
        Values for which the output or function value of a hyperbolic function should be calculated (argument of function)

    l, S_G, L_mu: float
        We use optimal parameters determined with the help of scipy.optimize.curve_fit

    Returns
    -------
    output: numpy.ndarray
        Function output of a hyperbolic growth function with the given parameters
    """
    
    return(l/(S_G-S)) + L_mu

def linear_function(S, k, d):
    """
    Returns the function output of a linear growth function
    Parameters
    ----------
    S : numpy.ndarray 
        Values for which the output or function value of a hyperbolic function should be calculated (argument of function)

    k, d: float
        Slope (k) and intercept (d) of the linear function 

    Returns
    -------
    output: numpy.ndarray
        Function output of a linear function with the given parameters
    """
    return k*S + d
