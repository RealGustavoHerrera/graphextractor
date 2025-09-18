import argparse, sys, os
from processOutput import ProcessOutput

parser=argparse.ArgumentParser(description="Just process output without re-generating")
parser.add_argument('local_path', type=str, help="local path to the output file")
args = parser.parse_args()

po = ProcessOutput()

if os.path.isfile(args.local_path) and os.access(args.local_path, os.R_OK):
    # if exist, attempt to ingest
    print(f"processing local file...")
    po.ingestOutput(args.local_path)
    
else:
    # if not, error
    print("that file does not exist or can't be read")
    sys.exit()

print(f"done")
