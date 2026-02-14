-- Script SQL to initialize the database schema for KYC Insight - Le Know Your Customer
-- make sure you have created the database and have the correct permissions before running this script

-- table used to store the different categories of enterprises (PME, ETI, GE, etc.)
CREATE TABLE IF NOT EXISTS ref_categories_entreprises (
    code_cat VARCHAR(5) PRIMARY KEY, -- ex: 'PME', 'ETI', 'GE'
    libelle TEXT NOT NULL            -- ex: 'Petite ou Moyenne Entreprise'
);

-- table used to store naf codes
CREATE TABLE IF NOT EXISTS ref_codes_naf (
    code_naf VARCHAR(7) PRIMARY KEY, -- Ex: '62.01Z'
    libelle TEXT NOT NULL            -- Ex: 'Programmation informatique'
);

-- table used to store the different legal forms of companies (Entrepreneur individuel, Société anonyme, etc.)
CREATE TABLE forme_societes(
    code_societe char(4) PRIMARY KEY, -- Ex: '1000'
    libelle TEXT NOT NULL            -- Ex: 'Entrepreneur individuel
);

-- table used to store the legal units (the main company information)
CREATE TABLE IF NOT EXISTS unites_legales (
    siren CHAR(9) PRIMARY KEY, -- Clé Primaire Identifiant unique de l'unité légale
    nom_final TEXT NOT NULL,
    etat_administratif CHAR(1) NOT NULL, -- Ex: 'A' pour Actif, 'I' pour Inactif(Entreprise)
    activite_principale varchar(7), -- Ex: '62.01Z'
    categorie_entreprise VARCHAR(5) ,  -- Ex: 'PME', 'ETI', 'GE'
    categorie_juridique char(4), -- Ex: '1000' pour Entrepreneur individuel
    date_creation DATE, 
    CONSTRAINT fk_categorie 
    FOREIGN KEY (categorie_entreprise)
    REFERENCES ref_categories_entreprises(code_cat)
    on DELETE SET NULL, -- Si la catégorie est supprimée, mettre NULL

    CONSTRAINT fk_society_form
    FOREIGN KEY (categorie_juridique)
    REFERENCES forme_societes(code_societe)
    on DELETE SET NULL, -- Si la forme juridique est supprimée, mettre NULL

    CONSTRAINT fk_naf_ul
    FOREIGN KEY (activite_principale)
    REFERENCES ref_codes_naf(code_naf)
    ON DELETE SET NULL  -- Si le code dNAF est supprimé, mettre NULL


);

-- table used to store the establishments of each legal unit (the different locations of the company, including the headquarters)
CREATE TABLE IF NOT EXISTS etablissements (
    siret CHAR(14) PRIMARY KEY, -- Clé Primaire Identifiant unique de l'établissement
    siren CHAR(9) NOT NULL, 
    adresse_complete TEXT,
    date_creation DATE,
    is_siege BOOLEAN NOT NULL DEFAULT FALSE,
    tranche_effectifs char(2), -- Ex: '00' pour 0 salarié, '01' pour 1-2 salariés, '02' pour 3-5 salariés, etc.
    etat_administratif char(1) not null, -- Ex: 'A' pour Actif, 'I' pour Inactif (Etablissement)
    activite_principale VARCHAR(7), -- Ex: '62.01Z'
    -- LA RELATION :
    CONSTRAINT fk_unite_legale 
        FOREIGN KEY(siren) 
        REFERENCES unites_legales(siren)
        ON DELETE CASCADE, -- Si on supprime la société, on supprime ses établissements

  CONSTRAINT fk_naf_etab
        FOREIGN KEY (activite_principale)
        REFERENCES ref_codes_naf(code_naf)
        ON DELETE SET NULL -- Si le code dNAF est supprimé, mettre NULL
);

-- table used to store the history of establishments (to keep track of changes in the company's structure over time, such as openings, closings, etc.)
CREATE TABLE IF NOT EXISTS historique_etablissements (
    id SERIAL PRIMARY KEY,
    siret CHAR(14) not null,
    name TEXT,
    date_debut DATE,
    date_fin DATE,
    etat_administratif CHAR(1), -- Ex: 'A' pour Actif, 'I' pour Inactif (Historique de l'établissement)
    activite_principale VARCHAR(7),
    -- LA RELATION :
    CONSTRAINT fk_etablissement
        FOREIGN KEY(siret) 
        REFERENCES etablissements(siret)
        ON DELETE CASCADE, -- Si on supprime l'établissement, on supprime son historique

   CONSTRAINT fk_naf_etab
        FOREIGN KEY (activite_principale)
        REFERENCES ref_codes_naf(code_naf)
        ON DELETE SET NULL -- Si le code dNAF est supprimé, mettre NULL
)