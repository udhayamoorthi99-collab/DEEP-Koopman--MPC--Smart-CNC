import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error




df = pd.read_csv('CNC_physics_digital_twin.csv')

X = df[["w", "Fc", "T", "Ra","V", "E", "H"]].to_numpy(dtype=float)
U = df[["f", "N", "c"]].values

Y = df[["w_n", "Fc_n", "T_n", "Ra_n", "V_n", "E_n", "H_n"]].to_numpy(dtype=float)



x_scaler = StandardScaler()
u_scaler = StandardScaler()
y_scaler = StandardScaler()

u_scaler.fit(U)
x_scaler.fit(X)
y_scaler.fit(Y)   

X_scaled = x_scaler.fit_transform(X)
U_scaled = u_scaler.fit_transform(U)
Y_scaled = y_scaler.fit_transform(Y)

x_tensor = torch.tensor(X_scaled, dtype=torch.float32)
u_tensor = torch.tensor(U_scaled, dtype=torch.float32)
y_tensor = torch.tensor(Y_scaled, dtype=torch.float32)


model = Deepkoopman( state_dime = 7, input_dime = 3, latent_dime = 16)

model.load_state_dict(torch.load("DEEPKOOPMAN_CNC_MODEL.pth"))
model.eval()

with torch.no_grad():
    Y_p_lift, _, _ = model(x_tensor, u_tensor)

Y_p_lift = Y_p_lift.detach().numpy()

y_p = x_scaler.inverse_transform(Y_p_lift)

mse = mean_squared_error(Y, y_p)
mae = mean_absolute_error(Y, y_p)

print("Deep Koopman MSE:", mse)
print("Deep Koopman MAE:", mae)


state_names = ["Tool Wear", "Cutting Force", "Temperature", "Surface Roughness", "vibrations", "energy consuptions", "hardness"]


for i, name in enumerate(state_names):
    error = mean_absolute_error(Y[:, i], y_p[:, i])
    print(f"{name} MAE:", error)
