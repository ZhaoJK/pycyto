1. step 1 _ install anaconda or miniconda 
	+ download from https://repo.anaconda.com/archive/Anaconda3-2022.10-Windows-x86_64.exe 
	+ install by double click Anaconda3-2022.10-Windows-x86_64.exe 
	+ you might have to run "conda init" for initiation accordinglly. 
	
2. step 2 _ create conda environment with a name you like, for example **pycyto** 
	+ how to use conda ref: https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html 
	+ run "powershell prompt (anaconda3)" or "anaconda prompt (annconda3)" 
	+ run command: **conda create -n pycyto python**, it will create a environment named "pycyto" and install python 
 
3. step 3 _ activate conda environemnt 
	+ activate env "pycyto": **conda activate pycyto** 
	+ install library within your environment with commands: "conda(or mamba ) install 'your lib or pkg name'", like  
		+ **conda install -c conda-forge mamba**  (mamba is a tool same as conda but faster than conda when install libs or pkgs from conda repository, we will replace conda with mamba in following steps) 
		+ **mamba install -c conda-forge jupyterlab** (install jupyterlab from "conda-forge", "conda-forge" is a conda repository) 
		+ **mamba install -c conda-forge spyder** (editor of py with perfect user interface) 
		+ **mamba install -c conda-forge pip** (pip is a tool, which help you install packages from pipy, a python repo) 
	 + or install batchly,  
	  	+ **mamba install -c conda-forge jupyterlab, spyder, pip** 
	+ install packages from pipy, bacause Pytometry published in [pipy](https://pypi.org/project/pytometry/) and [github](https://github.com/buettnerlab/pytometry) but not in conda repo 
		+ **pip install Pytometry** (wainting for finishing all installation) 
 
4. (Optional)step 4 _ modify jupyter configure, if you are going to work outside of your personal directory "C:\Users\username"
	+ in cmd run, jupyter notebook --generate-config
	+ find configure files in C:\Users\username\.jupyter\jupyter_notebook_config.py 
	+ edit #c.NotebookApp.notebook_dir = '' >> c.NotebookApp.notebook_dir = 'path to your folder', like "F:\\"
	+ run jupyterlab by typing "jupyter lab" 
5. Step 5 _ run jupyterlab locally
 	+ start **Anaconda Prompt (pycyto)** if exist, otherwise start **Anaconda Prompt (anaconda3)** 
 	+ run **conda activate pycyto**, if you start from **Anaconda Prompt (anaconda3)**
 	+ run **jupyter lab**, waiting for commands open your default explorer like Chrome, then load jupyterlab.
 	+ Strat working ... 
