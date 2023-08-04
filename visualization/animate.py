import numpy as np
import matplotlib.animation
import matplotlib.pyplot as plt


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

        if light[num] == "green" or light[num] == 'g':
            light_marker.set_markerfacecolor("g")
            light_marker.set_markeredgecolor("g")
        elif light[num] == "yellow" or light[num] == 'y':
            light_marker.set_markerfacecolor("y")
            light_marker.set_markeredgecolor("y")                     
        elif light[num] == "red" or light[num] == 'r':
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