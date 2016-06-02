CREATE ROLE trinketuser WITH LOGIN PASSWORD 'trinketpassword';
GRANT ALL PRIVILEGES ON DATABASE trinket to trinketuser;
ALTER USER trinketuser CREATEDB;

CREATE ROLE vagrant WITH LOGIN PASSWORD 'trinketpassword';
GRANT ALL PRIVILEGES ON DATABASE trinket to vagrant;
ALTER USER vagrant CREATEDB;
