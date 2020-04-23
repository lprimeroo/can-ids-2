import os
import subprocess
import threading

# Generate random CAN data for the purpose of the simulation
def cangen(interface, time):
    cangen_proc = subprocess.Popen(['cangen', interface])
    cangen_timer = threading.Timer(time, cangen_proc.kill)
    cangen_timer.start()
    cangen_proc.wait()


# Acts like Wireshark and takes a dump of the CAN bus
def candump(interface, time=None):
    candump_proc = subprocess.Popen(['candump', interface, '-l'])
    if time is not None:
        candump_timer = threading.Timer(time, candump_proc.kill)
        candump_timer.start()
    candump_proc.wait()


# Loads a logfile into the CAN bus
def canplayer(interface, logfile_path):
    canplayer_proc = subprocess.Popen(['canplayer',  'vcan0=%s' % interface, '-I', logfile_path])
    canplayer_proc.wait()


# Launch the ICSim Simulator
def open_sim(interface):
    icsim_proc = subprocess.Popen(['./icsim', interface])
    controller_proc = subprocess.Popen(['./controls', interface])
    icsim_proc.wait()
    controller_proc.wait()