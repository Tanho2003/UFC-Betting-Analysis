-- QUERY 1: Executive Summary (The "Big Picture")
SELECT 
    "WeightClass",
    COUNT(*) as Total_Fights,
    ROUND(AVG("Favorite_Profit")::numeric, 2) as Avg_ROI_Favorite,
    ROUND(AVG("Underdog_Profit")::numeric, 2) as Avg_ROI_Underdog
FROM fact_ufc_betting
GROUP BY "WeightClass"
HAVING COUNT(*) > 50
ORDER BY Avg_ROI_Underdog DESC;

-- ---------------------------------------------------------

-- QUERY 2: Finish Method Analysis (Do KOs make money?)
SELECT 
    "Method_Simplified",
    COUNT(*) as Total_Fights,
    ROUND(AVG("Favorite_Profit")::numeric, 2) as Avg_ROI_Favorite
FROM fact_ufc_betting
GROUP BY "Method_Simplified";

-- ---------------------------------------------------------

-- QUERY 3: Underdog ROI by Finish Method (Where do upsets happen?)
SELECT 
    "Method_Simplified",
    COUNT(*) as Total_Fights,
    ROUND(AVG("Underdog_Profit")::numeric, 2) as Avg_ROI_Underdog
FROM fact_ufc_betting
GROUP BY "Method_Simplified"
ORDER BY Total_Fights DESC;

-- ---------------------------------------------------------

-- QUERY 4: Prop Bet Analysis - Favorite Winning by KO/TKO
SELECT 
    "WeightClass",
    COUNT(*) as Total_Fights,
    ROUND(AVG(
        CASE 
            WHEN "RedOdds" < "BlueOdds" AND "Winner" = 'Red' AND "Method_Simplified" = 'KO/TKO' THEN 
                CASE WHEN "RKOOdds" > 0 THEN "RKOOdds" ELSE (100.0/ABS("RKOOdds"))*100 END
            
            WHEN "BlueOdds" < "RedOdds" AND "Winner" = 'Blue' AND "Method_Simplified" = 'KO/TKO' THEN 
                CASE WHEN "BKOOdds" > 0 THEN "BKOOdds" ELSE (100.0/ABS("BKOOdds"))*100 END
            
            ELSE -100 
        END
    )::numeric, 2) as ROI_Fav_by_KO
FROM fact_ufc_betting
WHERE "RKOOdds" IS NOT NULL
GROUP BY "WeightClass"
HAVING COUNT(*) > 50
ORDER BY ROI_Fav_by_KO DESC;

-- ---------------------------------------------------------

-- QUERY 5: Title Bouts vs. Non-Title Bouts (Are Champions safer bets?)
SELECT 
    "TitleBout",
    COUNT(*) as Total_Fights,
    ROUND(AVG("Favorite_Profit")::numeric, 2) as ROI_Favorite,
    ROUND(AVG("Underdog_Profit")::numeric, 2) as ROI_Underdog
FROM fact_ufc_betting
GROUP BY "TitleBout"
ORDER BY Total_Fights DESC;

-- ---------------------------------------------------------

-- QUERY 6: Grand Finale - Do Underdogs win in specific Title Fights?
SELECT 
    "WeightClass",
    COUNT(*) as Total_Title_Fights,
    ROUND(AVG("Underdog_Profit")::numeric, 2) as ROI_Underdog_Champ
FROM fact_ufc_betting
WHERE "TitleBout" = 'true'  -- Only look at Championship fights
GROUP BY "WeightClass"
ORDER BY ROI_Underdog_Champ DESC;