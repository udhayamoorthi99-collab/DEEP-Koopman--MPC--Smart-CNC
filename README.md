<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-red)
![CasADi](https://img.shields.io/badge/CasADi-MPC-green)
![Control](https://img.shields.io/badge/Control-Model%20Predictive%20Control-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

</p>
--------------------------------------------------------------------------------------------
                    Deep Koopman MPC for Adaptive CNC Machining 
--------------------------------------------------------------------------------------------

This project presents an AI-driven adaptive control framework for CNC machining using Deep Koopman Learning and Model Predictive Control (MPC). A physics-inspired industrial digital twin is developed to simulate nonlinear machining dynamics including tool wear, cutting force, temperature, surface roughness, vibration, power consumption, and material hardness.

The Deep Koopman model learns a latent linear representation of the nonlinear CNC process, which is then used inside an MPC framework to optimise feed rate, spindle speed, and coolant flow.

## Key Results

Compared with fixed-parameter CNC operation, the proposed Deep Koopman MPC framework achieved:



 Performance Metric | Fixed CNC | Deep Koopman MPC | Improvement |
|-------------------|----------:|-----------------:|------------:|
| Tool Wear         | 0.207     | 0.203            |   2.09%    |
| Cutting Force (N) | **896.05**| **497.65**       | **44.46%** |
| Temperature (°C)  | 189.55     | 175.74          |   7.28%    |
| Surface Roughness (µm) | 0.473 | 0.454           |   3.99%    |
| Vibration         | 0.571      | 0.543           |   5.06%    |
| Power             | 106.47     | 99.41           |   6.64%    |



## Highlights

- Developed a physics-based industrial CNC digital twin
- Implemented Linear System Identification, DMDc, and Deep Koopman models
- Designed a Deep Koopman MPC controller for adaptive machining
- Achieved a 44.46% reduction in cutting force compared with fixed CNC parameters
- Improved machining stability while reducing temperature, vibration, and power consumption

## Industrial Motivation

Modern manufacturing increasingly requires intelligent machining systems capable of adapting to changing operating conditions.

During machining:

-  Tools gradually wear
-  Temperature continuously changes
-  Power consumption varies
-  Cutting forces fluctuate
-  Surface quality degrades

Traditional CNC controllers operate using fixed machining parameters and cannot proactively respond to these changes.

This project demonstrates how Deep Koopman Learning enables nonlinear process modelling while Model Predictive Control continuously adjusts machining parameters to maintain optimal performance.

##  Key Features

- Physics-based CNC Digital Twin
- Synthetic Manufacturing Dataset Generation
- Linear System Identification
- Dynamic Mode Decomposition with Control (DMDc)
- Deep Koopman Neural Network
- Latent Linear Dynamics Learning
- Deep Koopman Model Predictive Control (MPC)
- Closed-loop CNC Process Optimisation
- Comparative Performance Analysis

## Architecture Diagram

  
  Physics-Based CNC Digital Twin
               │
               ▼
      Synthetic Dataset
               │
               ▼
   Linear System Identification
               │
               ▼
        DMDc Baseline
               │
               ▼
      Deep Koopman Learning
               │
               ▼
      Latent Linear Dynamics
               │
               ▼
     Model Predictive Control
               │
               ▼
 Adaptive CNC Process Optimisation

 ## Technology Stack

| Category | Technologies |
|-----------|--------------|
| Programming | Python |
| Machine Learning | PyTorch |
| Control | Model Predictive Control |
| Optimisation | CasADi |
| Scientific Computing | NumPy, Pandas |
| Visualisation | Matplotlib |
| System Identification | Linear SS, DMDc, Deep Koopman |
  

| Folder    | Purpose                                 |
| --------- | --------------------------------------- |
| simulator | Physics-based CNC digital twin          |
| models    | Linear, DMDc, and Deep Koopman models   |
| mpc       | Model Predictive Control implementation |
| notebooks | End-to-end experiments                  |
| results   | Figures, metrics, comparison tables     |
| docs      | Methodology and technical documentation |

## Overall Architecuture 

             Deep Koopman MPC for Adaptive CNC Machining

 ┌─────────────────────────────────────────────────────────────────────┐
 │                 Physics-Based CNC Digital Twin                      │
 │                                                                     │
 │ States: Tool Wear | Force | Temperature | Roughness | Vibration     │
 │          Power | Material Hardness                                  │
 └─────────────────────────────────────────────────────────────────────┘
                               │
                               ▼
                 Synthetic Manufacturing Dataset
                               │
         ┌─────────────────────┴──────────────────────┐
         ▼                                            ▼
 Linear System ID                               Deep Koopman
         │                                            │
         ▼                                            ▼
     Baseline Model                     Latent Linear Representation
         │                                            │
         └─────────────────────┬──────────────────────┘
                               ▼
                    Model Predictive Control (MPC)
                               │
                               ▼
      Feed Rate • Spindle Speed • Coolant Flow Optimisation
                               │
                               ▼
        Reduced Force • Lower Temperature • Improved Quality


## Deep koopman Architecture 

              Current CNC State

                     x(k)
                      │
          ┌───────────▼───────────┐
          │     Encoder Network    │
          └───────────┬───────────┘
                      │
                Latent State z(k)
                      │
        ┌─────────────▼─────────────┐
        │ Linear Koopman Dynamics   │
        │   z(k+1)=Az(k)+Bu(k)      │
        └─────────────┬─────────────┘
                      │
               Latent State z(k+1)
                      │
          ┌───────────▼───────────┐
          │     Decoder Network    │
          └───────────┬───────────┘
                      │
               Predicted CNC State


## Results 
The proposed Deep Koopman MPC framework significantly reduced cutting force while simultaneously improving machining quality, reducing power consumption, and maintaining stable process behaviour.


Fixed CNC
───────────────
High Force
High Temperature
Higher Energy
More Tool Wear

          │

          ▼

Deep Koopman MPC

Lower Force
Lower Temperature
Lower Power
Improved Surface Finish
Adaptive Machining


## Future Improvements

- Robust MPC
- Multi-step Deep Koopman Prediction
- Online Learning
- Reinforcement Learning Controller
- Real CNC Sensor Integration
- Edge Deployment

##  Author

**UDHAYAMOORTHI ARACHALAKUMAR**
Masters in Intelligent Manufacturing, TU Clausthal 

Interests:
- Machine Learning
- Data-Driven Control
- Model Predictive Control
- Industrial AI
