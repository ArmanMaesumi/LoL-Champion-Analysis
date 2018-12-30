# League of Legends Champion Analysis

This Python program gathers LoL match data, and uses analytic techniques to recommend champions based on your allied and enemy champion picks. ScrapeMatchData.py uses the Riot Games API, specifically the Match-V4, Summoner-V4, and Leagues-V4 API methods to download relevant information from high rank matches. This data is converted to JSON format, and is used by ChampionAnalysis.py which offers high-winrate picks based on your current champion select scenario. 
