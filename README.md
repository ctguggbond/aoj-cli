# all online judge code cli

各oj的命令行前端... 参考 leetcode-cli

- 已支持ctguoj全部功能
- hihocoder 接入登录 获取比赛列表

功能列表:
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
- 改改结构, 争取能适配更多的oj
