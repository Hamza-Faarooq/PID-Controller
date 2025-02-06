    import numpy as np
		import matplotlib.pyplot as plt
		from scipy import signal
		
		# Define system transfer function G(s) = 1 / (s^3 + 3s^2 + 5s + 1)
		# This represents a third-order dynamic system
		numerator = [1]  # Numerator of the transfer function (constant value 1)
		denominator = [1, 3, 5, 1]  # Denominator coefficients of the characteristic equation
		system = signal.TransferFunction(numerator, denominator)  # Create transfer function object
		
		# Define PID controller transfer function C(s) = Kp + Ki/s + Kd*s
		# PID controller consists of three terms: Proportional (P), Integral (I), and Derivative (D)
		Kp = 50  # Proportional gain: Improves response speed but can cause oscillations
		Ki = 100  # Integral gain: Eliminates steady-state error but may introduce overshoot
		Kd = 10  # Derivative gain: Helps reduce overshoot and improves stability
		
		# Transfer function representation of PID controller: (Kd * s^2 + Kp * s + Ki) / s
		pid_controller = signal.TransferFunction([Kd, Kp, Ki], [1, 0])  
		
		# Compute the closed-loop transfer function: T(s) = C(s)G(s) / (1 + C(s)G(s))
		# This equation represents how the system behaves when controlled by the PID controller
		closed_loop = signal.feedback(signal.series(pid_controller, system))
		
		# Time vector for simulation (0 to 10 seconds with 500 points)
		t = np.linspace(0, 10, 500)
		
		# Compute step response of the closed-loop system
		t, y = signal.step(closed_loop, T=t)  # Step response output
		
		# Add random Gaussian noise to simulate sensor inaccuracies
		noise_level = 0.05  # Noise amplitude
		noise = noise_level * np.random.randn(len(t))  # Generate Gaussian noise
		y_noisy = y + noise  # Add noise to the system response
		
		# Simulate actuator saturation (control signals beyond a threshold are clipped)
		max_control_signal = 10  # Maximum allowed output (actuator limit)
		y_noisy_saturated = np.clip(y_noisy, -max_control_signal, max_control_signal)  # Apply saturation
		
		# Plot the system response with noise and actuator saturation
		plt.figure(figsize=(10, 6))
		plt.plot(t, y_noisy, label="Noisy Output")  # Plot system response with noise
		plt.plot(t, y_noisy_saturated, label="Saturated Output", linestyle='--')  # Plot saturated response
		plt.title('PID Control with Noise and Actuator Saturation')  # Graph title
		plt.xlabel('Time [s]')  # X-axis label
		plt.ylabel('System Output')  # Y-axis label
		plt.legend()  # Show legend
		plt.grid(True)  # Enable grid for better readability
		plt.show()  # Display the plot
