# Priconne Automaton

[公主连结 Re:Dive](https://game.bilibili.com/pcr/) 自动机。使用 OpenCV 图像识别来读取屏幕上的控件，通过 UIAutomator2 来实现模拟触控的操作。

本项目重构于 [SimonShi1994 / Princess-connection-farm](https://github.com/SimonShi1994/Princess-connection-farm)，目前还在测试阶段中。

## 特点

* 准确的图像识别和完善的逻辑。
* 更强大的扫荡模版，可以自由配置每个账号扫荡的关卡。
* 更清晰且易用的 API，方便用户实现自己的脚本。
* 支持多开。全局延迟参数收纳，提升多开的容错性。

## 脚本功能

* [x] 农场日常：领取礼物、扫荡、地下城使用支援、捐赠。
* [x] 农场捐赠：单独完成捐赠请求。
* [x] 农场初始：新号从新手教程到 N3-2 开放行会的脚本。
* [ ] 29to1 农场管理：
* [ ] 40to1 农场管理：

## API 功能

1. 批量登录和切换账号。
2. 扫荡模版，支持如 `N1-1*100`、`H10~H12*3`、`N11-4~N12-3` 等灵活的刷图配置。
3. 收取任务、礼物、公会之家。
4. 购买体力、玛那、经验药剂。
5. 行会点赞、捐赠。
6. 角色自动强化。
7. 地下城使用支援。

## 环境

* [Python](https://www.python.org) >= 3.6。
  
  Python 需要的包已经定义在 requirements.txt 中，请使用指令 `pip install requirements.txt` 安装。

* 安卓模拟器，推荐使用 [雷电模拟器](https://www.ldmnq.com)。

  模拟器分辨率设置为 960*540，网络设置为桥接模式，并打开 USB 调试。安装 [公主连结 Re:Dive](https://game.bilibili.com/pcr/)，并下载好全部游戏数据。

## 使用方法

1. 将 `accounts_demo.txt` 复制一份，命名为 `accounts.txt`，按照格式填写好账号的信息。

2. （可选）编辑要运行的脚本（例如 `农场日常.py`），根据自身需求对脚本进行修改。

3. 启动安卓模拟器的多开器，根据电脑性能情况确定多开的数量，复制模拟器后批量启动。

4. 打开终端，切换该项目文件夹目录下。
    ```
    cd D:\
    cd D:\priconne-automaton\
    ```

5. 运行脚本。
    ```
    python 农场日常.py
    ```
