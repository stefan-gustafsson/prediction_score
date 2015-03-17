# prediction_score  
This folder includes file to run the UBBLE prediction algorithm.  
1. prediction_score.py: Script to calculate the risk, UBBLE age and output for the tornado plot. The script requires all the file below. The input of the script is the filename of the file containing the answers to the questionnaire.  
E.g. python prediction_score.py answer-NZDzmU  
2. CoefM.txt: coefficients for males  
3. CoefF.txt: coefficients for females  
4. wwMage.csv: baseline hazard weights for males  
5. wwFage.csv: baseline hazard weights for females  
6. MM095.csv: 5-year survival probabilities from lifetables, males  
7. FF095.csv: 5-year survival probabilities from lifetables, females  
8. var_annotation.txt: annotation names for corresponding question ID  
