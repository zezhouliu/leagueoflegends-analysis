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