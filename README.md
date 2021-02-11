# hso
基于go-cqhttp nonebot2的setu 插件
# TODO
- [X] 发送setu(无需命令符)(默认关闭)
  - 正则匹配`来(.*?)[点丶份张幅](.*?)的?(|r18)[色瑟涩🐍][图圖🤮]`
- setu api:
  - [x] lolicon.app
- [X] 自动撤回
- [x] 群独立配置
- [ ] 统计
- [x] 命令修改配置(最前面加上.env内设置的命令符)
  - 开启/关闭 original   
    是否原图
  - 开启/关闭 setu       
    setu功能开关
  - 开启/关闭 r18        
    是否开启r18
  - 修改 setu_level      
    默认等级 0:正常 1:性感 2:色情 3:All
  - 修改 max_num        
    一次最多数量
  - 修改 revoke         
    setu撤回开关
  - 修改 top            
    色图最大上限(0为无限)
# 配置文件
```
api1=True # 色图库是否开启 api1=lolicon
ps:如果自己添加api后别忘了在config.py中Config添加api对应开关
PRIORITY=[1]  #　色图库(元组)优先级:api0 > api1  如果是[1,0]即为api1 > api0
LOLICON_KEY=none  # lolicon.app 的Key，前往https://api.lolicon.app申请
Friend=True  #
```
# 鸣谢
[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)  
[nonebot2](https://github.com/nonebot/nonebot2)  
[SetuBot](https://github.com/yuban10703/OPQ-SetuBot)  
