import os
import re
import time
import queue
import threading
import uiautomator2

from api import *


def get_device_addresses():
    assert not os.system('adb\\adb connect 127.0.0.1')
    assert not os.system('python -m uiautomator2 init')

    out = os.popen('adb\\adb devices').read()
    addresses = []
    for line in out.split('\n'):
        match = re.match(r'(\S+)\s*device', line)
        if match:
            address = match.groups()[0]
            addresses.append(address)

    return addresses


def get_accounts():
    accounts = queue.Queue()
    with open('accounts.txt') as f:
        for line in f:
            match = re.match(r'(\S+)\s+(\S+)\s*(\S*)', line)
            if match:
                account = match.groups()
                accounts.put(account)

    return accounts


def thread(address: str, accounts: queue.Queue, function):
    device = uiautomator2.connect(address)
    device.app_start('com.bilibili.priconne')

    while True:
        try:
            username, password, note = accounts.get_nowait()
        except queue.Empty:
            return

        # device.username = username
        # device.password = password
        # device.note = note

        if isinstance(function, Command):
            Sequence(
                登录(username, password),
                我的主页(),
                function,
                登出(),
            )(device)
        else:
            function(device, username, password, note)


def run(function):
    addresses = get_device_addresses()
    accounts = get_accounts()
    threads = []
    for address in addresses:
        t = threading.Thread(target=thread, args=(address, accounts, function), daemon=True)
        t.start()
        threads.append(t)
    try:
        while threading.active_count():
            time.sleep(1)
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    run(Sequence(
        我的主页(),
        我的主页.体力(3),
        主线关卡(),
        主线关卡.扫荡('H10-1', 扫荡次数=3, 关卡数=9),
    ))
