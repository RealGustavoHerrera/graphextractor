import os, pprint, json
from random import randrange
from datetime import datetime, timezone
from random import randrange
from arango import ArangoClient
from arango.exceptions import DatabaseCreateError, CollectionCreateError
from dotenv import load_dotenv

load_dotenv()
known_classes = ["medication", "diagnosis", "condition", "treatment"]

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

        print(f"DB ready to receive data...")

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

            print(f"processing document {graph_data['document']['_key']}")

            # add entities related back to the document
            for extraction in line['extractions']:
                graph_data = self.addEntityToGraph(extraction, graph_data)

                # we now can create relationships between entities
                if extraction['extraction_class'] == 'relationship':
                    graph_data = self.addRelationshipsToGraph(extraction, graph_data) 

            outcome.append(graph_data)

            #  Store the graph

            ## Store the document (safe if processed twice)
            self.db.collection('documents').insert(graph_data['document'], overwrite=True)

            ## Store the entities (safe if already exist in the db)
            if(graph_data['entities']):
                aql = '''
                FOR entity IN @entities
                    UPSERT { _key: entity._key }
                    INSERT entity
                    UPDATE entity
                    IN entities
                '''
                self.db.aql.execute(aql, bind_vars={'entities': graph_data['entities']})

            ## Store the relationships (safe if already exist in the db)
            if(graph_data['relationships']):
                aql = '''
                FOR relationship IN @relationships
                    UPSERT {_key: relationship._key }
                    INSERT MERGE (relationship, {count: 1})
                    UPDATE ({ count: OLD.count + 1 })
                    IN relationships
                '''
                self.db.aql.execute(aql, bind_vars={'relationships': graph_data['relationships']})
            
        return outcome

    def addEntityToGraph(self, extraction, graph_data):
        if extraction['extraction_class'] == 'relationship':
            # this is a relationship not an entity. Do nothing.
            return graph_data
        
        if extraction['extraction_class'] in known_classes:
            # if the class is known (ie. "medication", "diagnosis", "condition", "treatment") the key is the extraction_text
            extraction['_key'] = extraction["extraction_text"].lower().replace(" ","_")
            
        else:
            # otherwise, it's a unique entity (ie symptoms, other)
            # TODO do demographics
            extraction['_key'] = extraction["extraction_class"]+"_"+str(randrange(0,9999))        
            
        if any(entity['_key'] == extraction['_key'] for entity in graph_data['entities']):
            print(f"found entity {extraction['_key']} duplicated, skipping insertion of entity")
            return graph_data

        print(f"inserting entity {extraction['_key']} with rel to document {graph_data['document']['_key']}")

        # Insert relationship entity - document
        ent_rel_doc = {
                        '_from': f"documents/{graph_data['document']['_key']}",
                        '_to': f"entities/{extraction['_key']}",
                        'relationship_type': 'extraction',
                        'char_interval': extraction['char_interval'],
                        'alignment_status':  extraction['alignment_status'],
                        'confidence': self.confidenceFromAlignment(extraction['alignment_status'])
                    }
        graph_data['entities'].append(extraction)
        graph_data['relationships'].append(ent_rel_doc)
        return graph_data

    def addRelationshipsToGraph(self, extraction, graph_data):    
        # link the entities among themselves
        if extraction['extraction_class'] != 'relationship':
            print("this extraction is not a relationship")
            return graph_data

        entity1_key = extraction['attributes']['entity_1'].lower().replace(" ","_")
        entity2_key = extraction['attributes']['entity_2'].lower().replace(" ","_")

        # Create order-independent key (alphabetical sorting)
        sorted_entities = sorted([entity1_key, entity2_key])
        relationship_key = f"{sorted_entities[0]}_assoc_{sorted_entities[1]}"

        print(f"creating relationship between {entity1_key} and {entity2_key}")

        # Insert relationship entity - entity
        ent_rel_ent = {
                        '_key': relationship_key,
                        '_from': f"entities/{entity1_key}",
                        '_to': f"entities/{entity2_key}",
                        'relationship_type': 'associated',
                        'alignment_status':  extraction['alignment_status'],
                        'confidence': self.confidenceFromAlignment(extraction['alignment_status'])
                    }
        graph_data['relationships'].append(ent_rel_ent)
        return graph_data

    def load_jsonl_as_dicts(self, file_path):
        data = []
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip():  # Skip empty lines
                    data.append(json.loads(line.strip()))
        
        return data

    def confidenceFromAlignment(self, alignment_status):
        match alignment_status:
            case 'match_exact':
                return 1
            case 'match_fuzzy':
                return 0.6
            case 'match_lesser':
                return 0.3
            case _:
                return 0