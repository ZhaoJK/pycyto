随着AI的大潮，Python大火大热，学了Py，那就是学了写人工智能的语言，而人工智能著名竞赛Kaggle钦定的在线笔记本：Jupyter可谓是每个AI开发者必备的工具了。用了Jupyter，你才进入了AI的行业；用了Jupyter，你才能与国际赛事接轨；用了Jupyter，你才能写吴恩达的在线作业！(这段请勿当真)



你是不是立刻就想装上它了？

pip install jupyter
jupyter notebook
OK！是不是很简单？当然你要是装的Anaconda，那就更简单了，直接自带，启动即可。什么你连Python都没装？



好的现在它已经运行起来了，但如果你用的是Windows，或者你准备把它放到Windows系统的服务器上，那还有点特别小的问题。Jupyter一般都是作为后台服务运行，以便随时使用，如果你在自己的家用机上运行，它要占一个任务栏格子，而且还要一直打开一个难看的黑框框命令行界面，有时候一不小心就点到它。这是很烦人的，一个合格的笔记本应该学聪明点，在我想用的时候才出来，其他时间呆在后台睡大觉就好。



而在Windows系统的服务器上运行Jupyter，也有问题，大家都知道，想在Windows上活得持久，那就得当个服务，不然一登出所有的用户进程全部都会停掉，而且万一服务器他自己突然不舒服，想重启一下，还得让我们的Jupyter也随系统启动（不是随用户登录启动哦）。



想想其他的第三方服务，什么Tomcat啊，装完直接给你塞个Windows服务，那叫一个方便，你Jupyter是看不起我Windows？，既然它不支持，那还得自己来支持。



Google了一会，没找到怎么让它当个服务的方法，倒是看到个偏方，那就是用任务计划程序：(网址见这里 Directions For Running Jupyter In The Background On Windows)。不过我不喜欢这种方式，明明人家微软给准备了个服务功能专门干这事，用任务计划干嘛。

......一小时后



在研究了一番Jupyter的源码之后，写出了用代码启动和停止它的方法，再配合Pywin32，成功地把它搞成了一个服务！好的不瞎扯了，首先你需要安装Pywin32（这个Anaconda也没带）：



pip install pywin32
python Scripts/pywin32_postinstall.py -install
同样是两条命令搞定，想当年Pywin32还得下安装包，现在它也终于敌不过历史的进程，从过气的Sourceforge搬到了Github，从安装包安装变成了pip安装。



万事具备，有请启动脚本登场！！！

import inspect
import logging
import os
import win32serviceutil
from notebook.notebookapp import NotebookApp, JupyterApp

# 作为服务运行时的工作目录是system32，这里改为文件所在目录
current_file = os.path.abspath(inspect.getfile(inspect.currentframe()))
os.chdir(os.path.dirname(current_file))

class NotebookService(win32serviceutil.ServiceFramework):

	_svc_name_ = "JupyterNotebook"
	_svc_display_name_ = "Jupyter Notebook Service"
	_svc_description_ = "Jupyter的服务啦"

	def __init__(self, args):
		super().__init__(args)
		self.app = NotebookApp()

	def _init_notebook(self):
		JupyterApp.initialize(self.app)
		self.app.init_configurables()
		self.app.init_components()
		self.app.init_webapp()
		self.app.init_terminals()
		self.app.init_server_extensions()
		self.app.init_mime_overrides()
		self.app.init_shutdown_no_activity()

	def SvcDoRun(self):
		self.app.config_dir = "config" # 设置配置文件目录
		self._init_notebook()
		logging.getLogger("NotebookApp").addHandler(logging.FileHandler("notebook.log"))
		self.app.start()

	def SvcStop(self):
		self.app.stop()

	def SvcShutdown(self):
		self.SvcStop()


if __name__ == '__main__':
	win32serviceutil.HandleCommandLine(NotebookService)


OK！是不是很简单？带注释50行不到，你可以直接新建一个py文件,比如叫winservice.py,然后把它粘贴进去保存，再以管理员权限运行

python winservice.py install --startup=auto
之后打开服务就能看到它已经进去了（默认服务名 Jupyter Notebook Service）。



其他注意事项
如果在服务器上运行，并由公网访问，那是需要配置一下的，比如设密码啊、改端口啊，具体可以直接百度或谷歌一大堆教程，这里就不说了。



修改了配置文件后又有个小问题，那就是默认安装的服务是以系统账户运行的，你要是在用户目录保存了Jupyter的配置文件，它是找不到的。一种解决方法是在服务面板里修改登录身份为你的账户，或者在安装服务时加上参数。

python winservice.py install --startup=auto --username=xxx --password=xxx


还有一种方法就是自定义配置文件位置，看到代码里那个设置配置文件目录 的注释了没，把前面的字符串改成配置文件所在的目录，比如C:\\Users\\Administor\\.jupyter，或者把配置文件复制到指定的目录里即可。
