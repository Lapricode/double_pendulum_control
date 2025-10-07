import numpy as np
from pendu_visualization import animate_system


# double pendulum system parameters
mass = [0.10548177618443695, 0.07619744360415454]
m1, m2 = mass[0], mass[1]
length = [0.05, 0.05]
l1, l2 = length[0], length[1] 
com = [0.05, 0.03670036749567022]
r1, r2 = com[0], com[1]
inertia = [0.00046166221821039165, 0.00023702395072092597]
I1, I2 = inertia[0], inertia[1]
damping = [7.634058385430087e-12, 0.0005106535523065844]
b1, b2 = damping[0], damping[1]
coulomb_fric = [0.00305, 0.0007777]
mu1, mu2 = coulomb_fric[0], coulomb_fric[1]
grav = 9.81
Ir = 0.0  # rotors inertia
gr = 0.0  # gear ratio between motors and links

# position_limit = []
# velocity_limit = []
torque_limits = [-0.15, 0.15]

# dynamics of the double pendulum
def dynamics(x, u):
    # state x is 4x1 numpy vector
    # # control input u is a 2x1 numpy vector
    q1, q2 = x[0, 0], x[1, 0]  # the 2 angles (joints) in rad
    q1_dot, q2_dot = x[2, 0], x[3, 0]  # the 2 angular velocities in rad/sec
    M = np.block([[I1 + I2 + l1**2*m2 + 2.*l1*m2*r2*np.cos(q2) + gr**2*Ir + Ir, I2 + l1*m2*r2*np.cos(q2)], \
                  [I2 + l1*m2*r2*np.cos(q2), I2]])
    C = np.block([[-2.*q2_dot*l1*m2*r2*np.sin(q2), -q2_dot*l1*m2*r2*np.sin(q2)], \
                  [q1_dot*l1*m2*r2*np.sin(q2), 0.]])
    G = np.block([[grav*m1*r1*np.sin(q1) + grav*m2*(l1*np.sin(q1)+r2*np.sin(q1+q2))], \
                  [grav*m2*r2*np.sin(q1+q2)]])
    F = np.block([[b1*q1_dot + mu1*np.arctan(100.*q1_dot)], \
                  [b2*q2_dot + mu2*np.arctan(100.*q2_dot)]])
    q_ddot = np.linalg.solve(M, u - C @ np.array([[q1_dot], [q2_dot]]) - G - F)
    x_dot = np.zeros((4, 1))
    x_dot[0, 0], x_dot[1, 0], x_dot[2, 0], x_dot[3, 0] = q1_dot, q2_dot, q_ddot[0, 0], q_ddot[1, 0]
    return x_dot  # return the 4x1 state derivative vector

def force_limits(x, min, max):
    return np.minimum(np.maximum(x, min), max)

# this function descritizes the dynamics of the system using the Runge-Kutta 4th order method
def runge_kutta_4th_order(xk, uk, dt):
    f1 = dynamics(xk, uk)
    f2 = dynamics(xk + f1 * dt / 2, uk)
    f3 = dynamics(xk + f2 * dt / 2, uk)
    f4 = dynamics(xk + f3 * dt, uk)
    x = xk + dt / 6 * (f1 + 2*f2 + 2*f3 + f4)
    return x

# simulation parameters
total_time = 10  # total time in sec
dt = 0.005  # time step in sec
x0 = np.array([[np.pi/2], [0.0], [0.0], [0.0]])  # initial state
states = [x0]
x = np.copy(x0)
for step in range(int(total_time/dt)):
    u_new = np.zeros((2, 1))
    u_new = force_limits(u_new, torque_limits[0], torque_limits[1])
    x = runge_kutta_4th_order(x, u_new, dt)  # compute next state
    states.append(x)

animate_system(states, 10, dt, 1, 1)
