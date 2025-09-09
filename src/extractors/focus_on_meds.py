import langextract as lx
from extractors.langextractor import LangExtractor
import textwrap

class ExtractorFocusOnMeds(LangExtractor):

    def __init__(self, model):
        super().__init__(model)
        self.prompt = textwrap.dedent("""\
                        Extract patient, diagnosis and medication information including:
                        patient age, sex, 
                        patient symptoms, patient conditions and causes, 
                        patient medication, dosage, frequency and duration.
                        Focus on the relationship between symptons, conditions and medication""")
        
        # Sample 0 
        self.examples = [
            lx.data.ExampleData(
                    text=(
                        """A a sixteen year-old girl, presented to our Outpatient department with the complaints of discomfort in the neck and lower back as well as restriction of body movements. 
                        She was not able to maintain an erect posture and would tend to fall on either side while standing up from a sitting position. She would keep her head turned to the right 
                        and upwards due to the sustained contraction of the neck muscles. There was a sideways bending of the back in the lumbar region. To counter the abnormal positioning of the 
                        back and neck, she would keep her limbs in a specific position to allow her body weight to be supported. Due to the restrictions with the body movements at the neck and in the 
                        lumbar region, she would require assistance in standing and walking. She would require her parents to help her with daily chores, including all activities of self-care.
                        \\nShe had been experiencing these difficulties for the past four months since when she was introduced to olanzapine tablets for the control of her exacerbated mental illness. 
                        This was not her first experience with this drug over the past seven years since she had been diagnosed with bipolar affective disorder. 
                        Her first episode of the affective disorder was that of mania at the age of eleven which was managed with the use of olanzapine tablets in 2.5\u201310 mg doses per day at 
                        different times. The patient developed pain and discomfort in her neck within the second week of being put on tablet olanzapine at a dose of 5 mg per day. 
                        This was associated with a sustained and abnormal contraction of the neck muscles that would pull her head to the right in an upward direction. These features had persisted 
                        for the first three years of her illness with a varying intensity, distress, and dysfunction which would tend to correlate with the dose of olanzapine. Apart from a brief 
                        period of around three weeks when she was given tablet trihexyphenidyl 4 mg per day for rigidity in her upper limbs, she was not prescribed any other psychotropic medication. 
                        The rigidity showed good response to this medication which was subsequently stopped. The introduction and subsequent withdrawal of this medication did not bring about any 
                        change in the sustained abnormal contraction of her neck muscles.\\nImprovement and subsequent remission of the mood symptoms of the patient provided the treatment team 
                        with an opportunity to stop olanzapine. The discomfort in the neck and the abnormal movement of the neck muscles persisted over the next three months\u2019 period when she was 
                        off olanzapine without any significant change, even with a trial of propranolol, trihexyphenidyl, and phenargan injection. 
                        Reintroduction of olanzapine (at a dose of 2.5 mg per day) after a gap of three months for the reemergence of some behavioral features led to a slight aggravation of the already 
                        existing abnormal movement and posturing of the neck.\\nWith improvement in the clinical picture, olanzapine was reduced and stopped. 
                        She was put on tablet sodium valproate, 1000 mg per day during this period for the stabilization of her mood when she was also given escitalopram for a period of three months for 
                        her depressive features. The patient responded well to this change in medication, but she developed amenorrhea for which no cause was established after a detailed gynecological 
                        evaluation. Keeping in mind the possibility of valproate-induced menstrual disturbance, she was shifted to tablet lithium 450 mg per day. The patient was well maintained on this 
                        medication for a period of around two years. However, she developed hypothyroidism for which eltroxin was introduced at a dose of 50 micrograms per day.\\nDuring this period of 
                        two years and seven months, the abnormal contraction of the neck muscles and the abnormal positioning of the head improved slightly, and with the improvement, it would cause less 
                        discomfort and interference in her activities. However, these movements failed to disappear completely. Another exacerbation of the mood symptoms in the form of mania warranted 
                        a need for the introduction of olanzapine (by a different treatment team) and the patient was reintroduced to 10 mg olanzapine on a daily basis, which led to the current presentation 
                        as described earlier.
                        
                        \\nAfter the case was seen at our institute, the psychotropic medications were stopped as her mood symptoms had remitted and she was put on tablet 
                        tetrabenazine (built up to 75 mg per day in divided doses) with which the patient had started showing some response with an improvement in abnormal movements of the muscles of the 
                        neck as well as the back. She is now able to stand with support and can do some daily chores on her own. The pain and discomfort in the back and neck have also reduced.
                        \\nDuring the course of the illness, the patient has been investigated for the presence of any neurological illness as the cause of her abnormal movements. 
                        Her MRI scan of the brain, serum and urine copper levels, slit lamp microscopy for the KF ring, complete blood count, TLC, DLC, and USG of the abdomen did not reveal any 
                        abnormalities. Her thyroid function tests were deranged subsequent to the introduction of tablet lithium carbonate which was restored to normal after the introduction of 
                        tablet eltroxin.\\nDystonia is a syndrome of sustained muscle contractions that produce twisting and repetitive movements or abnormal postures. The descriptions of the extent 
                        and severity of muscle involvement are variable, ranging from intermittent contraction limited to a single body region, to generalized dystonia involving the limbs and axial 
                        muscles.\\nEver since the introduction of the term, \u201cdystonia\u201d by Oppenhiem in the early part of the twentieth century, it has been an area of focused attention of 
                        the neurologists. In 1973, Keegan and Rajput introduced the term, \u201c\u201d to describe drug-induced, sustained muscle spasm causing repetitive movements or abnormal p
                        ostures. \u201c\u201d was a term introduced by Burke in 1982, the description of which required the presence of chronic dystonia, a history of antipsychotic drug treatment 
                        preceding or concurrent with the onset of dystonia, the exclusion of known causes of secondary dystonia by appropriate clinical and laboratory evaluation, and a negative 
                        family history of dystonia for definitive diagnosis.\\nThe dystonia could be classified based on the region(s) of the body involved. Involvement of isolated regions like the face, 
                        neck, and arms would be labeled as focal dystonia, whereas simultaneous involvement of two or more contiguous areas would be called segmental dystonia. When the clinical picture 
                        is that of involvement of two or more noncontiguous regions, the label used is, \u201cmultifocal\u201d and the involvement of one leg and one other body region makes it the 
                        generalized type.\\nThe symptoms of tardive dystonia could begin even after a few days or weeks of exposure to the offending agent. Tardive dystonia is prevalent in 0.5\u201321.6% of 
                        the patients who are treated with neuroleptics.\\nThe syndrome of tardive dystonia has been reported with most of the typical antipsychotics.[] It has been associated with the 
                        atypical antipsychotics, namely risperidone, olanzapine, quetiapine, and aripiprazole. Reports of tardive dystonia developing with the use of atypical antipsychotics have been 
                        predominantly in the cases of nonaffective psychosis and in the adult population in the age ranges of the midthirties and forties. Our case is the first case of an affective illness 
                        in an adolescent girl developing tardive dystonia on olanzapine. The aggravation of the clinical features with the inadvertent reintroduction of the medication suggests olanzapine 
                        is the offending agent. With the growing acceptance of olanzapine as the first-line therapy for the manic phase of bipolar illness and as a mood stabilizer for the maintenance 
                        therapy, one needs to be cautious about the emergence of this troublesome adverse effect of this therapy. The patient has shown some response to the introduction of tetrabenazine."""
                    ),
                    extractions=[
                        lx.data.Extraction(extraction_class="age", extraction_text="16 years old", attributes={"years":"16"}),
                        lx.data.Extraction(extraction_class="sex", extraction_text="girl", attributes={"sex": "female"}),


                        lx.data.Extraction(extraction_class="symptoms", extraction_text="Her first episode of the affective disorder was that of mania at the age of eleven", 
                                        attributes={"diagnosis":"mania", "duration": "past six years", "since" : "11 years old", "related_condition":"bipolar affective disorder"}),
                        lx.data.Extraction(extraction_class="symptoms", extraction_text="for her depressive features", 
                                        attributes={"diagnosis":"depression", "duration": "past six years", "since" : "11 years old", "related_condition":"bipolar affective disorder"}),
                        lx.data.Extraction(extraction_class="symptoms", extraction_text="sustained and abnormal contraction of the neck muscles", 
                                        attributes={"diagnosis":"unspecified", "duration": "first three years", "since" : "11 years old", "related_condition":"rigidity in her upper limbs"}),
                        lx.data.Extraction(extraction_class="symptoms", extraction_text="discomfort in the neck and lower back as well as restriction of body movements", 
                                        attributes={"diagnosis":"unspecified", "duration": "past four months", "since" : "when she was introduced to olanzapine tablets", "related_condition" : "tardive dystonia"}),
                        lx.data.Extraction(extraction_class="symptoms", extraction_text="not able to maintain an erect posture and would tend to fall on either side while standing up from a sitting position", 
                                        attributes={"diagnosis":"unspecified", "duration": "past four months", "since" : "when she was introduced to olanzapine tablets", "related_condition" : "tardive dystonia"}),
                        lx.data.Extraction(extraction_class="symptoms", extraction_text="keep her head turned to the right and upwards due to the sustained contraction of the neck muscles", 
                                        attributes={"diagnosis":"unspecified", "duration": "past four months", "since" : "when she was introduced to olanzapine tablets", "related_condition" : "tardive dystonia"}),
                        lx.data.Extraction(extraction_class="symptoms", extraction_text="sideways bending of the back in the lumbar region", 
                                        attributes={"diagnosis":"unspecified", "duration": "past four months", "since" : "when she was introduced to olanzapine tablets", "related_condition" : "tardive dystonia"}),

                        lx.data.Extraction(extraction_class="conditions", extraction_text="bipolar affective disorder", attributes={"cause":"unspecified", "age" : "11 years old"}),
                        lx.data.Extraction(extraction_class="conditions", extraction_text="rigidity in her upper limbs", attributes={"cause":"unspecified", "age" : "11 years old"}),
                        lx.data.Extraction(extraction_class="conditions", extraction_text="amenorrhea", attributes={ "age": "14 years old", "cause" : "sodium valproate", "concurrent medications" :[ "sodium valproate", "escitalopram"], "prescribed_medication":["discontinue sodium valproate", "lithium"]}),
                        lx.data.Extraction(extraction_class="conditions", extraction_text="hypothyroidism", attributes={"age":"14 years old","cause":"unspecified", "concurrent_medications":["lithium", "escitalopram"], "prescribed_medication":"eltroxin"}),
                        lx.data.Extraction(extraction_class="conditions", extraction_text="tardive dystonia", attributes={"cause":"olanzapine", "age":"16 years old"}),

                        lx.data.Extraction(extraction_class="medication", extraction_text="olanzapine", 
                                        attributes = {"dosis":"2.5 mg per dose", "frequency":"per day", "age": "11 years old",
                                                        "related_condition":"bipolar affective disorder"}),
                        lx.data.Extraction(extraction_class="medication", extraction_text="trihexyphenidyl", 
                                        attributes = {"dosis":"4mg", "frequency":"per day", "duration" : "three weeks", "age" : "14 years old",
                                                        "related_condition":"rigidity in her upper limbs"}),
                        lx.data.Extraction(extraction_class="medication", extraction_text="sodium valproate", 
                                        attributes = {"dosis":", 1000 mg", "frequency":"per day","duration": "three months", "age": "14 years old",
                                        "related_condition":"bipolar affective disorder"}),
                        lx.data.Extraction(extraction_class="medication", extraction_text="escitalopram", 
                                        attributes = {"duration" : "three months",
                                        "related_condition":"bipolar affective disorder"}),
                        lx.data.Extraction(extraction_class="medication", extraction_text="lithium", 
                                        attributes={"dosis" : "450 mg per day", "duration": "two years",
                                        "related_condition":"bipolar affective disorder"}),
                        lx.data.Extraction(extraction_class="medication", extraction_text="eltroxin", 
                                        attributes={"dosis": "50 micrograms per day",
                                        "related_condition":"hypothyroidism"}),
                        lx.data.Extraction(extraction_class="medication", extraction_text="olanzapine", 
                                        attributes={ "age":"14 years old", "dosis":"10mg", "frequency":"per day",
                                        "related_condition":"bipolar affective disorder"}),
                        lx.data.Extraction(extraction_class="medication", extraction_text="existing psychotropic medications stopped", 
                                        attributes = {"age":"16 years old",
                                        "related_condition":"bipolar affective disorder"}),
                        lx.data.Extraction(extraction_class="medication", extraction_text="tetrabenazine", 
                                        attributes = {"age":"16 years old","dosis":"75 mg", "frequency":"per day divided in doses", "duration":"unspecified",
                                        "related_condition":"bipolar affective disorder"}),
                    ],
                ),
            ]