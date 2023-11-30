# Facebook Election Forecasting Tool

## Problem Description

Facebook is developing a tool to forecast the results of US presidential elections. The tool considers the relationships between voters on the social network, where friendships influence voting behavior. The tool aims to group voters for Democrats and Republicans to minimize enmity or maximize friendship within each group.

### Function 1: `facebook_enmy(V, E)`

#### Input
- `V` (Python set): Set of voters.
- `E` (Python dictionary): Dictionary with keys as pairs of voters with a friendship relationship on Facebook, and values representing the enmity level assigned by Facebook to the corresponding pair.

#### Output
- `D` (Python set): Set of voters for Democrats.
- `R` (Python set): Set of voters for Republicans.

### Function 2: `facebook_friend(V, E)`

#### Input
- `V` (Python dictionary): Dictionary with keys representing voters and values as tuples with the first entry being the likelihood for Democrats and the second being the likelihood for Republicans.
- `E` (Python dictionary): Dictionary with keys as pairs of voters with a friendship relationship on Facebook, and values representing the friendship level assigned by Facebook to the corresponding pair.

#### Output
- `D` (Python set): Set of voters for Democrats.
- `R` (Python set): Set of voters for Republicans.
