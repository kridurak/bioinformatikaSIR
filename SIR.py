# The SIR model is one of the simplest compartmental models, 
# and many models are derivatives of this basic form. 
# The model consists of three compartments:

# Susceptible (S), when an individual be infected with the disease;
# Infected (I), when an individual can infect neighbouring susceptible individuals; and
# Removed (R), when an individual has recovered from the infection and neither infects nor can be infected.

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Set initial conditions
N=1000      # total population     
I0=1        # infected     
R0=0        # recovered
S0=N-I0-R0  # everyone else, susceptible to infect
beta=0.2    # contact rate
gamma=0./10 # mean recovery rate (1/days)
time = np.linspace(0,160,160)  # time points (days)

# SIR model differential equations
def derivations(y,time,N,beta,gamma): 
    S,I,R=y
    dS_dt=-beta*S*I            # susceptible deriv
    dI_dt=beta*S*I/N-gamma*I   # infected deriv
    dR_dt=gamma*I              # recovered deriv
    return dS_dt,dI_dt,dR_dt

# Initial conditions vector
y0=S0,I0,R0

# SIR model equations in time
ret=odeint(derivations, y0, time, args=(N, beta, gamma))
# print(ret)
S,I,R=ret.T
# print(ret.T)

# Plot the data curves for S, I, R
fig=plt.figure(facecolor='w')
ax=fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
ax.plot(time, S/1000, 'b', alpha=0.5, lw=2, label='Susceptible')
ax.plot(time, I/1000, 'r', alpha=0.5, lw=2, label='Infected')
ax.plot(time, R/1000, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
ax.set_xlabel('Time /days')
ax.set_ylabel('Number (1000s)')
ax.set_ylim(0,1.2)
ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
ax.grid(b=True, which='major', c='w', lw=2, ls='-')
legend=ax.legend()
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)
plt.show()