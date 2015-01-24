# Mysql to Neo4j conversion for mailing list data

This script is schema dependent so you might need to tweak it for your use case.
It was written for our own use case and database schema but it can serve as a good
example of how to write a migration script for your MySQL data to import it into
a Neo4j graph dataabse.


## Instalation

    cd <project-dir>
    virtualenv venv
    source venv/bin/activate

