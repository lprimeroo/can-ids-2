import os
import subprocess
import threading


def cangen(interface, time):
    cangen_proc = subprocess.Popen(['cangen', interface])
    cangen_timer = threading.Timer(time, cangen_proc.kill)
    cangen_timer.start()
    cangen_proc.wait()


def candump(interface, time):
    candump_proc = subprocess.Popen(['candump', interface, '-l'])
    candump_timer = threading.Timer(time, candump_proc.kill)
    candump_timer.start()
    candump_proc.wait()

def open_sim(interface):
    icsim_proc = subprocess.Popen(['./icsim', interface])
    controller_proc = subprocess.Popen(['./controls', interface])
    icsim_proc.wait()
    controller_proc.wait()