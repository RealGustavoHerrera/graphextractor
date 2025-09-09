import os, pprint, json
from random import randrange
from datetime import datetime, timezone
from random import randrange
from arango import ArangoClient
from arango.exceptions import DatabaseCreateError, CollectionCreateError
from dotenv import load_dotenv

load_dotenv()

class ProcessOutput():
    def __init__(self):
        try:
            self.arango_client = ArangoClient(hosts=os.getenv('ARANGO_HOST'))
            self.sys_db = self.arango_client.db('_system', username=os.getenv('ARANGO_USER'), password=os.getenv('ARANGO_PASSWORD'))
        except Exception as e:
            print(f"❌ Failed to initialize ArangoDB client: {e}")
            self.arango_client = None

        # Create or connect to test database
        try:
            self.sys_db.create_database(os.getenv('ARANGO_DB_NAME'))
        except DatabaseCreateError:
            print(f"📝 Database {os.getenv('ARANGO_DB_NAME')} already exists")
    
        self.db = self.arango_client.db(os.getenv('ARANGO_DB_NAME'), username=os.getenv('ARANGO_USER'), password=os.getenv('ARANGO_PASSWORD'))

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

        print(f"output processor initialized...")

    def ingestOutput(self, fileJsonl):
        # array to store the outcome
        outcome = []

        # convert fileJsonl to dictionary
        dict_file = self.load_jsonl_as_dicts(fileJsonl)

        for line in dict_file:
            graph_data = {
                'document': {
                    '_key': "",
                    'content': "",
                    'analyzed_at': datetime.now(timezone.utc).isoformat(),
                    'source': ''
                },
                'entities': [],
                'relationships': []
            }
            # add document to graph
            graph_data['document']['_key'] = line['document_id']
            graph_data['document']['content'] = line['text']

            # add entities related back to the document
            for extraction in line['extractions']:
                graph_data = self.addEntityToGraph(extraction, graph_data)

            # we now can create relationships between entities
            # addRelationshipsToGraph() 

            outcome.append(graph_data)

            # store the graph
            self.db.collection('documents').insert(graph_data['document'])

            entref = self.db.collection('entities')
            for entity in graph_data['entities']:
                entref.insert(entity)
            
            relref = self.db.collection('relationships')
            for relation in graph_data['relationships']:
                relref.insert(relation)
        
        return outcome

    def addEntityToGraph(self, extraction, graph_data):
        # TODO change this, entities should be shared across documents (no more rand unique key)
        extraction['_key'] = graph_data['document']['_key']+"_"+str(randrange(0,9999))
        relationship = {
                        '_from': f"documents/{graph_data['document']['_key']}",
                        '_to': f"entities/{extraction['_key']}",
                        'relationship_type': 'extraction',
                        'confidence': extraction['alignment_status']
                    }
        graph_data['entities'].append(extraction)
        graph_data['relationships'].append(relationship)
        return graph_data

    def addRelationshipsToGraph(self):    
        # TODO link the entities among themselves
        # this will require some unique key for entities

        pass


    def load_jsonl_as_dicts(self, file_path):
        data = []
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip():  # Skip empty lines
                    data.append(json.loads(line.strip()))
        
        return data