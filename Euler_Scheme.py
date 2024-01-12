# In this section we define the different Euler discretization Schemes
# we are using for the different examples


import numpy as np


# Euler scheme for simulating SDEs over a fixed time grid.
def Euler_Scheme(X0, funcMu, Sigma0, T, mSteps):
    #time step size
    dt = T / mSteps
    X = np.zeros(mSteps+1)

    # the Euler scheme at X0
    X[0] = X0
    # Get the grid (t0,...,tm=T) with steps dt
    time_grid = np.linspace(0, T, mSteps + 1)

    # Euler scheme loop
    for i in range(mSteps):
        # Euler scheme formula
        X[i+1] = X[i] + funcMu(time_grid[i], X[i])*dt + Sigma0 * np.random.normal(loc=0.0, scale=np.sqrt(dt))

    return X


# Euler scheme for simulating SDEs over a fixed time grid.
def Euler_Scheme_PathDep(X0, funcMu, Sigma0, T, mSteps, lTimeIntervals): #mSteps for each subinterval
    lX = [X0]
    for k in range(1,len(lTimeIntervals)):
        #time step size
        tk = lTimeIntervals[k]
        t_kminus1 = lTimeIntervals[k-1]
        dt = (tk - t_kminus1) / mSteps
        X_tk_tkminus1 = np.zeros(mSteps+1)

        # the Euler scheme at X0
        X_tk_tkminus1[0] = lX[-1]
        # Get the grid (t0,...,tm=T) with steps dt
        time_grid = np.linspace(t_kminus1, tk, mSteps + 1)

        # Euler scheme loop
        for i in range(mSteps):
            # Euler scheme formula
            X_tk_tkminus1[i+1] = X_tk_tkminus1[i] + funcMu(time_grid[i], X[i])*dt + Sigma0 * np.random.normal(loc=0.0, scale=np.sqrt(dt))

        lX.append(X_tk_tkminus1[-1])

    return lX

def Euler_Scheme_Pathdep2(X0, funcMu, Sigma0, T, mSteps):
    #time step size
    dt = T / mSteps
    X = np.zeros(mSteps+1)
    L=[]
    # the Euler scheme at X0
    X[0] = X0
    # Get the grid (t0,...,tm=T) with steps dt
    time_grid = np.linspace(0, T, mSteps + 1)
    # Euler scheme loop
    for i in range(mSteps):
        # Euler scheme formula
        X[i+1] = X[i] + funcMu(time_grid[i], X[i])*dt + Sigma0 * np.random.normal(loc=0.0, scale=np.sqrt(dt))
    return X




"""
    Euler Scheme for the SDE: dX_t = 2σ / (1 + X_t^2) dW_t.
    (example 3 of numerical methods)
    Parameters:
    m (int): Number of time steps.
    N (int): Number of simulations.
    sigma (float): Volatility parameter.
    K (float): Strike price.
    x (float): Initial value of the process.
    T (float): Terminal time.

    Returns:
    float: Statistical error (sqrt(Var(estimator) / N)).
    
def EulerScheme_Numex3(m, N, sigma, K, x, T):

    h = T / m  # Time step size
    X = x + np.zeros(N)  # Initial values

    for j in range(m):
        W = np.random.randn(N) * np.sqrt(h)
        X += (2 * sigma * W) / (1 + X**2)  # SDE dynamics

    payoff = np.maximum(X - K, 0)  # Payoff function
    mean_payoff = np.mean(payoff)
    std_payoff = np.std(payoff)

    return mean_payoff,std_payoff / np.sqrt(N)
"""


# We now provide a Monte Carlo estimation of Euler Scheme in the Markovian Case
def MC_estimator_EulerScheme_Markovian(funcG, X0, funcMu, Sigma0, T, nDim, mSteps, nSamples):

    g_hats = np.zeros(nSamples)

    for i in range(nSamples):
        g_hats[i] = funcG(Euler_Scheme(X0, funcMu, Sigma0, T, mSteps)[-1])

    p = np.mean(g_hats)
    s = np.std(g_hats)

    #test, statistical confidence interval, statistical error
    return p, [p - 1.96 * s / np.sqrt(nSamples), p + 1.96 * s/np.sqrt(nSamples)], s / np.sqrt(nSamples)


# We now provide a Monte Carlo estimation of Euler Scheme for a path-dependent payoff
def MC_estimator_EulerScheme_Pathdep(funcG, X0, funcMu, Sigma0, T,mSteps, nSamples, lTimeIntervals):

    g_hats = np.zeros(nSamples)
    step_size = mSteps // (len(lTimeIntervals)-1) #get the right step for getting (t1,...,tn)
    for i in range(nSamples):
        g_hats[i] = funcG(Euler_Scheme_Pathdep2(X0, funcMu, Sigma0, T, mSteps)[step_size::step_size])

    p = np.mean(g_hats)
    s = np.std(g_hats)

    #test, statistical confidence interval, statistical error
    return p, [p - 1.96 * s / np.sqrt(nSamples), p + 1.96 * s / np.sqrt(nSamples)], s / np.sqrt(nSamples)
