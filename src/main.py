import pandas as pd
from extractors.focus_on_meds import ExtractorFocusOnMeds
from extractors.focus_on_trauma import ExtractorFocusOnTrauma
from extractors.general_extractor import GeneralExtractor
import argparse, sys, os
from processOutput import ProcessOutput

parser=argparse.ArgumentParser(description="Analyze clinical notes to extract structured data")
parser.add_argument('type', type=str, help='Type of extractor to use (meds | trauma | general)', choices=["meds", "trauma", "general"])
parser.add_argument('record', type=int, help='Target Record in AGBonnet (see https://huggingface.co/datasets/AGBonnet/augmented-clinical-notes)')
args = parser.parse_args()

match args.type:
    case "meds":
        extractor = ExtractorFocusOnMeds("OPENAI")
    case "trauma":
        extractor = ExtractorFocusOnTrauma("OPENAI")
    case "general":
        extractor = GeneralExtractor("OPENAI")
    case _:
        print(f"you need to specify a type of extractor (meds, trauma, general)")
        sys.exit()

print(f"using an extractor specialized on {args.type}")

local_path = 'data/agbonnet.json'
if os.path.isfile(local_path) and os.access(local_path, os.R_OK):
    # if already downloaded, load from local
    print(f"using local data...")
    df = pd.read_json(local_path)
else:
    # if not, download and store
    print(f"downloading data from HuggingFace... wait...\n")
    df = pd.read_json("hf://datasets/AGBonnet/augmented-clinical-notes/augmented_notes_30K.jsonl", lines=True)
    df.to_json('data/agbonnet.json', orient='records', indent=2)
    print(f"data downloaded. Continuing...\n")

i = args.record
input_text = df.iloc[i].full_note
print(f"using 'full_note' from record {i} as input text: \n{input_text[:80]}...")

# creating processor now, so we stop if DB is not available
po = ProcessOutput()

# now extract
extractor.setInputText(input_text)
result =  extractor.extract()

# save them
fileName = 'sample_output_' + args.type + str(args.record)
saved = extractor.saveResults(fileName)
extractor.createHTMLResults("sample_view_" + args.type + str(args.record))

# now to the database
print(f"attempt to save on database...")
po.ingestOutput(saved)

print(f"done")
