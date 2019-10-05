# all online judge code cli

各oj的命令行前端... 想法来源: [leetcode-cli](https://github.com/skygragon/leetcode-cli)

# 进展

- 已支持ctguoj全部功能
- hihocoder 支持登录、查看比赛列表，题目列表，显示题目信息
- 这个无聊的项目先停止了...

# 使用及开发
```
git https://github.com/ctguggbond/aoj-cli.git
cd aoj-cli
运行: python3 aoj/__main__.py
失败需安装相关依赖库

拓展其它oj
参考ctguoj / hihocoer 目录下代码， 实现aojOperate类 然后该改的改，能删的删...
```

# 功能列表:
```
	list -c          | 列出所有正在进行的比赛
	use id           | 根据cid选择比赛
	list -p          | 列出当前比赛题目
	list -c -a       | 列出所有进行和已结束的比赛
	show id          | 显示id对应题目的详细信息
	show id -g c     | 显示题目信息并生成c语言代码文件
	submit filename  | 提交代码文件判题
	show ranking     | 显示当前参加比赛对应的排名
	passed           | 显示已提交的题目列表
	passed id        | 显示所有已提交题目详细信息
 	test filename    | 用测试样例测试当前代码
	login            | 登录
	checkout oj name | 切换oj
	help             | 显示此帮助信息
```
  
# Todo
- 先适配更多oj, 结构及功能还需要在适配更多oj的过程中慢慢添加修改
