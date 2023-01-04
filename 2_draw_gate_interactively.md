# 2 Working with matplotlib ineractively

## matplotlib draw graph interactively need nodejs, ipympl and jupyter-extionsion
Ref ipympl (github)[https://github.com/matplotlib/ipympl]
Ref [matplotlib interaction tutorial](https://matplotlib.org/stable/tutorials/index.html)

1. install matplotlib stable version
    pip install -U matplotlib
2. install nodejs and ipympl
    conda install -c conda-forge ipympl nodejs
3. install jupyter extension - widgets and matplotlib, then re-build jupyter lab
    jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyter-matplotlib
    jupyter lab build

## Now, magic %matplotlib should work
run fellowing code in jupyter lab

*****************
%matplotlib ipympl

import matplotlib.pyplot as plt

def draw_polygon(points):
    x = [point[0] for point in points]
    y = [point[1] for point in points]
    plt.plot(x, y, 'o-')
    plt.show()

points = []

def onclick(event):
    global points
    points.append((event.xdata, event.ydata))
    if len(points) > 1:
        draw_polygon(points)

fig, ax = plt.subplots()
fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()

********