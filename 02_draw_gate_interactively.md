# 2 Working with matplotlib ineractively 
 
## matplotlib draw graph interactively need nodejs, ipympl and jupyter-extionsion 
Ref [ipympl github](https://github.com/matplotlib/ipympl) 
Ref [matplotlib interaction tutorial](https://matplotlib.org/stable/tutorials/index.html) 
 
Open powershell in Windows
1. define alias: "new-alias grep findstr", "grep" means "findstr" in fellowing cmd.  
 
2. In base env, we update nodejs by "conda install -c conda-forge nodejs".
    nodejs version should be greater than 16 when you check with "conda list | grep nodejs"  
 
3. Activate env "pycyto", "conda activate pycyto".  
 
4. We confirm matplotlib version 3.6.2. otherwise "conda install -c conda-forge matplotlib==3.6.2 nodejs" 
 
5. Install jupyter again, "conda install jupyterlab ipympl ipywidgets"  
 
6. install Jupyter extension, "jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyter-matplotlib" 

7. In case of error when import scanpy, run-install numba and scanpy 
    + update numba, "pip install --upgrade numba" 
    + install scanpy, "pip install scanpy" 
 
8. Create multi-kernel for jupyter, optional.
    + pip install ipykernel
    + python -m ipykernel install --user --name=pycyto
    + conda install Jupyter
    + jupyter kernelspec list
    
8. Run jupyter lab, test fellowing code 
 
## Now, magic %matplotlib should work  
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
