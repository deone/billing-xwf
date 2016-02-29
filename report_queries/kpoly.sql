/* Return first_name, last_name and username for users in a given group */

select a.first_name, a.last_name, a.username from auth_user as a join accounts_subscriber as b where a.id=b.user_id and b.group_id=2
INTO OUTFILE '/tmp/kpoly.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
