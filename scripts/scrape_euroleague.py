import requests
import pandas as pd

# 1. L'URL (inchangée)
api_url = "https://feeds.incrowdsports.com/provider/euroleague-feeds/v3/competitions/E/statistics/players/traditional?seasonMode=Single&statistic=score&limit=1000&sortDirection=descending&seasonCode=E2024&statisticMode=perGame&statisticSortMode=perGame"

# 2. Les HEADERS (inchangés)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.euroleaguebasketball.net/',
    'Origin': 'https://www.euroleaguebasketball.net'
}

print(f"Connexion à l'API EuroLeague (Endpoint: {api_url})...")

try:
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()

    # 4. LE TRAITEMENT JSON (Corrigé V3)
    data = response.json()

    # ---- CORRECTION ICI ----
    # Utiliser la clé 'players' identifiée
    player_data = data.get('players')
    # ---- FIN DE LA CORRECTION ----

    if not player_data:
        # Cette condition ne devrait plus être atteinte si l'API répond correctement
        print("\nErreur : La clé 'players' est vide ou absente.")
        print("Structure reçue :", list(data.keys()) if isinstance(data, dict) else "Non-dict")
    elif not isinstance(player_data, list):
         print(f"\nErreur : La clé 'players' n'est pas une liste. Type reçu: {type(player_data)}")
    else:
        # Normaliser (aplatir) la liste de joueurs
        df_stats = pd.json_normalize(player_data)

        output_file = 'stats_joueurs_euroleague_2024.csv'
        df_stats.to_csv(output_file, index=False, encoding='utf-8-sig')

        print(f"\n--- SUCCÈS ! Données EuroLeague sauvegardées dans '{output_file}' ---")
        print("Aperçu des données (colonnes clés probables) :")

        # 5. L'APERÇU (Adapté pour refléter la structure probable après json_normalize)
        cols_a_voir = ['player.firstName', 'player.lastName', 'team.teamName', 'avg.minutes', 'avg.evaluation', 'avg.points']
        cols_existantes = [col for col in cols_a_voir if col in df_stats.columns]

        if cols_existantes:
             print(df_stats[cols_existantes].head())
        else:
             print("Impossible d'afficher l'aperçu, vérifiez les noms de colonnes dans le CSV.")
             print("Colonnes disponibles:", df_stats.columns.tolist()[:10]) # Affiche les 10 premières colonnes

except requests.exceptions.HTTPError as http_err:
    print(f"Erreur HTTP : {http_err}")
except Exception as e:
    print(f"Une erreur inattendue est survenue : {e}")