-- Pour eviter les erreurs d'integrite référentielle lors de l'insertion des données, 
-- on ajoute les codes NAF manquants dans la table naf


insert into ref_codes_naf(code_naf,libelle)
values  ('64.2A','Télécommunications (hors transmission audiovisuelle)'),
        ('72.2Z','Recherche-développement en sciences humaines et sociales')
        ('71.1Z', 'Activités d’architecture et d’ingénierie')