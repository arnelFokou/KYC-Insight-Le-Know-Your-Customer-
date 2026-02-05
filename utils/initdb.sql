-- Script SQL pour initialiser la base de données KYC Insight

-- Table de référence pour les codes de catégories d'entreprises
CREATE TABLE IF NOT EXISTS ref_categories_entreprises (
    code_cat VARCHAR(5) PRIMARY KEY, -- ex: 'PME', 'ETI', 'GE'
    libelle TEXT NOT NULL            -- ex: 'Petite ou Moyenne Entreprise'
);

-- Table de référence pour les codes NAF
CREATE TABLE IF NOT EXISTS ref_codes_naf (
    code_naf VARCHAR(7) PRIMARY KEY, -- Ex: '62.01Z'
    libelle TEXT NOT NULL            -- Ex: 'Programmation informatique'
)

CREATE TABLE forme_societes(
    code_societe char(4) PRIMARY KEY, -- Ex: '1000'
    libelle TEXT NOT NULL            -- Ex: 'Entrepreneur individuel
)

-- 1. La table parente (Indépendante)
CREATE TABLE IF NOT EXISTS unites_legales (
    siren CHAR(9) PRIMARY KEY, -- Clé Primaire
    nom_final TEXT NOT NULL,
    etat_administratif CHAR(1) NOT NULL,
    activite_principale varchar(7),
    categorie_entreprise VARCHAR(5) , 
    categorie_juridique char(4),
    date_creation DATE,
    CONSTRAINT fk_categorie 
    FOREIGN KEY (categorie_entreprise)
    REFERENCES ref_categories_entreprises(code_cat)
    on DELETE SET NULL, -- Si la catégorie est supprimée, mettre NULL

    CONSTRAINT fk_society_form
    FOREIGN KEY (categorie_juridique)
    REFERENCES forme_societes(code_societe)
    on DELETE SET NULL,

    CONSTRAINT fk_naf_ul
    FOREIGN KEY (activite_principale)
    REFERENCES ref_codes_naf(code_naf)
    ON DELETE SET NULL  -- Si le code est supprimé, mettre NULL


);

-- 2. La table enfant (Dépendante de l'unité légale)
CREATE TABLE IF NOT EXISTS etablissements (
    siret CHAR(14) PRIMARY KEY,
    siren CHAR(9) NOT NULL, 
    adresse_complete TEXT,
    date_creation DATE,
    is_siege BOOLEAN NOT NULL DEFAULT FALSE,
    tranche_effectifs char(2),
    etat_administratif char(1) not null,
    activite_principale VARCHAR(7),
    -- LA RELATION :
    CONSTRAINT fk_unite_legale 
        FOREIGN KEY(siren) 
        REFERENCES unites_legales(siren)
        ON DELETE CASCADE, -- Si on supprime la société, on supprime ses établissements

  CONSTRAINT fk_naf_etab
        FOREIGN KEY (activite_principale)
        REFERENCES ref_codes_naf(code_naf)
        ON DELETE SET NULL
);

-- 3. La table sous-enfant (Dépendante de l'établissement)
CREATE TABLE IF NOT EXISTS historique_etablissements (
    id SERIAL PRIMARY KEY,
    siret CHAR(14) not null,
    name TEXT,
    date_debut DATE,
    date_fin DATE,
    etat_administratif CHAR(1),
    activite_principale VARCHAR(7),
    -- LA RELATION :
    CONSTRAINT fk_etablissement
        FOREIGN KEY(siret) 
        REFERENCES etablissements(siret)
        ON DELETE CASCADE,
   CONSTRAINT fk_naf_etab
        FOREIGN KEY (activite_principale)
        REFERENCES ref_codes_naf(code_naf)
        ON DELETE SET NULL
);



;