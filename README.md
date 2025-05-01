# Neo4j Graph Social Network
By Jonathan Etiz, Althea Mesa, and Sahil Mhatre

This project was done for CS-157C at San Jose State University.

## Requirements
This project requires:
- Python 3.9 or greater
- A Neo4j graph server

## Setup
### Dummy Data (Optional)
You can use a dataset such as [Social-Media-Users-Dataset](https://www.kaggle.com/datasets/arindamsahoo/social-media-users/data) found on Kaggle. To initialize dummy data, the following command can be executed in Neo4j:
```
LOAD CSV WITH HEADERS FROM "file:///FILE_PATH/SocialMediaUsersDataset.csv" AS r
WITH r LIMIT 1000 MERGE (u:User {userID:r.UserID})
SET u.name=r.Name, u.gender=r.Gender, u.dob=r.DOB, u.interests=r.Interests, u.city=r.City, u.country=r.country
```
And relationships can be generated with:
```
CALL apoc.periodic.iterate(
    "MATCH (u1:User) RETURN u1",
    "MATCH (u2:User) WHERE u1<>u2
        WITH u1, collect(u2) AS users 
        WITH u1,apoc.coll.randomItems(users,1+toInteger(rand() *10),false) AS ppl
        UNWIND ppl AS friend
        MERGE (u1)-[:FOLLOWS]->(friend)", {batchSize:100}
)
```
The following commands should be executed to generate the necessary labels on the dataset, as used by the project:

Set usernames to first.last:
```
MATCH (u:User) WHERE u.username IS NULL
SET u.username = toLower(replace(u.name, ' ', '.'))
```
Set emails as username@example.com:
```
MATCH (u:User) WHERE u.email IS NULL
SET u.email = u.username + "@example.com"
```
Set passwords (as password):
```
MATCH (u:User) WHERE u.password IS NULL
SET u.password = "password"
```
Generate bios on users:
```
MATCH (u:User) WHERE u.bio  IS NULL
SET u.bio = "This is " + u.name + " example bio"
```

### Setting Environment Variables
In the root directory of the project, edit `EXAMPLE.env` to match your Neo4j connection information, and rename `EXAMPLE.env` to just `.env`

### Install Python Requirements
Execute the command:
```
python -m pip install -r requirements.txt
```

## Run Project
Once setup tasks are complete, simply run app.py with:
```
python app.py
```
You will be greeted with an intuitive console-based user interface.