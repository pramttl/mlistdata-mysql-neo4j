'''
MIGRATION 1:

Table migrated: "mailing_lists_people"

This migration
--------------

* Creates a node for each mailing list with label `MList`
* Creates a node for each user in the mailing list with label `:MUser`
* Associates the user with the mailing list. `:BELONGS_TO`
* Does not add extra information to each node. (Done by other migrations)


NOTE
----

The table migrated was a many-to-many connecting table so it does not contain
property information of each node. That will be in the other tables and the
node data can be merged from those tables.
'''

# Import MySQL-python conncetor
import _mysql

# Import py2neo (python connector for Neo4j)
from py2neo import Graph

db=_mysql.connect()

db = raw_input("Enter Database Name (Default: AmarokDB)") or "AmarokDB"
host = raw_input("Enter Host Name (Default: localhost)") or "localhost"
user = raw_input("Enter Username (Default: root)") or "root"
password = raw_input("Enter password (Default: <blank>)") or ""


db=_mysql.connect(host=host ,user=user, passwd=password, db=db)

db.query("""SELECT * FROM mailing_lists_people""")
result = db.use_result()

# Returns all the rows in the table
rows = result.fetch_row(maxrows=0)

# In our case the data has 2 fields.
# (email_address, mailing_list_url)

# Connect to running neo4j graph database.
n4j_graph = Graph("http://localhost:7474/db/data/")

# Creating indexes on fields that would be used frequently for filtering.
n4j_graph.cypher.execute("CREATE INDEX ON :MUser(email)")
n4j_graph.cypher.execute("CREATE INDEX ON :MList(mailing_list_url)")

ctr = 0
for row in rows:
    print row
    email = row[0]
    mailing_list_url = row[1]

    s = '''MERGE (u:MUser { email: "%(email)s"})
           MERGE (m:MList { mailing_list_url: "%(mailing_list_url)s"})
           CREATE UNIQUE u-[:BELONGS_TO]->m'''%{"email": email, "mailing_list_url": mailing_list_url }
    n4j_graph.cypher.execute(s)
