# Example current CNC state:
# x = [w, Fc, T, Ra, V, E, H]
x_current = np.array([0.2, 400, 180, 1.2, 10, 5000, 180])

data = []
for i in range(100):
    
    x_scaled = x_scaler.transform(x_current.reshape(1, -1))[0]

    z0 = encode_state(x_scaled)

    u_scaled = koopman_mpc(z0, A, B, H=10)

# IMPORTANT: use fitted u_scaler from training
    u_real = u_scaler.inverse_transform(u_scaled.reshape(1, -1))[0]

    f = np.clip(f, f_min, f_max)
    N = np.clip(N, N_min, N_max)
    c = np.clip(c, c_min, c_max)

    u_real = np.array([f, N, c])

    x_next = cnc_physics_digital_twin(x_current, u_real, params)

    data.append([i,
        *x_current,
        *u_real,
    ])

    x_current = x_next

result_datasets = pd.DataFrame(data, columns=[
    "time",
    "w", "Fc", "T", "Ra", "V", "P", "H",
    "f", "N", "c"
])

result_datasets.head()
result_datasets.describe()
result_datasets[["Fc", "T", "Ra", "V", "P"]].plot()

##################
# Digital twin MPC 

x_fixed  = np.array([0.2, 400, 180, 1.2, 10, 5000, 180])

fixed_data = []

u_fixed = np.array([0.20, 3500, 0.50])

for t in range(100):
  x_next = cnc_physics_digital_twin(x_fixed, u_fixed, params)
  fixed_data.append([t, *x_fixed, *u_fixed])
  x_fixed = x_next

fixed_result = pd.DataFrame(fixed_data, columns=[
    "time",
    "w", "Fc", "T", "Ra", "V", "P", "H",
    "f", "N", "c"
])

fixed_result

##########################
# Results of comaparisons 

metrics = ["w", "Fc", "T", "Ra", "V", "P"]

comparison = pd.DataFrame({
    "Fixed CNC": fixed_result[metrics].mean(),
    "Deep Koopman MPC": result_datasets[metrics].mean()
})

comparison["Improvement %"] = (
    (comparison["Fixed CNC"] - comparison["Deep Koopman MPC"])
    / comparison["Fixed CNC"]
) * 100

print(comparison)

fixed_result[["Fc", "T", "Ra", "V", "P"]].plot(title="Fixed CNC Parameters")
result_datasets[["Fc", "T", "Ra", "V", "P"]].plot(title="Deep Koopman MPC")
    
