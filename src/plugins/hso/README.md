# hso
基于go-cqhttp nonebot2的setu 插件
# TODO
- [X] 发送setu(无需命令符)
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

# 鸣谢
[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)  
[nonebot2](https://github.com/nonebot/nonebot2)  
[SetuBot](https://github.com/yuban10703/OPQ-SetuBot)  
