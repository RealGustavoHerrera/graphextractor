import langextract as lx
from extractors.langextractor import LangExtractor
import textwrap

class ExtractorFocusOnTrauma(LangExtractor):

    def __init__(self, model):
        super().__init__(model)
        self.prompt = textwrap.dedent("""\
                        Extract patient, diagnosis and treatment information including:
                        patient age, sex, 
                        patient symptoms, patient conditions and causes, 
                        patient diagnosis, methods and outcomes
                        patient medication, dosage, frequency and duration.
                        surgical interventions or treatments
                        Focus on the relationship between symptons, conditions, medication and treatment""")
        
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
                        lx.data.Extraction(extraction_class="age", extraction_text="56 years old", attributes={"years":"56"}),
                        lx.data.Extraction(extraction_class="sex", extraction_text="man", attributes={"sex": "male"}),

                        lx.data.Extraction(extraction_class="symptoms", extraction_text="dump pain on the right back and a swelling right in this place for several weeks", 
                                            attributes={"diagnosis":"", "duration": "several weeks", "since" : "ongoing", "related_condition":"sclerosing xanthofibroma"}),

                        lx.data.Extraction(extraction_class="diagnostic_findings", extraction_text="simple fracture of the 9th right rib without any other consequences", 
                                        attributes={"method":"interview", "related_condition":"thoracic trauma at work one year ago"}),
                        lx.data.Extraction(extraction_class="diagnostic_findings", extraction_text="X-ray was seen a shadow in the lower part of the right hemithorax", 
                                        attributes={"method":"X-ray", "related_condition":"sclerosing xanthofibroma"}),
                        lx.data.Extraction(extraction_class="diagnostic_findings", extraction_text="CT-scan of the thorax that revealed a tumor of the thoracic wall in the right hemithorax that measured 8 \u00d7 4 cm and had a heterogeneous density inside of it", 
                                        attributes={"method":"CT-scan", "related_condition":"sclerosing xanthofibroma"}),
                        lx.data.Extraction(extraction_class="diagnostic_findings", extraction_text=" The tumor had involved and destructed the 9th rib and was lying even in two adjacent intercostal spaces, but without involving the lung and muscular layers", 
                                        attributes={"method":"CT-scan", "related_condition":"sclerosing xanthofibroma"}),
                        lx.data.Extraction(extraction_class="diagnostic_findings", extraction_text="CT-scan were seen micronodular infiltrations of both lungs with diameters up to 5 mm and only one nodule in lower lobe of the right lung with diameter almost 1 cm ().", 
                                        attributes={"method":"CT-scan", "related_condition":"sclerosing xanthofibroma"}),
                        lx.data.Extraction(extraction_class="diagnostic_findings", extraction_text="The mediastinum was without enlarged lymph nodes and no other lesion was seen in adjacent organs.", 
                                        attributes={"method":"CT-scan", "related_condition":"sclerosing xanthofibroma"}),
                        lx.data.Extraction(extraction_class="diagnostic_findings", extraction_text="None of these samples resulted positive (no malignant cells found) after frozen biopsy", 
                                        attributes={"method":"biopsy", "related_condition":"sclerosing xanthofibroma"}),

                        lx.data.Extraction(extraction_class="conditions", extraction_text="sclerosing xanthofibroma", 
                                        attributes={"age":"56","cause":"trauma"}),
                        
                        lx.data.Extraction(extraction_class="surgical_procedure", extraction_text="oncologic resection of the tumor of the thoracic wall.",
                                        attributes = {"part":"thoracic wall", "outcome":"very good", "related_condition":"sclerosing xanthofibroma"}),
                        lx.data.Extraction(extraction_class="surgical_procedure", extraction_text="plastic procedure with polypropylene mesh in double layers to correct the defect.",
                                        attributes = {"part":"thoracic wall", "outcome":"very good", "related_condition":"sclerosing xanthofibroma"}),
                    ],
                )
            
            
            ]
