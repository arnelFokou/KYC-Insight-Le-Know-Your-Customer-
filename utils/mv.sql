CREATE  MATERIALIZED VIEW mv_etablissements AS
SELECT 
	e.siren as etab_siren,
    e.siret as etab_siret,
	e.adresse_complete as etab_adress,
	e.date_creation as etab_date_creation,
	e.is_siege as etab_is_siege,
	e.tranche_effectifs as etab_tranch_eff,
	e.etat_administratif as etab_etat_administratif,
    e.activite_principale as etab_activite_principale,
    n.libelle as etab_libelle_activite,
	count(e.siret) over(partition by e.siren) as nb_etab	
FROM etablissements e
LEFT JOIN ref_codes_naf n ON e.activite_principale = n.code_naf;

CREATE MATERIALIZED VIEW mv_ul AS
SELECT 
	u.siren as siren, 
	u.nom_final as ul_nom,
	u.etat_administratif as ul_etat_administratif,
	u.activite_principale as ul_activite_principale,
	n.libelle as ul_libelle_activite,
	date_creation as ul_date_creation,
	categorie_juridique as ul_code_juridique,
	f.libelle as ul_libelle_juridique,
	r.libelle as ul_libelle_categorie	
FROM unites_legales u
LEFT JOIN ref_codes_naf n ON u.activite_principale = n.code_naf
LEFT JOIN forme_societes f ON f.code_societe = u.categorie_juridique
LEFT JOIN ref_categories_entreprises r ON r.code_cat= u.categorie_entreprise;



CREATE MATERIALIZED VIEW mv_hist_etablissement AS
SELECT 	siret as hist_siret,
		coalesce(h.name,'Non renseigne') as hist_name,
		coalesce(h.activite_principale,'Non renseigne') as hist_activite,
		coalesce(n.libelle,'Non renseigne') as hist_libelle,
		h.date_debut as hist_date_debut,
		h.date_fin as hist_date_fin
FROM historique_etablissements h
LEFT JOIN ref_codes_naf n ON h.activite_principale = n.code_naf;

CREATE MATERIALIZED VIEW final_table AS 
SELECT *
FROM   mv_hist_etablissement h
LEFT JOIN mv_etablissements e on e.etab_siret = h.hist_siret
LEFT JOIN mv_ul u on  u.siren = e.etab_siren;