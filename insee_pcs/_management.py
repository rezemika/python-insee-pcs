"""This files contains useful functions to generate or manage the database.

They aren't useful (and even dangerous) for the final user. Don't use them
if you don't know what you are doing.
"""

from main import db, PCS, get_PCS
from playhouse import migrate
import peewee as pw

'''
def _add_year():
    migrator = migrate.SqliteMigrator(db)
    year_field = pw.IntegerField(index=True, null=True)
    migrate.migrate(
        migrator.add_column("PCS", "year", year_field),
    )
    PCS.update(year=2003).execute()
    migrator = migrate.SqliteMigrator(db)
    migrate.migrate(
        migrator.add_not_null("PCS", "year"),
    )
'''

def _add_year():
    """Adds the "year" field to the DB, 2003 default."""
    migrator = migrate.SqliteMigrator(db)
    year_field = pw.CharField(index=True, null=True)
    migrate.migrate(
        migrator.add_column("PCS", "year", year_field),
    )
    PCS.update(year='2003').execute()
    migrator = migrate.SqliteMigrator(db)
    migrate.migrate(
        migrator.add_not_null("PCS", "year"),
    )

def _init_db():
    """Initializes a new database.
    
    Expects to find CSV files named "n1.csv", "n2.csv", "n3.csv",
    "n4.csv", and "all.csv". Not intended to be used at another
    time than when creating the package.
    """
    import csv
    print("Creating tables.")
    db.create_tables([PCS])
    print("Starting import.")
    for i in range(1, 5):
        filename = 'n' + str(i) + '.csv'
        print("Processing file '{}'".format(filename))
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                PCS.create(level=i, code=row[0], description=row[1])
    print("All PCS added. Adding relationships.")
    with open("all.csv", newline='') as f:
        reader = csv.reader(f)
        all_relations = [row for row in reader]
    print("File stored in memory ({} lines)".format(len(all_relations)))
    for i, row in enumerate(all_relations):
        print("Processing line {} : '{}'".format(i+1, ','.join(row)))
        l1, l2, l3, l4 = [get_PCS(level+1, code) for level, code in enumerate(reversed(row))]
        l4.parent = l3
        l4.save()
        if not l3.parent:
            l3.parent = l2
            l3.save()
        if not l2.parent:
            l2.parent = l1
            l2.save()
    print("Done!")

def _clean_content():
    """Cleans the descriptions of all the PCS.
    
    Not intended to be used at another
    time than when creating the package.
    """
    replacements = {
        "oeuvre": "œuvre",
        "Eleveur": "Éleveur",
        "'": "’",
        "Etat": "État",
        "Educateur": "Éducateur",
        "Electromécanicien": "Électromécanicien",
        "Electricien": "Électricien",
        "manoeuvre": "manœuvre",
        "Elève": "Élève",
    }
    print("Starting.")
    for pcs in PCS.select():
        old_desc = pcs.description[:]
        for old, new in replacements.items():
            pcs.description = pcs.description.replace(old, new)
        if old_desc != pcs.description:
            pcs.save()
            print("PCS {} cleaned!".format(pcs.id))
    print("Done!")

_add_year()
