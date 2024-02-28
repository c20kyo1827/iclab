import logging
import argparse
import sys
import os
import json
import subprocess

# Logging
STEPNAME = "Iclab"
logging.root.name = (STEPNAME + " executor")
logging.basicConfig(level=logging.INFO,
                format='[%(levelname)-7s] %(name)s - %(message)s',
                stream=sys.stdout)

# Argument
def parseArguments():
    parser = argparse.ArgumentParser(
        usage = "%(prog)s [options]",
        description = STEPNAME + " executor"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument("-s", "--step", type=str, choices=["RTL", "SYN", "GATE"], nargs="*", default=[], help="Choose step(s) from %(choices)s")
    parser.add_argument("-oj", "--output-json", type=str, help="Output options in JSON format to a file")
    group.add_argument("-l", "--lab", type=str, help="specify labXX")
    group.add_argument("-ij", "--input-json", type=str, help="Load options from a JSON file")

    return parser.parse_args()

if __name__=="__main__":
    args = parseArguments()

    # Parse argument
    # TODO
    # It's better to move the argument process into one class
    # TODO
    args_dict = vars(args)
    logging.info("Conver to dict : " + json.dumps(args_dict, indent=4))

    def save_options_to_json(data_dict, filename):
        with open(filename, 'w') as f:
            json.dump(data_dict, f, indent=4)

    def load_options_from_json(data_dict, filename):
        data_dict.clear()
        with open(filename, 'r') as f:
            data_json = json.load(f)
            for key, value in data_json.items():
                data_dict[key] = value
        

    if args.input_json:
        load_options_from_json(args_dict, args.input_json)
        logging.info("Loaded options from JSON : " + json.dumps(args_dict, indent=4))
    else:
        if args.output_json:
            save_options_to_json(args_dict, args.output_json)
            logging.info("Options saved to JSON file : " + args.output_json)

    logging.info("After : Parser argument from JSON : " + json.dumps(args_dict, indent=4))


    # Parse path
    # TODO
    #    1. Should consider the uppercase or lowercase "lab" name
    #    2. If there is no Exercise folder in the directory, it's need to prevent the bug
    cwd = os.getcwd()
    logging.info("Current path : " + cwd)
    lab_path = cwd + "/Lab" + args.lab + "/Exercise"
    logging.info("Lab path : " + lab_path)
    if os.path.exists(lab_path)==False:
        logging.error("Can't find the lab path : " + lab_path)
        exit(0)
    os.chdir(lab_path)
    logging.info(os.listdir(os.getcwd()))

    # Parse step
    step_set = set(args.step)
    logging.info(step_set)
    
    def run_sub_command(step_name, run_cmd):
        logging.info("Run {}...".format(step_name))
        logging.info("Current path : " + os.getcwd())
        cwd = os.getcwd()
        for folder in os.listdir(cwd):
            path = os.path.join(cwd, folder)
            if os.path.isdir(path):
                if step_name in folder:
                    os.chdir(path)
                    logging.info("Move to " + os.getcwd())
                    break
        process = subprocess.Popen(run_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode==0:
            logging.info("Run {} successfully...".format(step_name))
            # logging.info(stdout)
        else:
            logging.info("Run {} unsuccessfully...".format(step_name))
            logging.info(stderr)
        os.chdir(cwd)


    if "RTL" in step_set:
        # TODO
        # To specify which version script is we want to use
        step_name = "RTL"
        run_cmd = "./01_run_vcs_rtl"
        run_sub_command(step_name, run_cmd)
    
    if "SYN" in step_set:
        step_name = "SYN"
        run_cmd = "./01_run_dc_shell"
        run_sub_command(step_name, run_cmd)

    if "GATE" in step_set:
        step_name = "GATE"
        run_cmd = "./01_run_vcs_gate"
        run_sub_command(step_name, run_cmd)