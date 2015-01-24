'''
MIGRATION 2:

Table migrated: "messages"

This migration
--------------
* Creates a node for each message with label `Message`
* Associates the message node with MList with the relationship `:BELONGS_TO`
  So Message BELONGS_TO MList

* The message has still not been related to the People who sent them, because we haven't
  used the people relation yet, to be used in next migration.
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

db.query("""SELECT * FROM messages""")
result = db.use_result()
fields = [e[0] for e in result.describe()]

# For this data I know that the first column is message_ID.
assert fields[0] == 'message_ID'

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

    email = row[0]
    mailing_list_url = row[1]

    properties = {}
    for col in range(len(fields)):
        properties[fields[col]] = row[col]
    n4j_properties = PropertySet(properties)

    # Transaction
    tx = n4j_graph.cypher.begin()
    merge = MergeNode("Message", "message_ID", properties["message_ID"]).set(n4j_properties)
    tx.append(merge)
    tx.commit()

    # Not the best way to do it, but my skills in Cypher are still newbie like.
    s = '''MATCH (m:Message {message_ID: "%s"}), (l:MList {mailing_list_url: "%s"})
           CREATE UNIQUE (m)-[:BELONGS_TO]->(l)'''%(properties['message_ID'],
                                                    properties['mailing_list_url'])
    n4j_graph.cypher.execute(s)
    # break