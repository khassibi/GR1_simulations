import numpy as np
import matplotlib.animation
import matplotlib.pyplot as plt

from matplotlib.patches import Rectangle
from matplotlib.patches import Circle

from matplotlib.animation import FuncAnimation

from IPython.display import HTML

def _plot_grid(ax, xmin, xmax, ymin, ymax, xint, yint, labels):
    grid_width = 1
    intersection_grid_width = 5
    font_pt = 8

    ax.set_xlim((xmin, xmax))
    ax.set_ylim((ymin, ymax))

    for x in range(xmin, xmax + 1):
        if x > xint or x < 0:
            ax.plot([x, x], [0, yint], "k-", linewidth=grid_width)
        else:
            ax.plot([x, x], [ymin, ymax], "k-", linewidth=grid_width)
    for y in range(ymin, ymax + 1):
        if y > yint or y < 0:
            ax.plot([0, xint], [y, y], "k-", linewidth=grid_width)
        else:
            ax.plot([xmin, xmax], [y, y], "k-", linewidth=grid_width)

    for x in [0, xint]:
        ax.plot([x, x], [0, yint], "y-", linewidth=intersection_grid_width)
    for y in [0, yint]:
        ax.plot([0, xint], [y, y], "y-", linewidth=intersection_grid_width)

    for name, coord in labels.items():
        ax.text(coord[0] - 0.5, coord[1] - 0.5, name, size=font_pt)

    ax.axis("equal")
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)


def animate_intersection(light, paths, title):
    colors = "bgcmyk"
    fig, ax = plt.subplots()
    fig.suptitle(title)

    xmin = -1
    xmax = 2
    ymin = -1
    ymax = 6
    xint = 2
    yint = 2

    # The name of the cell and the coordinate of its center
    labels = {}
    last_idx = -1
    for i in range(ymax - ymin):
        last_idx += 1
        labels["c" + str(last_idx)] = (0 + 0.5, ymax - i - 0.5)
    for i in range(xmin, 1):
        last_idx += 1
        labels["c" + str(last_idx)] = (1.5, i + 0.5)
    last_idx += 1
    labels["c" + str(last_idx)] = (-0.5, 1.5)

    def init():
        _plot_grid(ax, xmin, xmax, ymin, ymax, xint, yint, labels)

    def update_line(num, path_dlist, path_lines, light_marker):
        for count, ((point, trail), path_data) in enumerate(zip(path_lines, path_dlist)):
            shift = 0
            if count == 2:
                shift = -0.33
                point.set_markersize(5)
            trail.set_data(path_data[..., : num + 1] + [[shift], [0]])
            point.set_data(path_data[..., num] + [shift, 0])

        if 'g' in light[num]:
            light_marker.set_markerfacecolor("g")
            light_marker.set_markeredgecolor("g")
        elif 'y' in light[num]:
            light_marker.set_markerfacecolor("y")
            light_marker.set_markeredgecolor("y")                     
        elif 'r' in light[num]:
            light_marker.set_markerfacecolor("r")
            light_marker.set_markeredgecolor("r")
        else:
            light_marker.set_markerfacecolor("b")
            light_marker.set_markeredgecolor("b")

        return path_lines, light_marker

    path_data = []
    path_lines = []
    (light_marker,) = ax.plot(xint, yint, "o", markersize=20.0, zorder=3)
    for n, path in enumerate(paths):
        arr = np.array([labels[cell] for cell in path]).transpose()
        path_data.append(arr)
        (point,) = ax.plot([], [], "o", color=colors[n], markersize=10.0, zorder=2)
        (path_trail,) = ax.plot([], [], "-", color=colors[n], zorder=1)
        path_lines.append((point, path_trail))

    anim = matplotlib.animation.FuncAnimation(
        fig,
        update_line,
        len(paths[0]),
        init_func=init,
        fargs=(path_data, path_lines, light_marker),
        interval=500,
    )

    return anim

def _plot_grid_car(ax, xmin, xmax, ymin, ymax, labels):
    grid_width = 1
    font_pt = 8

    ax.set_xlim((xmin, xmax))
    ax.set_ylim((ymin, ymax))

    # Outlining the blocker's path
    bpath = Rectangle((xmin+1, ymin), 1, ymax-ymin, edgecolor='none', facecolor='purple', alpha=0.3)
    ax.add_patch(bpath)

    goal = Rectangle((xmin, ymax-1), 1, 1, edgecolor='none', facecolor='cyan', alpha=0.3)
    ax.add_patch(goal)

    refuel_zone = Rectangle((xmax-1, 2), 1, 1, edgecolor='none', facecolor='orange', alpha=0.3)
    ax.add_patch(refuel_zone)

    for x in range(xmin, xmax + 1):
        ax.plot([x, x], [ymin, ymax], "k-", linewidth=grid_width)
    for y in range(ymin, ymax + 1):
        ax.plot([xmin, xmax], [y, y], "k-", linewidth=grid_width)

    for name, coord in labels.items():
        ax.text(coord[0] - 0.5, coord[1] - 0.5, name, size=font_pt)

    ax.axis("equal")
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

def animate_pat_car(fuel, paths, title, max_fuel):
    colors = "bgcmyk"
    fig, ax = plt.subplots()
    fig.suptitle(title)

    # Setting the boarders of the grid
    xmin = 0
    xmax = 5
    ymin = 0
    ymax = 5
    # The location of the fuel markers
    xint = 6
    yint = 0

    # The name of the cell and the coordinate of its center
    labels = {}
    for x in range(xmin, xmax, 1):
        for y in range(ymin, ymax, 1):
            labels['c' + str(x) + str(y)] = (x + 0.5, y + 0.5)

    def init():
        _plot_grid_car(ax, xmin, xmax, ymin, ymax, labels)

    def update_line(num, path_dlist, path_lines, fuel_marker):
        for count, ((point, trail), path_data) in enumerate(zip(path_lines, path_dlist)):
            shift = 0
            if count == 2:
                shift = -0.33
                point.set_markersize(5)
            trail.set_data(path_data[..., : num + 1] + [[shift], [0]])
            point.set_data(path_data[..., num] + [shift, 0])
        
        # colors['r','g','b']
        # fuel_marker.set_markerfacecolor('r')
        # font_pt = 8
        # fuel_txt = ax.text(xmax, ymax, str(fuel), size=font_pt)

        for i, fuel_marker in enumerate(fuel_markers):
            if i >= fuel[num]:
                fuel_marker.set_markerfacecolor('w')
            else:
                fuel_marker.set_markerfacecolor('r')

        return path_lines, fuel_marker

    path_data = []
    path_lines = []
    fuel_markers = []
    for i in range(max_fuel):
        fuel_markers.append(ax.plot(xint, yint + i*0.5, "bs", markersize=20.0, zorder=3)[0])

    shapes = ['o', 'D']
    for n, path in enumerate(paths):
        arr = np.array([labels[cell] for cell in path]).transpose()
        path_data.append(arr)
        (point,) = ax.plot([], [], shapes[n], color=colors[n], markersize=10.0, zorder=2)
        (path_trail,) = ax.plot([], [], "-", color=colors[n], zorder=1)
        path_lines.append((point, path_trail))

    anim = matplotlib.animation.FuncAnimation(
        fig,
        update_line,
        len(paths[0]),
        init_func=init,
        # fargs=(path_data, path_lines, light_marker),
        fargs=(path_data, path_lines, fuel_markers),
        interval=500,
    )

    return anim

def _plot_grid_T(ax, xmin, xmax, ymin, ymax, xint, yint, labels):
    grid_width = 1
    font_pt = 8

    ax.set_xlim((xmin, xmax))
    ax.set_ylim((ymin, ymax))

    for x in range(xint, xint + 2):
        ax.plot([x, x], [ymin, ymax], "k-", linewidth=grid_width)
    for y in range(ymin, ymax+1):
        ax.plot([xint, xint+1], [y, y], "k-", linewidth=grid_width)
    for y in range(yint, yint + 2):
        ax.plot([xmin, xmax], [y, y], "k-", linewidth=grid_width)
    for x in range(xmin, xmax+1):
        ax.plot([x, x], [yint, yint+1], "k-", linewidth=grid_width)

    

    for name, coord in labels.items():
        ax.text(coord[0] - 0.5, coord[1] - 0.5, name, size=font_pt)

    ax.axis("equal")
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

def animate_Tgame(paths, title):
    colors = "bgcmyk"
    fig, ax = plt.subplots()
    fig.suptitle(title)

    # Setting the boarders of the grid
    xmin = 0
    xmax = 4
    ymin = 0
    ymax = 5
    # Where the T is
    xint = 2
    yint = 2

    # The name of the cell and the coordinate of its center
    labels = {}
    for x in range(xmin, xmax, 1):
        labels['c' + str(x)] = (x + 0.5, yint + 0.5)
    text_counter = 0
    for y in range(ymin, ymax, 1):
        labels['b=' + str(y)] = (xint + 0.5, y + 0.5)
        text_counter += 1
        if text_counter != 3:
            labels['c' + str(y + 4)] = (x + 0.5, ymax - yint + 0.5)
        else:
            labels[''] = (x + 0.5, ymax - yint + 0.5)

    def init():
        _plot_grid_T(ax, xmin, xmax, ymin, ymax, xint, yint, labels)

    def update_line(num, path_dlist, path_lines):
        for count, ((point, trail), path_data) in enumerate(zip(path_lines, path_dlist)):
            shift = 0
            if count == 2:
                shift = -0.33
                point.set_markersize(5)
            trail.set_data(path_data[..., : num + 1] + [[shift], [0]])
            point.set_data(path_data[..., num] + [shift, 0])

        return path_lines

    path_data = []
    path_lines = []
    for n, path in enumerate(paths):
        arr = np.array([labels[cell] for cell in path]).transpose()
        path_data.append(arr)
        (point,) = ax.plot([], [], "o", color=colors[n], markersize=10.0, zorder=2)
        (path_trail,) = ax.plot([], [], "-", color=colors[n], zorder=1)
        path_lines.append((point, path_trail))

    anim = matplotlib.animation.FuncAnimation(
        fig,
        update_line,
        len(paths[0]),
        init_func=init,
        fargs=(path_data, path_lines),
        interval=500,
    )

    return anim

def animate_Rs(R, trajectory, title):
    # Setup plot
    fig, ax = plt.subplots()
    fig.suptitle(title)
    max_rad = len(R) + 1
    ax.set_xlim(-max_rad, max_rad)  # Set wide enough limits to enclose all circles
    ax.set_ylim(-max_rad, max_rad)
    ax.set_aspect('equal', adjustable='datalim')  # Keep the aspect ratio of the plot square
    # Create circles and add them to the axes
    # circles = [Circle((0, 0), radius=i+1, fill=False, color='blue', alpha=0.5, edgecolor='blue', linewidth=1.5) for i in sorted(R, reverse=False)]
    circles = [Circle((0, 0), radius=i+1, fill=False, edgecolor='black', linewidth=1.5) for i in R]
    for circle in circles:
        ax.add_patch(circle)
    
    # Animation update function
    def update(frame):
        # node = trajectory[frame % len(trajectory)]
        node = trajectory[frame]
        
        # Reset all circles to non-highlighted state
        for circle in circles:
            circle.set_edgecolor('black')
            circle.set_linewidth(1.5)
        
        # the find_R_i function in test_builder
        i = 0
        while i < len(R):
            if node not in R[i]:
                i += 1
            else:
                break
        
        # Highlight the relevant circle(s)
        # for i, circle in enumerate(circles):
        #     if node in R[len(R) - 1 - i]:  # Adjust index for reverse order of circles
        #         # circle.set_edgecolor('red')
        #         circle.set_facecolor('red')  # Change fill color
        #         circle.set_alpha(0.8)  # Less transparency for highlight
        #         circle.set_linewidth(3.0)
        circle = circles[i]
        circle.set_edgecolor('red')
        circle.set_linewidth(3.0)
        
        return circles
    
    # Initialize function to reset the view during the first frame
    def init():
        for circle in circles:
            circle.set_edgecolor('blue')
            circle.set_linewidth(1.5)
        return circles

    # Create and display the animation
    ani = FuncAnimation(fig, update, frames=len(trajectory), init_func=init, blit=False, repeat=True)

    return ani
    # Use HTML to display the animation within the notebook
    # HTML(ani.to_jshtml())
    # Save the animation to an HTML file
    # with open(title, 'w') as f:
    #     print(ani.to_jshtml(), file=f)