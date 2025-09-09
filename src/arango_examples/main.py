import os
from dotenv import load_dotenv
from google.cloud import language_v1
from arango import ArangoClient
from arango.exceptions import DatabaseCreateError, CollectionCreateError
from datetime import datetime, timezone
from random import randrange

load_dotenv()

class DocumentGraphExtractor:
    def __init__(self):
        # Initialize Google Language client
        try:
            self.language_client = language_v1.LanguageServiceClient()
        except Exception as e:
            print(f"❌ Failed to initialize Google Language client: {e}")
            self.language_client = None

        # Initialize ArangoDB client
        try:
            self.arango_client = ArangoClient(hosts=os.getenv('ARANGO_HOST'))
            self.sys_db = self.arango_client.db('_system', username=os.getenv('ARANGO_USER'), password=os.getenv('ARANGO_PASSWORD'))
        except Exception as e:
            print(f"❌ Failed to initialize ArangoDB client: {e}")
            self.arango_client = None

        # Create or connect to test database
        try:
            self.sys_db.create_database(os.getenv('ARANGO_DB_NAME'))
        except DatabaseCreateError as e:
            print(f"📝 Database {os.getenv('ARANGO_DB_NAME')} already exists")
    
        self.db = self.arango_client.db(os.getenv('ARANGO_DB_NAME'), username=os.getenv('ARANGO_USER'), password=os.getenv('ARANGO_PASSWORD'))

        if self.language_client and self.arango_client:
            print(f"📝 DocumentGraphExtractor initialized")
    
    def analyze_document(self, document_text, doc_id):
        if not self.language_client:
            return False
        
        print(f"📝 analizing doc {doc_id}")

        graph_data = {
            'document': {
                '_key': doc_id,
                'content': document_text.strip(),
                'analyzed_at': datetime.now(timezone.utc).isoformat(),
                'source': 'test'
            },
            'entities': [],
            'relationships': []
        }
        
        try:
            document = language_v1.Document(
                    content=document_text,
                    type_=language_v1.Document.Type.PLAIN_TEXT
                )
            
            # Extract entities
            entities_response = self.language_client.analyze_entities(
                request={"document": document}
            )

            print(f"✅ entities extracted: {len(entities_response.entities)}")

            for entity in entities_response.entities:
                entity_data = {
                    '_key': doc_id+"_"+entity.name.lower().replace(' ', '_').replace('.', ''),
                    'name': entity.name,
                    'type': entity.type_.name.lower(),
                    'salience': entity.salience,
                    'mentions': len(entity.mentions)
                }
                graph_data['entities'].append(entity_data)

                # Create relationship with the document
                relationship = {
                    '_from': f"documents/{graph_data['document']['_key']}",
                    '_to': f"entities/{entity_data['_key']}",
                    'relationship_type': 'mentions',
                    'confidence': entity.salience
                }
                graph_data['relationships'].append(relationship)

            print(f"✅ Graph data created")
            return graph_data
        
        except Exception as e:
            print(f"❌ Failed to analyze document: {e}")
            return None
    
    def store_graph(self, graph_data):
        # Store in ArangoDB
        if not self.db:
            return False
        
        print(f"📝 storing the graph in the database")

        # Create collections in the database
        collections_to_create = [
            ('documents', False),  # Document collection
            ('entities', False),   # Another document collection
            ('relationships', True)  # Edge collection for relationships
        ]
        for coll_name, is_edge in collections_to_create:
            try:
                self.db.create_collection(coll_name, edge=is_edge)
            except CollectionCreateError:
                print(f"📝 Collection {coll_name} already exists")

        # store the graph
        self.db.collection('documents').insert(graph_data['document'])

        entref = self.db.collection('entities')
        for entity in graph_data['entities']:
            entref.insert(entity)
        
        relref = self.db.collection('relationships')
        for relation in graph_data['relationships']:
            relref.insert(relation)
        return

if __name__ == "__main__":
    extractor = DocumentGraphExtractor()

    with open('example.txt', 'r') as file:
        sample_text = file.read()

    graph_data = extractor.analyze_document(sample_text, str(randrange(0,9999)))

    extractor.store_graph(graph_data=graph_data)

    print(f"✅ DONE. Go to ArangoDB to check the results (http://localhost:8529)")
