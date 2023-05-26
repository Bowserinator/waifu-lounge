import argparse
import yaml

import config
from waifu import Waifu

# Setup argparse
parser = argparse.ArgumentParser(description='Generate JSON output for frontend + download images.')
parser.add_argument('--input', type=str, nargs=1, required=True,
                    help='Input waifu yaml file')
args = parser.parse_args()

# Read args
input_file = args.input[0]
waifus = []
names = set()

with open(input_file, "r") as stream:
    docs = yaml.safe_load_all(stream)
    for doc in docs:
        # Ignore empty documents
        if not doc: continue
        waifus.append(Waifu(doc))

        # Test for duplicates
        name = waifus[-1].name.split("(")[0].lower().strip()
        if name in names or (" " in name and name.split(" ", 1)[1] + " " + name.split(" ", 1)[0] in names):
            print("[WARNING] Duplicate waifu name", name, waifus[-1].name)

        names.add(name)

with open(config.DATA_OUTPUT, "w") as f:
    f.write("\n".join([Waifu.headers()] + [str(w) for w in waifus]))
