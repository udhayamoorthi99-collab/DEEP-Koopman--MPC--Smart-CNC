# Model Predictive Control

import casadi as ca
import numpy as np
import torch
from sklearn.preprocessing import StandardScaler


f_min, f_max = 0.05, 0.40
N_min, N_max = 1000, 6000
c_min, c_max = 0.1, 1.0

H = 10

model = Deepkoopman( state_dime = 7, input_dime = 3, latent_dime = 16)


A =  model.A.weight.detach().numpy()
B =  model.B.weight.detach().numpy()

def encode_state(x_scaled):
  x_tensor = torch.tensor(x_scaled.reshape(1,-1), dtype=torch.float32)
  with torch.no_grad():

    z = model.encoder(x_tensor).numpy().flatten()
  return z

def koopman_mpc(z0, A, B, H = 10 ):
  latent_dim = A.shape[0]
  input_dim = B.shape[1]

  opti = ca.Opti()

  Z = opti.variable(latent_dim, H+1)
  U  = opti.variable(input_dim , H)

  opti.subject_to(Z[:,0] == z0)

  cost = 0

  for k in range(H):
    z_next = ca.mtimes(A, Z[:,k]) + ca.mtimes(B, U[:, k])
    opti.subject_to(Z[:, k+1]== z_next)

    f = U[0, k]
    N = U[1,k]
    c = U[2, k]

    opti.subject_to(f >= -2)
    opti.subject_to(f <= 2)
    opti.subject_to(N >= -2)
    opti.subject_to(N <= 2)
    opti.subject_to(c >= -2)
    opti.subject_to(c <= 2)
    
    cost += 0.05 * ca.sumsqr(U[:,k])

    cost += 0.5 * ca.sumsqr(Z[:, k+1])
    cost += -0.1 * f

  opti.minimize(cost)

  opti.solver( "ipopt" )
  sol = opti.solve()

  u_scaled = sol.value(U[:, 0])

  return u_scaled 





