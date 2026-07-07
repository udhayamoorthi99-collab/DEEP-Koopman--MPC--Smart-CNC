#        Deep Koopman MPC for Adaptive CNC Machining using an
#        Industrial Digital Twin


'''
x=[w,Fc​,T,Ra​,V,E,H]

u=[f,N,c]

'''


import numpy as np
import pandas as pd

def cnc_physics_digital_twin(x, u, params):
    """
    x = [w, Fc, T, Ra, V, E, H]
    u = [f, N, c]
    """

    w, Fc, T, Ra, V, E, H = x
    f, N, c = u

    dt = params["dt"]
    D = params["D"]
    ap = params["ap"]
    Tamb = params["Tamb"]

    # Cutting speed: m/min
    Vc = np.pi * D * N / 1000

    #  Cutting force target
    Fc_target = (
        params["Kc"]
        * ap
        * f
        * (1 + params["alpha_w"] * w)
        * (1 + params["beta_H"] * H)
    )
    thermal_softening = 1 - 0.0005 * max(T - 100, 0)

    Fc_target *= thermal_softening

    Fc_next = (
        (1 - params["lambda_F"]) * Fc
        + params["lambda_F"] * Fc_target
    )

    #  Temperature update
    heat_generated = params["eta"] * Fc * Vc
    cooling = params["h_c"] * c * (T - Tamb)
    heat_loss = params["h_l"] * (T - Tamb)

    T_next = T + dt * (
        (heat_generated - cooling - heat_loss)
        / (params["m"] * params["Cp"])
    )

    #  Tool wear update
    wear_rate = (
        params["k_w"] * Fc
        + params["k_T"] * max(T - params["Tcrit"], 0)
        + params["k_v"] * Vc
    )
    if w > 0.2:
      wear_rate *= 1.5

    w_next = w + dt * wear_rate

    #  Surface roughness update
    Ra_theoretical = (f ** 2) / (32 * params["r"])

    Ra_target = (
        Ra_theoretical
        + params["gamma_w"] * w
        + params["gamma_v"] * V
    )

    Ra_next = (
        (1 - params["lambda_R"]) * Ra
        + params["lambda_R"] * Ra_target
    )

    #  Vibration update
    V_target = (
        Fc / params["k_machine"]
        + params["gamma_N"] * abs(N - params["N_res"]) / 1000
    )

    V_next = (
        (1 - params["lambda_V"]) * V
        + params["lambda_V"] * V_target
    )

    #  Energy update
    power_cutting = Fc_next * Vc/60000
    E_next = power_cutting + params["P_aux"] - params["eta_c"] * c

    #  Hardness disturbance
    H_next = (
        0.98 * H
        + np.random.normal(0, params["sigma_H"])
    )

    # Add small sensor/process noise
    noise = np.array([
    np.random.normal(0,0.0005),
    np.random.normal(0,2),
    np.random.normal(0,1),
    np.random.normal(0,0.01),
    np.random.normal(0,0.02),
    np.random.normal(0,5),
    np.random.normal(0,0.5)
    ])

    x_next = np.array([
        w_next,
        Fc_next,
        T_next,
        Ra_next,
        V_next,
        E_next,
        H_next
    ]) + noise

    return np.maximum(x_next, [0, 0, Tamb, 0, 0, 0, 0])


params = {
    "dt": 0.1,
    "D": 50,              # mm
    "ap": 1.5,            # depth of cut, mm
    "Tamb": 25,           # ambient temp, Celsius

    "Kc": 1500,           # specific cutting force
    "alpha_w": 4.0,
    "beta_H": 0.002,
    "lambda_F": 0.3,

    "eta": 0.0004,
    "h_c": 3.0,
    "h_l": 0.8,
    "m": 2.0,
    "Cp": 500,

    "k_w": 1e-6,
    "k_T": 2e-6,
    "k_v": 1e-7,
    "Tcrit": 80,

    "r": 0.8,
    "gamma_w": 1.5,
    "gamma_v": 0.2,
    "lambda_R": 0.2,

    "k_machine": 5000,
    "gamma_N": 0.03,
    "N_res": 3500,
    "lambda_V": 0.25,

    "P_aux": 50,
    "eta_c": 2.0,

    "sigma_H": 0.5
}


rows = []

x = np.array([
    0.02,   # w: tool wear
    100.0,  # Fc: cutting force
    60.0,   # T: temperature
    0.6,    # Ra: surface roughness
    0.1,    # V: vibration
    0.0,    # E: energy
    180.0   # H: hardness
])

samples = 50000

for k in range(samples):
    f = np.random.uniform(0.05, 0.4)      # feed
    N = np.random.uniform(1000, 6000)     # spindle speed
    c = np.random.uniform(0.1, 1.0)       # coolant

    u = np.array([f, N, c])

    x_next = cnc_physics_digital_twin(x, u, params)

    rows.append([
        *x,
        *u,
        *x_next
    ])

    x = x_next


df = pd.DataFrame(rows, columns=[
    "w", "Fc", "T", "Ra", "V", "E", "H",
    "f", "N", "c",
    "w_n", "Fc_n", "T_n", "Ra_n", "V_n", "E_n", "H_n"
])

df.to_csv("CNC_physics_digital_twin.csv", index=False)

print(df.head())
print(df.describe())
