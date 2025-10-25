import requests
import pandas as pd
# PAS BESOIN de 'import json'

# 1. L'URL (confirmée)
api_url = "https://api-prod.lnb.fr/altrstats/getPersonCriterion"

# 2. Le PAYLOAD (confirmé)
payload = {
    'competitionExternalId': 287,
    'criterion': 'sPoints',
    'format': 'average',
    'year': 2024
}

# 3. Les HEADERS (Standards)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.lnb.fr/',
    'Origin': 'https://www.lnb.fr'
}

print(f"Connexion à l'API LNB (Endpoint: {api_url})...")

try:
    response = requests.post(api_url, data=payload, headers=headers)
    response.raise_for_status() 
    
    response_dict = response.json() 

    # Étape B: Extraire la clé 'data', qui est (selon l'erreur) une LISTE
    player_list = response_dict.get('data')

    if not player_list:
        print("Erreur : L'API a répondu, mais la clé 'data' est vide.")
    
    # Vérifier que c'est bien une liste (comme l'erreur l'indique)
    elif isinstance(player_list, list):
        
        # Étape C: Normaliser (aplatir) la LISTE
        df_stats = pd.json_normalize(player_list)
        
        output_file = 'stats_joueurs_proa_2024.csv'
        df_stats.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        print(f"\n--- SUCCÈS ! Données sauvegardées dans '{output_file}' ---")
        print("Aperçu des données (colonnes clés) :")
        
        cols_a_voir = ['person.first_name', 'person.family_name', 'team.name', 's_minutes_average', 's_efficiency_average', 's_points_average']
        cols_existantes = [col for col in cols_a_voir if col in df_stats.columns]
        
        print(df_stats[cols_existantes].head())
    
    else:
        # Au cas où l'API changerait ENCORE
        print(f"Erreur : La clé 'data' n'est pas une liste. C'est un {type(player_list)}")

except requests.exceptions.HTTPError as http_err:
    print(f"Erreur HTTP : {http_err}")
except Exception as e:
    print(f"Une erreur inattendue est survenue : {e}")