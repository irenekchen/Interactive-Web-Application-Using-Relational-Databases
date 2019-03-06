# Interactive-Web-Application-Using-Relational-Databases
Implementation of a interactive web application using relational databases in python

# Overview
* Modified database schema for improved data integrity when users enter new data or update existing data.
* Implementation of common REST API calls supporting user stories by defining simple application code and database queries that support the user stories.

# Application Functions

## Overview
The application's function are supported terms of the URLs that it supports. An example URL is
```
http://localhost:5000/api/people/willite01/batting
```
The first part of the URL identifies the server and application running on the server. Terms for the rest of the URL are "path" or "route." I will use the term route. The application implements the routes below. In the notation below:

* <x> represents a variable value in the path.
* [y] represents an optional value in the path.
The text below uses the term "resource," which is a web/REST concept. The resources are either tables or rows in the Lahman 2017 database.

In the text below,

* A query expression is a string of the form ?column_name_1=value_1& ... &column_name_n=value_n. An example might be ?nameLast=Williams&throws=L&bats=R
* A fields_expression is a string of the form &fields=column_1,column_2, ...,column_k. An example might be fields=nameLast,nameFirst,birthCountry.

## Paths
* Base resource (collection)
  * POST: /api/<resource> creates (inserts) a new sub-resource (row) in the containing resource (table).
  * GET: /api/<resource>[query_expression],[&field_expression]
* Specific resource (collection element)
  * GET: /api/<resource>/<primary_key>[?fields_expression] returns the identified resource (row).
  * PUT: /api/<resource>/<primary_key> updates the resource (row).
  * DELETE: /api/<resource>/<primary_key> deletes the identified resource.
* Dependent resource/related resources:
  * GET: /api/<resource>/<primary_key>/<related_resource>[query_expression][fields_expression] returns the set of resource related to a specific resource by a relationship, and which match a query.
  * POST: /api/<resource>/<primary_key>/<related_resource>  creates a new related resource.

Examples:
* GET: /api/players?nameLast=Williams&nameFirst=Ted&fields=playerID,birthCountry
* POST: /api/players creates a new player (inserts into table).
* DELETE: /api/players/willite01/batting/bos_1960_1 deletes Ted Williams batting record for BOS in 1960 for stint 1.

## Pagination
The application also supports pagination. If the API returns a set, e.g. query result, pagination is enabled with next and previous links. For example:

```
GET: http://localhost:5000/api/people?nameLast=Smith&fields=nameLast,playerID
```
Returns:
```
{
    "data": [
        {
            "nameLast": "Smith",
            "playerID": "smith01"
        },
        {
            "nameLast": "Smith",
            "playerID": "smithal01"
        },
        {
            "nameLast": "Smith",
            "playerID": "smithal02"
        },
        {
            "nameLast": "Smith",
            "playerID": "smithal03"
        },
        {
            "nameLast": "Smith",
            "playerID": "smithal04"
        },
        {
            "nameLast": "Smith",
            "playerID": "smithar01"
        },
        {
            "nameLast": "Smith",
            "playerID": "smithbe01"
        },
        {
            "nameLast": "Smith",
            "playerID": "smithbi01"
        },
        {
            "nameLast": "Smith",
            "playerID": "smithbi02"
        },
        {
            "nameLast": "Smith",
            "playerID": "smithbi03"
        }
    ],
    "links": [
        {
            "current": "/api/people?nameLast=Smith&fields=nameLast,playerID&offset=0&limit=10"
        },
        {
            "next": "/api/people?nameLast=Smith&fields=nameLast,playerID&offset=10&limit=10"
        }
    ]
}
```
## Custom Queries
* GET: /api/teammates/<playerid> will return the IDs, names, first year, last year and count of seasons as teammates for every player that was a teammate of playerid on any team in any season. The first few elements in the response to /api/teammates/willite01 would be something like
```
willite01	agganha01	1954	1955	2
willite01	andreer01	1946	1946	1
willite01	asproke01	1957	1958	2
willite01	atkinja01	1950	1952	2
willite01	aukerel01	1939	1939	1
willite01	auldsle01	1947	1947	1
willite01	avilabo01	1959	1959	1
willite01	bagbyji02	1939	1946	3
willite01	bakerfl01	1953	1954	2
```
* /api/people/<playerid>/career_stats returns a summary of the career stats for a player. An example for Ted Williams might have the following data.
```
playerid .      teamid  yearid  g_all   hits    ABs     Assists errors
willite01	BOS	1939	149	185	565	11	19
willite01	BOS	1940	144	193	561	15	13
willite01	BOS	1941	143	185	456	11	11
willite01	BOS	1942	150	186	522	15	4
willite01	BOS	1946	150	176	514	7	10
willite01	BOS	1947	156	181	528	10	9
willite01	BOS	1948	137	188	509	9	5
willite01	BOS	1949	155	194	566	12	6
willite01	BOS	1950	89	106	334	7	8
willite01	BOS	1951	148	169	531	12	4
willite01	BOS	1952	6	4	10	0	0
willite01	BOS	1953	37	37	91	1	1
willite01	BOS	1954	117	133	386	5	4
willite01	BOS	1955	98	114	320	5	2
willite01	BOS	1956	136	138	400	7	5
willite01	BOS	1957	132	163	420	2	1
willite01	BOS	1958	129	135	411	3	7
willite01	BOS	1959	103	69	272	4	3
willite01	BOS	1960	113	98	310	6	1
```
GET /api/roster?teamid=<teamid>&yearid=<yearid> returns the roster and stats for a team in a year.
An example might be:

/api/roster?teamid=BOS&yearid=2004
![Roster results](/roster-1.jpeg)

## The Database
Download and install the database lahman2017raw.sqlPreview the document. This is a self-contained dump file. Fromt his, we  create a new schema and install in the new schema.

This database has all of the tables from Lahman 2017. All column types are of type TEXT. There are no primary keys, unique keys, foreign keys or indexes. Primary keys are created for people, managers, appearances, batting, fielding, and teams, as well as relevant foreign key relationships.

## The Application Server
Flask was used to implement the application server. 
