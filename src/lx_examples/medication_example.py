import langextract as lx
import pprint
from extractors.langextractor import LangExtractor

extractor = LangExtractor('OPENAI')

extractor.setPrompt("""\
                    Extract medication information including medication name, dosage, 
                    route, frequency, and duration in the order they appear in the text.""")

extractor.setInputText("Patient took 400 mg PO Ibuprofen q4h for two days.")

extractor.setExamples(
    [
        lx.data.ExampleData(
            text=(
                "Patient was given 250 mg IV Cefazolin TID for one week"
            ),
            extractions=[
                lx.data.Extraction(extraction_class="dosage", extraction_text="250 mg"),
                lx.data.Extraction(extraction_class="route", extraction_text="IV"),
                lx.data.Extraction(extraction_class="medication", extraction_text="Cefazolin"),
                lx.data.Extraction(extraction_class="frequency", extraction_text="TID"),  # TID = three times a day
                lx.data.Extraction(extraction_class="duration", extraction_text="for one week")
            ],
        )
    ]
)

result = extractor.extract()
pprint.pprint(result)

extractor.displayEntitiesWithPosition()

outputfile = extractor.saveResults('sample_output')
print(f"output saved at test_output/{outputfile}")

viewfile = extractor.createHTMLResults('sample_view')
print(f"view available at {viewfile}")

print(f"done")