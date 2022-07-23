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

with open(input_file, "r") as stream:
    docs = yaml.safe_load_all(stream)
    for doc in docs:
        # Ignore empty documents
        if not doc: continue
        waifus.append(Waifu(doc))

with open(config.DATA_OUTPUT, "w") as f:
    f.write("\n".join([Waifu.headers()] + [str(w) for w in waifus]))
