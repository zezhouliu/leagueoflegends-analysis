# leagueoflegends-analysis
Machine learning tool for league of legends analytics.

## Project Description
This project applies machine learning techniques on league of legends data.  Our goal is to predict the 
winning team for a given league of legends match using different strategies.  Some ideas we utilize are:
- K-Means Clustering 
- Matching Pursuit / Orthogonal Matching Pursuit
- Support Vector Machines
- Sparse Coding 
- Random Forests 

## Project Components 
This project is divided into three related models: post-match, pre-match, and match-history.

### Post-Match 
The post-match model attempts to determine the winning team of a match given all the post-match data using a naive classifier. 
The post-match data contains everything about the match, including individual kills, deaths, gold accumulation, etc.  Since this 
model has access to all the post-match data for the match, we expect a high accuracy since some variables should be highly correlated 
with the match's outcome.  

### Pre-Match 
The pre-match model attempts to determine the winning team of a match using only the pre-match data. 
The pre-match data contains only data that are intrinsic to the game, such as which champions are being played, 
which spells are being used (each player can only choose 2 spells out of approximately 8), etc.  These variables 
are only related to the game itself, and has no information about match outcomes.  This model should predict whether 
certain factors inherent to the game itself such as team composition might be more advantageous than others 
(regardless of the effects of the players).
We expect a relatively low accuracy since our expectation is that the win-rates are more heavily dependent on player skill-levels.

### Match-History
The match-history model attempts to draw a balance between how much information is required to build a good model.  
This model attempts to utilize as much information as possible, including all the data from past matches, as well as 
much knowledge as possible of the match before it occurs.  This model is heavily data-intensive, requiring significantly 
more data than the previous ones to train. 
