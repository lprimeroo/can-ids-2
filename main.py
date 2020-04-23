import subprocess
from multiprocessing import Process
from argparse import ArgumentParser
from can_utils import cangen, candump, open_sim, canplayer
from ids import detect

# This is a handler function for running candump and cangen in different processes
def can_generate_handler(args):
    interface = args.generate
    time = int(args.time)
    if args.dump is not None:
        dump_proc = Process(target=candump, args=(interface, time + 2)) # added extra 2 secs as buffer
        dump_proc.start()
    gen_proc = Process(target=cangen, args=(interface, time)) # call cangen API from can-utils
    gen_proc.start()
    if args.dump is not None:
        dump_proc.join()
    gen_proc.join()


if __name__ == "__main__":
    # Handle parsing of all the command-line flags
    parser = ArgumentParser(prog='python3 main.py')
    parser.add_argument('--generate', metavar='[INTERFACE]', help='determine the interface on which random CAN data should be generated')
    parser.add_argument('--time', metavar='[TIME_LIMIT]', help='specify for how long the generation should be run (in secs)')
    parser.add_argument('--dump', metavar='[DIRECTORY]', help='specify the directory to dump the logfile in')
    parser.add_argument('--sim', metavar='[INTERFACE]', help='open the simulator for manual generation of CAN data')
    parser.add_argument('--attack', metavar='[ATTACK_LOG_FILE_PATH]', nargs='*', help='determine the attack to be simulated using the appropriate logfile')
    parser.add_argument('--ids', metavar='[MODEL_TYPE]', help='determine the IDS type to be used')
    args = parser.parse_args()

    # The network interface and time limit should always be specified together
    if args.generate is not None and args.time is not None:
        can_generate_handler(args)


    # Opens the simulator on the specified interface for manual generation of CAN data
    if args.sim is not None:
        interface = args.sim
        open_sim(interface)

    # # Carry out the appropriate attack using the logs
    if args.attack is not None:
        canplayer(args.attack[0], args.attack[1]) # takes the logfile as the parameter

    # # Use the specified IDS on logs
    if args.ids is not None:
        detect(args.ids)
        
    print(args)