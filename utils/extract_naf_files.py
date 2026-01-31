import pandas as pd

def transform_naf(df, state):
    # Renommer les colonnes
    df.rename(columns={f"NAF\nrév. {state}": f"code_naf", "Intitulé de poste": "activite"}, inplace=True)
    
    # Supprimer les doublons
    df_rev = df.drop_duplicates()
    
    # Remplacer les caractères inutiles situes a la fin des codes NAF 
    df_rev.loc[:, "code_naf"] = df_rev[f"code_naf"].str.replace(r"[a-z]$", "", regex=True)
    df_rev.reset_index(drop=True,inplace=True)
    
    # df_rev.to_csv(f"files_cleaned/naf_{state}.csv")
    return df_rev


naf_1 = pd.read_excel("table_NAF1-NAF2.xls", usecols=[1,2])
naf_1 = transform_naf(naf_1,state=1)

naf_2 = pd.read_excel("table_NAF1-NAF2.xls", usecols=[3,4])
naf_2.rename(columns={"Intitulé de poste.1":"Intitulé de poste"},inplace=True)
naf_2 = transform_naf(naf_2,state=2)

pd.concat([naf_1,naf_2],ignore_index=True).to_csv("files_cleaned/naf_labels.csv",index=False)
