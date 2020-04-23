## Install

Download the RenaultClio dataset and move it inside the `data/` folder.

```
sudo apt-get install libsdl2-dev libsdl2-image-dev -y
sudo apt-get install can-utils -y
pip3 install -r requirements.txt
pip3 install --user --upgrade tensorflow
```

Then, run
```sh
sh setup_interface.sh
```


Also, Wireshark always needs to be run as a `sudo` user.

## Examples

1. Randomly generate CAN data for 30 secs and dump the logfile in current directory.

```sh
python3 main.py --generate vcan0 --time 30 --dump .
```

2. Open the simulator for manual data generation. Use Wireshark to read the data.

```sh
python3 main.py --sim vcan0
```

3. Use logfile to generate traffic on the CAN bus. Useful for carrying out attacks.

```sh
python3 main.py --attack <path_to_logfile>
```

4. Use the trained IDS by specifying the model.

```sh
python3 main.py --ids lstm
```
