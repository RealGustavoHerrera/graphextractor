import langextract as lx

focus_on_trauma = lx.data.ExampleData(
        text=(
            """
            """
        ),
        extractions=[
            lx.data.Extraction(extraction_class="age", extraction_text="XX years old", attributes={"years":"xx"}),
            lx.data.Extraction(extraction_class="sex", extraction_text="man, male, female, girl, lady, gentleman", attributes={"sex": "male | female"}),

            lx.data.Extraction(extraction_class="symptoms", extraction_text="", 
                                attributes={"diagnosis":"", "duration": "", "since" : "", "related_condition":""}),

            lx.data.Extraction(extraction_class="conditions", extraction_text="", 
                               attributes={"age":"","cause":"", "concurrent_medications":["", ""], "prescribed_medication":""}),
            
            lx.data.Extraction(extraction_class="medication", extraction_text="", 
                                attributes = {"dosis":"", "frequency":"","duration": "", "age": "",
                                "related_condition":""}),
        ],
    )
