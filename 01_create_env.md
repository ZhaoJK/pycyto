1. step 1 _ install anaconda or miniconda 
	+ download from https://repo.anaconda.com/archive/Anaconda3-2022.10-Windows-x86_64.exe 
	+ install by double click Anaconda3-2022.10-Windows-x86_64.exe 
	+ you might have to run "conda init" for initiation accordinglly. 
	
2. step 2 _ create conda environment with a name you like, for example "pycyto" 
	+ how to use conda ref: https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html 
	+ run "powershell prompt (anaconda3)" 
	+ run command: "conda create -n pycyto python", it will create a environment named "pycyto" and install python, mamba (mamba is a tool same as conda but faster than conda when install libs or pkgs from conda repository) 
 
3. step 3 _ activate conda environemnt 
	+ activate env "pycyto": conda activate pycyto 
	+ install library within your environment with commands: "conda(or mamba ) install 'your lib or pkg name'", like  
		+ conda install -c conda-forge mamba
		+ mamba install -c conda-forge jupyterlab (install jupyterlab from "conda-forge", "conda-forge" is a conda repository) 
		+ mamba install -c conda-forge spyder 
		+ mamba install -c conda-forge pip 
	 + or install batchly,  
	  	+ mamba install -c conda-forge jupyterlab, spyder, pip 
	+ install libs from pipy, bacause Pytometry published in pipy ang github but not in conda repo 
		+ pip install Pytometry 
 
4. step 4 _ modify jupyter configure
	+ in cmd run, jupyter notebook --generate-config
	+ find configure files in C:\Users\username\.jupyter\jupyter_notebook_config.py 
	+ edit #c.NotebookApp.notebook_dir = '' >> c.NotebookApp.notebook_dir = 'path to your folder', like "F:\\"
	+ run jupyterlab by typing "jupyter lab" 
