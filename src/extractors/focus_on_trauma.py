import langextract as lx
from extractors.langextractor import LangExtractor
import textwrap

class ExtractorFocusOnTrauma(LangExtractor):

    def __init__(self, model):
        super().__init__(model)
        self.prompt = textwrap.dedent("""\
                        Extract patient demographics (age, sex),
                        conditions, causes and treatment,
                        medication, dosage, frequency and duration.
                        Focus on the relationship between conditions, medication and treatment""")
        
        # Sample 1 
        self.examples = [
            lx.data.ExampleData(
                    text=(
                        """This is the case of a 56-year-old man that was complaining of a dump pain on the right back and a swelling right in this place for several weeks. 
                        The patient was in good state and very active. There was not any health problem in the past except a thoracic trauma at work one year ago. 
                        In that time the patient was diagnosed with a simple fracture of the 9th right rib without any other consequences.\\n
                        On the X-ray was seen a shadow in the lower part of the right hemithorax. After that, it was decided to perform a CT-scan of the thorax that revealed a 
                        tumor of the thoracic wall in the right hemithorax that measured 8 \u00d7 4 cm and had a heterogeneous density inside of it. The tumor had involved and 
                        destructed the 9th rib and was lying even in two adjacent intercostal spaces, but without involving the lung and muscular layers. On lung window of the CT-scan 
                        were seen micronodular infiltrations of both lungs with diameters up to 5 mm and only one nodule in lower lobe of the right lung with diameter almost 1 cm (). 
                        The mediastinum was without enlarged lymph nodes and no other lesion was seen in adjacent organs. The conclusion of the radiologist was that probably this was 
                        the case of a malignant tumor of the thoracic wall with secondary lesions in both lungs and a biopsy of the tumor was recommended.\\n
                        Because there was not a correlation between the clinical picture of the patient and the conclusion of the radiology it was decided to perform frozen biopsy of the lesions of the right 
                        lung and an excision biopsy of the tumor of the thoracic wall. So, through a small posterior thoracotomy at 7th intercostal space were sampled five nodular 
                        lesions from the right lung and a sample from the tumor. None of these samples resulted positive (no malignant cells found) after frozen biopsy. In such conditions 
                        was considered as more realistic the option of performing an oncologic resection of the tumor of the thoracic wall. (We resected three ribs where the 8th and 10th 
                        ribs were macroscopically free of the tumor. The resection was extended 10 cm anteriorly from the tumor and posteriorly it was accompanied by disarticulation of the 
                        ribs and partial resection of transversal processes of 8th, 9th, and 10th vertebras.) After that, we have performed a plastic procedure with polypropylene mesh in 
                        double layers to correct the defect. The clinical course of the patient was very good and five days later he was discharged from the hospital in very good condition. 
                        The conclusion of biopsy for both the tumor of thoracic wall and the lung nodules was sclerosing xanthofibroma which is considered by most people to be a tumor with 
                        different clinical and radiological features. Lesions were characterized by a network of anastomosing bone trabeculae without osteoblast lining within a fibrous stroma ().\\n
                        Referring to the follow-up, the patient was in a great state of health and from the first month after the surgery he turned back at his work place. Two years after the 
                        surgery the thoracic CT-scan showed neither recurrences of the lesions of the thoracic wall nor new developments on the lungs.
                        """
                    ),
                    extractions=[
                        lx.data.Extraction(extraction_class="demographics", extraction_text="56 years old", attributes={"years":"56"}),
                        lx.data.Extraction(extraction_class="demographics", extraction_text="man", attributes={"sex": "male"}),

                        lx.data.Extraction(extraction_class="condition", extraction_text="sclerosing xanthofibroma", attributes={"cause":"trauma"}),

                        lx.data.Extraction(extraction_class='relationship', extraction_text="performing an oncologic resection of the tumor of the thoracic wall", 
                                           attributes={ "entity_1" : "sclerosing xanthofibroma", "entity_2" : "oncologic resection of the tumor"}),
                        lx.data.Extraction(extraction_class='relationship', extraction_text="After that, we have performed a plastic procedure with polypropylene mesh in double layers to correct the defect", 
                                           attributes={ "entity_1" : "sclerosing xanthofibroma", "entity_2" : "plastic procedure"}),
                        
                        lx.data.Extraction(extraction_class="treatment", extraction_text="oncologic resection of the tumor",
                                        attributes = {"type":"surgical procedure", "part":"thoracic wall", "outcome":"very good", "related_condition":"sclerosing xanthofibroma"}),
                        lx.data.Extraction(extraction_class="treatment", extraction_text="plastic procedure",
                                        attributes = {"type":"surgical procedure", "part":"thoracic wall", "outcome":"very good", "related_condition":"sclerosing xanthofibroma"}),
                    ],
                )
            ]

    def getExamples(self):
        return self.examples