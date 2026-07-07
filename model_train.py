import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader, TensorDataset





df = pd.read_csv('CNC_physics_digital_twin.csv')

X = df[["w", "Fc", "T", "Ra","V", "E", "H"]].to_numpy(dtype=float)
U = df[["f", "N", "c"]].values

Y = df[["w_n", "Fc_n", "T_n", "Ra_n", "V_n", "E_n", "H_n"]].to_numpy(dtype=float)




X_scaled = StandardScaler().fit_transform(X)
U_scaled = StandardScaler().fit_transform(U)
Y_scaled= StandardScaler().fit_transform(Y)

x_tensor = torch.tensor(X_scaled, dtype=torch.float32)
u_tensor = torch.tensor(U_scaled, dtype=torch.float32)
y_tensor = torch.tensor(Y_scaled, dtype=torch.float32)

dataset = TensorDataset(x_tensor, u_tensor, y_tensor)

dataloader = DataLoader(dataset, batch_size=256, shuffle=True)

model = Deepkoopman( state_dime = 7, input_dime = 3, latent_dime = 16)

optim = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-5)
scheduler = torch.optim.lr_scheduler.StepLR(
    optim,
    step_size=200,
    gamma=0.5
)
epoch = 600
for i in range(epoch):

  t_loss = 0
  t_p_loss = 0
  t_r_loss = 0

  for x_batch, u_batch, y_batch in dataloader:
    optim.zero_grad()

    x_n_p, z_n, x_r = model(x_batch, u_batch)

    loss, p_loss, r_loss, _ = model.loss(x_batch,y_batch, x_n_p, x_r, z_n)

    loss.backward()
    optim.step()
    scheduler.step()

    t_loss += loss.item()
    t_p_loss += p_loss.item()
    t_r_loss += r_loss.item()
  if i % 50 == 0:
        print(
            f"Epoch {i} | "
            f"Total Loss: {t_loss:.6f} | "
            f"Prediction: {t_p_loss:.6f} | "
            f"Reconstruction: {t_r_loss:.6f}"
        )
torch.save(model.state_dict(), "DEEPKOOPMAN_CNC_MODEL.pth")

print("Training complete. Model saved")
