from dotenv import load_dotenv
import langextract as lx
import os
import textwrap

load_dotenv()

class LangExtractor():

    def __init__(self, model):
        match model:
            case 'GEMINI':
                print('creating a GEMINI instance')
                key = os.getenv('LANGEXTRACT_API_KEY')
                if not key:
                    print('LANGEXTRACT_API_KEY not set')
                    return False
                self.model = model
                

            case 'OPENAI':
                print('creating an OPENAI instance')
                key = os.getenv('OPENAI_API_KEY')
                if not key:
                    print('OPENAI_API_KEY not set')
                    return False
                self.model = model

            case _:
                print('model must be one of `GEMINI` or `OPENAI`')
                return False

    def setPrompt(self, prompt):
        self.prompt = textwrap.dedent(prompt)
    
    def setInputText(self, inputText):
        self.input_text = inputText

    def setExamples(self, examples):
        self.examples = examples
    
    def extract(self):
        if not self.prompt or not self.input_text or not self.examples:
            print(f"We need prompt, input text and examples to do an extraction")
            return False
        
        if self.model == 'GEMINI':
            self.result = lx.extract(
                text_or_documents=self.input_text,
                prompt_description=self.prompt,
                examples= self.examples,
                model_id="gemini-2.5-pro"
            )
        elif self.model == 'OPENAI':
            self.result = lx.extract(
                text_or_documents=self.input_text,
                prompt_description=self.prompt,
                examples=self.examples,
                model_id="gpt-4o",  # Automatically selects OpenAI provider
                api_key=os.environ.get('OPENAI_API_KEY'),
                fence_output=True,
                use_schema_constraints=False
            )
        else:
            print(f"Some error has occurred. the model -- {self.model} -- is invalid")
            return False
        
        return self.result

    def displayEntitiesWithPosition(self):
        # Display entities with positions
        print(f"Entities with position: \n")
        print(f"Input: {self.input_text}\n")
        print("Extracted entities:")
        for entity in self.result.extractions:
            position_info = ""
            if entity.char_interval:
                start, end = entity.char_interval.start_pos, entity.char_interval.end_pos
                position_info = f" (pos: {start}-{end})"
            print(f"• {entity.extraction_class.capitalize()}: {entity.extraction_text}{position_info}")

    def saveResults(self, fileName):
        lx.io.save_annotated_documents([self.result], output_name=f"{fileName}.jsonl")
        print(f"Results saved to test_output/{fileName}.jsonl")
        return f"test_output/{fileName}.jsonl"

    def createHTMLResults(self, fileName):
        # Generate the interactive visualization from the file
        html_content = lx.visualize(self.result)
        with open(f"test_output/{fileName}.html", "w") as f:
            f.write(html_content)
        print(f"html visualization saved to test_output/{fileName}.html")
        return f"test_output/{fileName}.html"