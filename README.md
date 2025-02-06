# PID-Controller

# PID Controller for a Third-Order System with Noise and Actuator Saturation

## Introduction
This project implements a **Proportional-Integral-Derivative (PID) Controller** for a third-order system, considering real-world constraints such as **sensor noise** and **actuator saturation**. The PID controller is used to improve the system's response time, reduce steady-state error, and ensure system stability.

## System Model
The given third-order system is represented by the transfer function:

\[
G(s) = \frac{1}{s^3 + 3s^2 + 5s + 1}
\]

This function represents the dynamic behavior of the system that we aim to control using a PID controller.

## PID Controller Design
A **PID controller** consists of three components:

\[
C(s) = K_p + \frac{K_i}{s} + K_d s
\]

where:
- **\( K_p \) (Proportional gain)**: Reduces error but can cause oscillations if set too high.
- **\( K_i \) (Integral gain)**: Eliminates steady-state error but may cause overshoot.
- **\( K_d \) (Derivative gain)**: Improves stability and reduces overshoot but is sensitive to noise.

For this project, the chosen values are:
- \( K_p = 50 \)
- \( K_i = 100 \)
- \( K_d = 10 \)

These values were selected based on a balance between response speed, stability, and overshoot reduction.

## Implementation Steps

1. **Define the third-order system** using the transfer function.
2. **Design the PID controller** with selected \( K_p, K_i, K_d \).
3. **Compute the closed-loop transfer function**:
   \[
   T(s) = \frac{C(s)G(s)}{1 + C(s)G(s)}
   \]
4. **Simulate system response** using a step input.
5. **Add sensor noise** (random Gaussian noise) to simulate real-world inaccuracies.
6. **Introduce actuator saturation** to prevent excessive control efforts.
7. **Visualize results** by plotting the noisy and saturated responses.

## Real-World Considerations

### **1. Sensor Noise**
Sensor inaccuracies introduce noise into the system. We simulate this using random Gaussian noise:

\[
y_{\text{noisy}} = y + \text{random Gaussian noise}
\]

High-frequency noise significantly affects the **derivative term** of the PID controller, which can lead to excessive oscillations. To mitigate this, we could use **low-pass filtering** or adjust the derivative gain.

### **2. Actuator Saturation**
In practical scenarios, actuators cannot produce unlimited output. To model this, we limit the control signal:

\[
y_{\text{saturated}} = \min(\max(y, -u_{\text{max}}), u_{\text{max}})
\]

Saturation can cause **integral windup**, where the integral term accumulates excessive error. Anti-windup techniques such as **conditional integration** or **clamping** can prevent this issue.

## Python Code
The implementation is done in Python using **SciPy** for system modeling and **Matplotlib** for visualization.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Define system transfer function G(s) = 1 / (s^3 + 3s^2 + 5s + 1)
numerator = [1]  
denominator = [1, 3, 5, 1]
system = signal.TransferFunction(numerator, denominator)

# Define PID controller C(s) = Kp + Ki/s + Kd*s
Kp = 50  
Ki = 100  
Kd = 10  
pid_controller = signal.TransferFunction([Kd, Kp, Ki], [1, 0])  

# Compute closed-loop transfer function: T(s) = C(s)G(s) / (1 + C(s)G(s))
closed_loop = signal.feedback(signal.series(pid_controller, system))

# Time vector for simulation
t = np.linspace(0, 10, 500)

# Step response
t, y = signal.step(closed_loop, T=t)

# Add Gaussian noise to simulate sensor inaccuracies
noise_level = 0.05  
noise = noise_level * np.random.randn(len(t))
y_noisy = y + noise  

# Apply actuator saturation
max_control_signal = 10  
y_noisy_saturated = np.clip(y_noisy, -max_control_signal, max_control_signal)

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(t, y_noisy, label="Noisy Output")
plt.plot(t, y_noisy_saturated, label="Saturated Output", linestyle='--')
plt.title('PID Control with Noise and Actuator Saturation')
plt.xlabel('Time [s]')
plt.ylabel('System Output')
plt.legend()
plt.grid(True)
plt.show()
