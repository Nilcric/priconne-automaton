from api import *


def function(device):
    if not device.note:
        return

    Sequence(
        登录(device.username, device.password),
        我的主页(),
        行会(),
        行会.捐赠(),
        登出(),
    )(device)


if __name__ == "__main__":
    import main
    main.run(function)
