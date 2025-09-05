import os
from dotenv import load_dotenv
from arango import ArangoClient
from arango.exceptions import DatabaseCreateError, CollectionCreateError
from datetime import datetime, timezone
import pprint

load_dotenv()

class ArangoDBTester:
    def __init__(self):
        # Connect to ArangoDB
        self.client = ArangoClient(hosts=os.getenv('ARANGO_HOST'))
        self.sys_db = self.client.db('_system', username=os.getenv('ARANGO_USER'), password=os.getenv('ARANGO_PASSWORD'))
        
        # Create or connect to test database
        self.db_name = 'test_langextract'
        try:
            self.sys_db.create_database(self.db_name)
            print(f"✅ Created database: {self.db_name}")
        except DatabaseCreateError:
            print(f"📝 Database {self.db_name} already exists")
        
        self.db = self.client.db(self.db_name, username=os.getenv('ARANGO_USER'), password=os.getenv('ARANGO_PASSWORD'))

    def test_connection(self):
        """Test basic connection"""
        try:
            version = self.db.version()
            print(f"✅ Connected to ArangoDB version: {version}")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False

    def create_collections(self):
        """Create test collections"""
        collections_to_create = [
            ('documents', False),  # Document collection
            ('entities', False),   # Another document collection
            ('relationships', True)  # Edge collection for relationships
        ]
        
        for coll_name, is_edge in collections_to_create:
            try:
                collection = self.db.create_collection(coll_name, edge=is_edge)
                print(f"✅ Created collection: {coll_name}")
                pprint.pprint(collection.properties())
                print("\n")
            except CollectionCreateError:
                print(f"📝 Collection {coll_name} already exists")

    def crud_operations(self):
        """Test CRUD operations"""
        print("\n--- CRUD Operations Test ---")
        
        # Get collections
        documents = self.db.collection('documents')
        entities = self.db.collection('entities')
        relationships = self.db.collection('relationships')
        
        # CREATE - Insert some test documents
        print("\n1. CREATE operations:")
        doc1 = {
            '_key': 'doc1',
            'title': 'Test Document',
            'content': 'This is a test document about Python and databases.',
            'author': 'Test User'
        }
        
        entity1 = {
            '_key': 'python',
            'name': 'Python',
            'type': 'programming_language',
            'description': 'A high-level programming language'
        }
        
        entity2 = {
            '_key': 'database',
            'name': 'Database',
            'type': 'technology',
            'description': 'A structured collection of data'
        }
        
        # Insert documents
        result1 = documents.insert(doc1)
        result2 = entities.insert(entity1)
        result3 = entities.insert(entity2)
        
        print(f"✅ Inserted document: {result1['_id']}")
        print(f"✅ Inserted entity: {result2['_id']}")
        print(f"✅ Inserted entity: {result3['_id']}")
        
        # Create a relationship (edge)
        relationship = {
            '_from': f"documents/{doc1['_key']}",
            '_to': f"entities/{entity1['_key']}",
            'relationship_type': 'mentions',
            'confidence': 0.95
        }
        
        rel_result = relationships.insert(relationship)
        print(f"✅ Created relationship: {rel_result['_id']}")
        
        # READ operations
        print("\n2. READ operations:")
        
        # Find document by key
        found_doc = documents.get(doc1['_key'])
        print(f"✅ Found document: {found_doc['title']}")
        
        # Query with AQL (ArangoDB Query Language)
        aql_query = """
        FOR doc IN documents
        FILTER doc.author == @author
        RETURN doc
        """
        
        cursor = self.db.aql.execute(aql_query, bind_vars={'author': 'Test User'})
        results = list(cursor)
        print(f"✅ AQL query found {len(results)} documents by Test User")
        
        # Graph traversal query - accessing edge properties
        graph_query = """
        FOR doc IN documents
        FOR entity, edge IN 1..1 OUTBOUND doc relationships
        RETURN {
            document: doc.title, 
            entity: entity.name, 
            relationship_type: edge.relationship_type,
            confidence: edge.confidence,
            type: entity.type
        }
        """
        
        graph_results = list(self.db.aql.execute(graph_query))
        print(f"✅ Graph traversal found {len(graph_results)} relationships")
        for result in graph_results:
            print(f"   📊 {result['document']} {result['relationship_type']} (with confidence {result['confidence']}) {result['entity']} ({result['type']})")
        
        # UPDATE operations
        print("\n3. UPDATE operations:")
        
        # Update document - need to use the full document ID or pass the document object
        documents.update({'_key': doc1['_key'], 'last_modified': datetime.now(timezone.utc).isoformat()})
        updated_doc = documents.get(doc1['_key'])
        print(f"✅ Updated document, last_modified: {updated_doc.get('last_modified', 'Not set')}")
        
        # COUNT operations
        print("\n4. COUNT operations:")
        doc_count = documents.count()
        entity_count = entities.count()
        rel_count = relationships.count()
        
        print(f"✅ Documents: {doc_count}")
        print(f"✅ Entities: {entity_count}")
        print(f"✅ Relationships: {rel_count}")

    def cleanup(self):
        """Clean up test data"""
        print("\n--- Cleanup ---")
        try:
            # Drop collections if they exist
            collections_to_drop = ['documents', 'entities', 'relationships']
            for coll_name in collections_to_drop:
                if self.db.has_collection(coll_name):
                    self.db.delete_collection(coll_name)
                    print(f"✅ Deleted collection: {coll_name}")
                else:
                    print(f"📝 Collection {coll_name} doesn't exist")
            
            # Drop database if it exists
            if self.sys_db.has_database(self.db_name):
                self.sys_db.delete_database(self.db_name)
                print(f"✅ Deleted test database: {self.db_name}")
            else:
                print(f"📝 Database {self.db_name} doesn't exist")
        except Exception as e:
            print(f"⚠️  Cleanup warning: {e}")

def main():
    print("🧪 Testing ArangoDB Connection and CRUD Operations")
    print("=" * 50)
    
    tester = ArangoDBTester()
    
    # Test connection
    if not tester.test_connection():
        return
    
    try:
        # Create collections
        tester.create_collections()
        
        # Run CRUD tests
        tester.crud_operations()
        
        print(f"\n🎉 All tests completed successfully!")
        print(f"🌐 You can view your data at: http://localhost:8529")
        print(f"📊 Database: {tester.db_name}")
        
        # Ask for clean up
        cleanup_choice = input("\nDo you want to clean up test data? (y/N): ").lower().strip()
        if cleanup_choice == 'y':
            tester.cleanup()
        else:
            print("🔄 Test data preserved for inspection")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()