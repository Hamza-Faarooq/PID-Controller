clc; clear; close all;

% Define system transfer function G(s) = 1 / (s^3 + 3s^2 + 5s + 1)
num = [1]; 
den = [1, 3, 5, 1]; 
G = tf(num, den);

% Define PID controller C(s) = Kp + Ki/s + Kd*s
Kp = 50;  % Proportional gain
Ki = 100; % Integral gain
Kd = 10;  % Derivative gain

% PID Controller Transfer Function: C(s) = Kp + Ki/s + Kd*s
C = tf([Kd, Kp, Ki], [1, 0]); 

% Closed-loop transfer function: T(s) = (C(s) * G(s)) / (1 + C(s) * G(s))
T_closed = feedback(C * G, 1);

% Time vector for simulation
t = linspace(0, 10, 500);

% Step response
[y, t] = step(T_closed, t);

% Add Gaussian noise to simulate sensor inaccuracies
noise_level = 0.05;  % Noise intensity
noise = noise_level * randn(size(y));
y_noisy = y + noise;

% Simulate actuator saturation (limit output)
max_control_signal = 10;
y_noisy_saturated = min(max(y_noisy, -max_control_signal), max_control_signal);

% Plot results
figure;
plot(t, y_noisy, 'b', 'LineWidth', 1.5); hold on;
plot(t, y_noisy_saturated, 'r--', 'LineWidth', 1.5);
xlabel('Time (s)');
ylabel('System Output');
title('PID Control with Noise and Actuator Saturation');
legend('Noisy Output', 'Saturated Output');
grid on;

