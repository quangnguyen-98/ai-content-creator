import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


class Projectile:
    def __init__(self, mass, angle, velocity, height=0):
        self.mass = mass
        self.angle = angle
        self.velocity = velocity
        self.height = height
        self.g = 9.81  # Acceleration due to gravity (m/s^2)
        
    def trajectory(self, t):
        # Initial position and velocity components
        vx = self.velocity * np.cos(np.radians(self.angle))
        vy = self.velocity * np.sin(np.radians(self.angle))
        x = vx * t
        y = self.height + vy * t - 0.5 * self.g * t ** 2
        return x, y

    def simulate(self, time_end, time_step):
        times = np.arange(0, time_end, time_step)
        x_positions = []
        y_positions = []
        
        for t in times:
            x, y = self.trajectory(t)
            x_positions.append(x)
            y_positions.append(y)
            if y < 0:  # Stop simulation when it hits the ground
                break
                
        return np.array(x_positions), np.array(y_positions)

    def plot_trajectory(self, time_end, time_step):
        x, y = self.simulate(time_end, time_step)
        plt.figure(figsize=(10, 5))
        plt.plot(x, y)
        plt.title('Projectile Motion: Angle = {}°, Velocity = {} m/s'.format(self.angle, self.velocity))
        plt.xlabel('Distance (m)')
        plt.ylabel('Height (m)')
        plt.grid()
        plt.xlim(0, max(x)*1.1)
        plt.ylim(0, max(y)*1.1)
        plt.show()


class Pendulum:
    def __init__(self, length, mass, theta0, b=0):
        self.length = length  # Length of pendulum (m)
        self.mass = mass      # Mass of pendulum bob (kg)
        self.theta0 = theta0  # Initial angle (rad)
        self.b = b            # Damping coefficient
        self.g = 9.81         # Acceleration due to gravity (m/s^2)
        
    def equations(self, t, y):
        theta, omega = y
        dydt = [omega, -(self.b/self.mass) * omega - (self.g/self.length) * np.sin(theta)]
        return dydt

    def simulate(self, time_end, num_points):
        t_span = (0, time_end)
        y0 = [self.theta0, 0]  # Initial angular displacement and velocity
        t_eval = np.linspace(0, time_end, num_points)
        
        sol = solve_ivp(self.equations, t_span, y0, t_eval=t_eval)
        return sol.t, sol.y[0], sol.y[1]

    def plot_pendulum(self, time_end, num_points):
        t, theta, omega = self.simulate(time_end, num_points)
        plt.figure(figsize=(10, 5))
        plt.plot(t, theta, label='Angle (rad)')
        plt.plot(t, omega, label='Angular Velocity (rad/s)')
        plt.title('Pendulum Motion')
        plt.xlabel('Time (s)')
        plt.ylabel('Theta and Omega')
        plt.legend()
        plt.grid()
        plt.show()


class Oscillator:
    def __init__(self, mass, spring_constant, damping_coefficient):
        self.mass = mass
        self.k = spring_constant  
        self.b = damping_coefficient  
    
    def equations(self, t, y):
        x, v = y
        dydt = [v, -(self.k/self.mass) * x - (self.b/self.mass) * v]
        return dydt

    def simulate(self, time_end, num_points):
        t_span = (0, time_end)
        y0 = [1, 0]  # Initial displacement and velocity
        t_eval = np.linspace(0, time_end, num_points)
        
        sol = solve_ivp(self.equations, t_span, y0, t_eval=t_eval)
        return sol.t, sol.y[0], sol.y[1]

    def plot_oscillator(self, time_end, num_points):
        t, x, v = self.simulate(time_end, num_points)
        plt.figure(figsize=(10, 5))
        plt.plot(t, x, label='Displacement (m)')
        plt.plot(t, v, label='Velocity (m/s)')
        plt.title('Damped Harmonic Oscillator Motion')
        plt.xlabel('Time (s)')
        plt.ylabel('Displacement and Velocity')
        plt.legend()
        plt.grid()
        plt.show()


def main():
    # Simulate and plot projectile motion
    projectile = Projectile(mass=1, angle=45, velocity=20)
    projectile.plot_trajectory(time_end=5, time_step=0.1)
    
    # Simulate and plot pendulum motion
    pendulum = Pendulum(length=1, mass=1, theta0=np.radians(60))
    pendulum.plot_pendulum(time_end=10, num_points=500)
    
    # Simulate and plot harmonic oscillator motion
    oscillator = Oscillator(mass=1, spring_constant=10, damping_coefficient=0.5)
    oscillator.plot_oscillator(time_end=10, num_points=500)


if __name__ == '__main__':
    main()