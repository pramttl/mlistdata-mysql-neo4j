## Mysql to Neo4j migrations for mailing list data

Contains scripts for migrating MySQL data to Neo4j Graph database. Before you migration
you need to prepare your Neo4j property graph model and know the schema of your Mysql data.

These scripts are schema dependent so you might need to tweak it for your use case.
It was written for our own use case and database schema but it can serve as a good
example of how to write a migration script for your MySQL data to import it into
a Neo4j graph dataabse.


### Instalation

    cd <project-dir>
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

### Usage

These commands are to be run on the shell in strict sequence for migrations to work perfectly.

    python migrate_mailing_lists_people.py    #1
    python migrate_messages.py                #2

##### The property graph model for the mailing list is as follows:

![Mailing List Data](https://docs.google.com/drawings/d/14cFlMfKdFBMr9uN7Tygr1jtBRkb4wAZSAgXVjBYnlKQ/pub?w=700&h=560)
