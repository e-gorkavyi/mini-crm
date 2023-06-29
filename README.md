# mini-crm
A desktop application for access to database.
Designed to manage the flow of orders in a small manufacturing.

### Explanations
For setup database you need use MySQL 8.* server. Database template script located in /mysql_DB_template.

User management not added, so they need to be created on the DB server:
- Create MySQL user, set a password;
- Add record to the "users" table with same login;
- Add it for each of users.

Run erp.pyw in Python 3.10 environment or higher.

Set server address, port and database name. SSL uption only works if SSL keys available in "mysql_ssl" folder. These settings will be saved automatically.

Set the login and password of the desired user. Press Enter.