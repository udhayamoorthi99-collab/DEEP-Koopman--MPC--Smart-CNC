import torch
import torch.nn as nn

class Deepkoopman(nn.Module):
  def __init__(self, state_dime = 7, input_dime = 3, latent_dime = 16):
     super().__init__()

     self.encoder = nn.Sequential(
         nn.Linear(state_dime, 64),
         nn.ReLU(),
         nn.Linear(64,64),
         nn.ReLU(),
         nn.Linear(64, latent_dime)
     )
     self.decoder = nn.Sequential(
         nn.Linear(latent_dime, 64),
         nn.ReLU(),
         nn.Linear(64, 64),
         nn.ReLU(),
         nn.Linear(64, state_dime))

     self.A = nn.Linear(latent_dime, latent_dime, bias=False)
     self.B = nn.Linear(input_dime, latent_dime, bias=False)

  def forward(self, x, u):
      z = self.encoder(x)
      z_n =  self.A(z) + self.B(u)
      x_n_p = self.decoder(z_n)

      x_r = self.decoder(z) # which we need to know the latent state which is lifted , it is actually comes back to same the input state . to check this we use this
      return x_n_p, z_n, x_r


  def loss(self, x, x_n , x_n_p , x_r, z_n_p):

   loss = nn.MSELoss()
   weights = torch.tensor([
        5.0,   # Tool wear
        1.0,   # Cutting force
        2.0,   # Temperature
        5.0,   # Surface roughness
        3.0,   # Vibration
        1.0,   # Energy
        2.0    # Hardness
    ], device=x.device)

   z_next_true = self.encoder(x_n)

   p_loss = ((x_n_p - x_n) ** 2 * weights).mean()

   r_loss = nn.MSELoss()(x_r, x)
   l_loss = loss(z_n_p,z_next_true)

   total_loss= p_loss + 0.1*r_loss + 1.0*l_loss
   return total_loss, p_loss, r_loss, l_loss




