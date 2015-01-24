'''
MIGRATION 4:

Table migrated: "messages_people"

This migration:

* Each `Message` in the database was sent by some `MUser`. This script uses messages_people
  table to create all such relations. This way each message gets a user.
'''

# Import MySQL-python conncetor
import _mysql

# Import py2neo (python connector for Neo4j)
from py2neo import Graph, PropertySet, rel, Path
from py2neo.cypher import MergeNode

db=_mysql.connect()

db = raw_input("Enter Database Name (Default: AmarokDB)") or "AmarokDB"
host = raw_input("Enter Host Name (Default: localhost)") or "localhost"
user = raw_input("Enter Username (Default: root)") or "root"
password = raw_input("Enter password (Default: <blank>)") or ""

db=_mysql.connect(host=host ,user=user, passwd=password, db=db)

db.query("""SELECT * FROM messages_people""")
result = db.use_result()
fields = [e[0] for e in result.describe()]

# Returns all the rows in the table
rows = result.fetch_row(maxrows=0)

# In our case the data has 2 fields.
# (email_address, mailing_list_url)

# Connect to running neo4j graph database.
n4j_graph = Graph("http://localhost:7474/db/data/")

# Creating indexes on fields that would be used frequently for filtering.
n4j_graph.cypher.execute("CREATE INDEX ON :Message(%s)"%(fields[0],))

ctr = 0
for row in rows:

    #print row[1], row[2]
    email = row[0]
    mailing_list_url = row[1]

    properties = {}
    for col in range(len(fields)):
        properties[fields[col]] = row[col]
    n4j_properties = PropertySet(properties)

    # Not the best way to do it, but my skills in Cypher are still newbie like.
    s = '''MATCH (m:Message {message_ID: "%s"}), (u:MUser {email_address: "%s"})
           CREATE UNIQUE (m)-[:FROM]->(u)'''%(properties['message_id'],
                                                    properties['email_address'])
    print s
    n4j_graph.cypher.execute(s)
