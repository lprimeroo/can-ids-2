## Install

Download the RenaulClio dataset and move it inside the `data/` folder.

Then, run
```sh
sh setup_interface.sh
```


## Running



## Examples

1. Randomly generate CAN data for 30 secs and dump the logfile in current directory.

```sh
python3 main.py --generate vcan0 --time 30 --dump .
```

2. Open the simulator for manual data generation.

```sh
python3 main.py --sim vcan0
```

3. Use logfile to generate traffic on the CAN bus. Useful for carrying out attacks.

```sh
python3 main.py --onbus <path_to_logfile>
```

4. Use the trained IDS by specifying the model.

```sh
python3 main.py --ids lstm
```
