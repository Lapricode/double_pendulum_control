import numpy as np
import matplotlib.pyplot as plt

# this function visualizes the states of the system during time
def visualize_system_states(states, dt):
    # initially, create the figure and the subplots
    fig = plt.figure(figsize = (10, 7))  # the figure object
    fig.suptitle("Visualizing the states (angles and angular velocities) of the system", fontsize = 14)  # the figure's title
    ax_q1_q2 = fig.add_subplot(1, 2, 1)  # subplot for angles q1 and q2 (joints)
    ax_q1_q2.set_title("Angles ${q}_1$, ${q}_2$ (joints)", fontsize = 10, fontweight = "bold")
    ax_q1_q2.set_xlabel("t(sec)", fontsize = 8, loc = "right")
    ax_q1_q2_dot = fig.add_subplot(1, 2, 2)  # subplot for angular velocities q1_dot and q2_dot
    ax_q1_q2_dot.set_title("Angular velocities $\dot{q}_1$, $\dot{q}_2$", fontsize = 10, fontweight = "bold")
    ax_q1_q2_dot.set_xlabel("t(sec)", fontsize = 8, loc = "right")
    t = np.array(range(len(states))) * dt  # the time vector (x-axis of the subplots)
    # plot the angles q1, q2 (joints)
    ax_q1_q2.plot(t, [s[0] for s in states], color = "blue", linewidth = 2, linestyle = "-", label = "${q}_1$ (rad)")
    ax_q1_q2.plot(t, [s[1] for s in states], color = "red", linewidth = 2, linestyle = "-", label = "${q}_2$ (rad)")
    ax_q1_q2.legend(loc = "upper right", fontsize = 8)
    # plot the angular velocities q1_dot and q2_dot
    ax_q1_q2_dot.plot(t, [s[2] for s in states], color = "blue", linewidth = 2, linestyle = "-", label = "$\dot{q}_1$ (rad/s)")
    ax_q1_q2_dot.plot(t, [s[3] for s in states], color = "red", linewidth = 2, linestyle = "-", label = "$\dot{q}_2$ (rad/s)")
    ax_q1_q2_dot.legend(loc = "upper right", fontsize = 8)
    plt.show()  # show the plots

# this function updates the frame of the animation of the double pendulum system
def update_frame(ax_visualization, x1, y1, x2, y2):
    ax_visualization.axhline(y = 0, color = "brown", lw = 10, label = "ceiling")  # draw a brown line representing the ceiling
    ax_visualization.plot(0, 0, "ks", markersize = 15, label = "origin")  # draw a square representing the fixed base-point (origin)
    ax_visualization.plot([0, x1], [0, y1], "b-", lw = 5, label = "link l1")  # draw a line representing the first link l1
    ax_visualization.plot([x1, x2], [y1, y2], "r-", lw = 5, label = "link l2")  # draw a line representing the second link l2
    ax_visualization.plot(x1, y1, "bo", markersize = 20, label = "mass m1")  # draw a point representing the mass m1
    ax_visualization.plot(x2, y2, "ro", markersize = 20, label = "mass m2")  # draw a point representing the mass m2
    
# this function animates the movement of the double pendulum system
def animate_system(states, states_step, time_step, l1, l2):
    fig, (ax_visualization, ax_trajectories) = plt.subplots(1, 2)  # create the figure and the subplots for the visualization of the system and the trajectories of the two masses
    fig.canvas.mpl_connect("key_release_event", lambda event: [exit(0) if event.key == "escape" else None])  # close the figure when pressing the escape key
    fig.suptitle("Animate movement", fontsize = 14, fontweight = "bold")  # the figure's title
    ax_visualization.grid(False)  # do not show the ax_visualization's grid
    ax_visualization.set_aspect("equal")  # set the aspect ratio of the ax_visualization to 1
    ax_trajectories.grid(True)  # show the ax_trajectories's grid
    ax_trajectories.set_aspect("equal")  # set the aspect ratio of the ax_trajectories to 1
    states_chosen = [states[i] for i in range(0, len(states), states_step)]  # choose the states to be visualized
    for k in range(len(states_chosen)):
        ax_visualization.cla()  # clear the ax_visualization plot
        ax_visualization.set(xlim = [-1.2*(l1+l2), 1.2*(l1+l2)], ylim = [-1.2*(l1+l2), 1.2*(l1+l2)])  # update the ax_visualization limits
        ax_trajectories.set(xlim = [-1.2*(l1+l2), 1.2*(l1+l2)], ylim = [-1.2*(l1+l2), 1.2*(l1+l2)])  # update the ax_trajectories limits
        # the current positions of the masses m1 and m2
        x1, y1 = l1*np.sin(states_chosen[k][0, 0]), -l1*np.cos(states_chosen[k][0, 0])
        x2, y2 = x1 + l2*np.sin(states_chosen[k][0, 0] + states_chosen[k][1, 0]), y1 - l2*np.cos(states_chosen[k][0, 0] + states_chosen[k][1, 0])
        update_frame(ax_visualization, x1, y1, x2, y2)  # update the state of the system
        if k != 0:
            # the previous positions of the masses m1 and m2
            x1_old, y1_old = l1*np.sin(states_chosen[k-1][0, 0]), -l1*np.cos(states_chosen[k-1][0, 0])
            x2_old, y2_old = x1_old + l2*np.sin(states_chosen[k-1][0, 0] + states_chosen[k-1][1, 0]), y1_old - l2*np.cos(states_chosen[k-1][0, 0] + states_chosen[k-1][1, 0])
            ax_trajectories.plot([x1_old, x1], [y1_old, y1], "b-", lw = 2)  # plot the trajectory of the mass m1
            ax_trajectories.plot([x2_old, x2], [y2_old, y2], "r-", lw = 2)  # plot the trajectory of the mass m2
        plt.pause(1.0 if k == 0 else time_step)  # pause the animation for 1 second if it is the first state, otherwise pause for time_step seconds
    print("\nAnimation finished!")  # print a message
    ax_trajectories.legend(["m1", "m2"], loc = "upper right", fontsize = 8)
    plt.show()  # keep the plot open
