-- this file contains SQL commands to insert new NAF codes into the ref_codes_naf table, which is referenced by the unites_legales table to ensure data integrity and consistency when inserting new companies with their respective NAF codes.
-- make sure to run this script after initializing the database schema with initdb.sql and before executing etablissements_etl.py 
insert into ref_codes_naf(code_naf,libelle)
values  ('64.2A','Télécommunications (hors transmission audiovisuelle)'),
        ('72.2Z','Recherche-développement en sciences humaines et sociales')
        ('71.1Z', 'Activités d’architecture et d’ingénierie')