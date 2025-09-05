import os
from dotenv import load_dotenv
from google.cloud import language_v1
from datetime import datetime, timezone

load_dotenv()

class GoogleLanguageTester:
    def __init__(self):
        """Initialize Google Cloud Language client"""
        try:
            credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
            if credentials_path and os.path.exists(credentials_path):
                print(f"✅ Using credentials from: {credentials_path}")
                self.client = language_v1.LanguageServiceClient()
            else:
                print("❌ GOOGLE_APPLICATION_CREDENTIALS not set or file not found")
                print("Please set the environment variable to your service account JSON file")
                return None
                
        except Exception as e:
            print(f"❌ Failed to initialize Google Language client: {e}")
            self.client = None

    def test_connection(self):
        """Test basic connection to Google Cloud Language API"""
        if not self.client:
            return False
            
        try:
            # Simple test with a basic sentence
            test_text = "Hello, Google Cloud Language API!"
            document = language_v1.Document(
                content=test_text,
                type_=language_v1.Document.Type.PLAIN_TEXT
            )
            
            # Test sentiment analysis (simplest API call)
            response = self.client.analyze_sentiment(
                request={"document": document}
            )
            
            print(f"✅ API connection successful!")
            print(f"✅ Test sentiment score: {response.document_sentiment.score:.2f}")
            return True
            
        except Exception as e:
            print(f"❌ API connection failed: {e}")
            return False

    def analyze_sample_document(self):
        """Analyze a sample document"""
        if not self.client:
            return
        
        sample_text_1 = """
        Apple Inc. is a technology company headquartered in Cupertino, California. 
        The company was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in 1976. 
        Apple is known for innovative products like the iPhone, iPad, and MacBook. 
        The company's CEO Tim Cook announced record quarterly earnings yesterday, 
        showing strong growth in both hardware and services revenue. 
        Apple's stock price rose 5% following the announcement.
        """
        
        document = language_v1.Document(
            content=sample_text_1,
            type_=language_v1.Document.Type.PLAIN_TEXT
        )
        
        print("\n" + "="*60)
        print("📄 ANALYZING SAMPLE DOCUMENT")
        print("="*60)
        print(f"Text: {sample_text_1.strip()}")
        print("\n")
        
        # 1. Sentiment Analysis
        print("1️⃣ SENTIMENT ANALYSIS")
        print("-" * 30)
        try:
            sentiment_response = self.client.analyze_sentiment(
                request={"document": document}
            )
            
            sentiment = sentiment_response.document_sentiment
            print(f"✅ Overall sentiment score: {sentiment.score:.2f} (range: -1.0 to 1.0)")
            print(f"✅ Magnitude: {sentiment.magnitude:.2f} (strength of emotion)")
            
            # Interpret sentiment
            if sentiment.score > 0.25:
                interpretation = "Positive 😊"
            elif sentiment.score < -0.25:
                interpretation = "Negative 😞"
            else:
                interpretation = "Neutral 😐"
            print(f"✅ Interpretation: {interpretation}")
            
        except Exception as e:
            print(f"❌ Sentiment analysis failed: {e}")

        # 2. Entity Recognition
        print(f"\n2️⃣ ENTITY RECOGNITION")
        print("-" * 30)
        try:
            entities_response = self.client.analyze_entities(
                request={"document": document}
            )
            
            entities = entities_response.entities
            print(f"✅ Found {len(entities)} entities:")
            
            for entity in entities:
                entity_type = entity.type_.name
                print(f"   🏷️  {entity.name} ({entity_type}) - Salience: {entity.salience:.3f}")
                
                # Show mentions (where in text this entity appears)
                if entity.mentions:
                    for mention in entity.mentions:
                        mention_type = mention.type_.name
                        print(f"      📍 Mention: '{mention.text.content}' ({mention_type})")
                        
        except Exception as e:
            print(f"❌ Entity recognition failed: {e}")

        # 3. Syntax Analysis
        print(f"\n3️⃣ SYNTAX ANALYSIS")
        print("-" * 30)
        try:
            syntax_response = self.client.analyze_syntax(
                request={"document": document}
            )
            
            tokens = syntax_response.tokens
            print(f"✅ Found {len(tokens)} tokens:")
            
            # Show first 10 tokens with their parts of speech
            for i, token in enumerate(tokens[:10]):
                content = token.text.content
                lemma = token.lemma
                pos = token.part_of_speech.tag
                print(f"   🔤 '{content}' -> {lemma} ({pos})")
            
            if len(tokens) > 10:
                print(f"   ... and {len(tokens) - 10} more tokens")
                
        except Exception as e:
            print(f"❌ Syntax analysis failed: {e}")

        # 4. Classification (if available)
        print(f"\n4️⃣ CONTENT CLASSIFICATION")
        print("-" * 30)
        try:
            classification_response = self.client.classify_text(
                request={"document": document}
            )
            
            categories = classification_response.categories
            if categories:
                print(f"✅ Found {len(categories)} categories:")
                for category in categories:
                    print(f"   📂 {category.name} (confidence: {category.confidence:.3f})")
            else:
                print("📝 No categories found (text might be too short)")
                
        except Exception as e:
            print(f"⚠️  Classification not available: {e}")

    def extract_graph_data(self):
        """Extract data in a format suitable for graph storage"""
        if not self.client:
            return None
        
        sample_text_2 = """
        Microsoft Corporation announced its quarterly earnings today. 
        CEO Satya Nadella highlighted strong performance in Azure cloud services. 
        The company's headquarters in Redmond, Washington saw increased activity 
        as engineers worked on new AI features for Office 365.
        """
        
        document = language_v1.Document(
            content=sample_text_2,
            type_=language_v1.Document.Type.PLAIN_TEXT
        )
        
        print("\n" + "="*60)
        print("🕸️  EXTRACTING GRAPH DATA")
        print("="*60)
        
        graph_data = {
            'document': {
                '_key': 'sample_doc_1',
                'content': sample_text_2.strip(),
                'analyzed_at': datetime.now(timezone.utc).isoformat(),
                'source': 'test'
            },
            'entities': [],
            'relationships': []
        }
        
        try:
            # Get entities
            entities_response = self.client.analyze_entities(
                request={"document": document}
            )
            
            print("🏷️  Entities extracted:")
            for entity in entities_response.entities:
                entity_data = {
                    '_key': entity.name.lower().replace(' ', '_').replace('.', ''),
                    'name': entity.name,
                    'type': entity.type_.name.lower(),
                    'salience': entity.salience,
                    'mentions': len(entity.mentions)
                }
                graph_data['entities'].append(entity_data)
                
                # Create relationship
                relationship = {
                    '_from': f"documents/{graph_data['document']['_key']}",
                    '_to': f"entities/{entity_data['_key']}",
                    'relationship_type': 'mentions',
                    'confidence': entity.salience
                }
                graph_data['relationships'].append(relationship)
                
                print(f"   ✅ {entity.name} ({entity.type_.name}) - salience: {entity.salience:.3f}")
            
            print(f"\n📊 Graph data structure:")
            print(f"   • 1 document")
            print(f"   • {len(graph_data['entities'])} entities")  
            print(f"   • {len(graph_data['relationships'])} relationships")
            
            return graph_data
            
        except Exception as e:
            print(f"❌ Graph extraction failed: {e}")
            return None

def main():
    print("🧪 Testing Google Cloud Language API")
    print("=" * 50)
    
    # Check environment
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not creds_path:
        print("❌ GOOGLE_APPLICATION_CREDENTIALS environment variable not set!")
        print("Please add this to your .env file:")
        print("GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json")
        return
    
    tester = GoogleLanguageTester()
    
    if not tester.test_connection():
        return
    
    # Run all tests
    tester.analyze_sample_document()
    
    graph_data = tester.extract_graph_data()
    
    if graph_data:
        print(f"\n🎉 All tests completed successfully!")
    else:
        print(f"\n⚠️  Some tests failed")

if __name__ == "__main__":
    main()