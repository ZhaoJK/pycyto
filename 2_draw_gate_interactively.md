# 2 Working with matplotlib ineractively 
 
## matplotlib draw graph interactively need nodejs, ipympl and jupyter-extionsion 
Ref [ipympl github](https://github.com/matplotlib/ipympl) 
Ref [matplotlib interaction tutorial](https://matplotlib.org/stable/tutorials/index.html) 
 
Open powershell in Windows
1. define alias: "new-alias grep findstr", "grep" means "findstr" in fellowing cmd.  
 
2. In base env, we update nodejs by "conda install nodejs".
    nodejs version should be greater than 16 when you check with "conda list | gret nodejs"  
     
3. I prefer python version is 3.9, if not, "conda update -n pycyto python==3.9"  
 
4. Activate env "pycyto", "conda activate pycyto".  
 
5. We confirm matplotlib version 3.6.2. otherwise "conda install matplotlib==3.6.2" 
 
6. Update nodejs again in current env, "conda install nodejs" 
 
7. Install jupyter again, "conda install jupyterlab ipympl ipywidgets"  
 
8. install Jupyter extension, "jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyter-matplotlib" 
 
9. jupyter lab build, then jupyter lab e:\ 


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
