apt-get update && apt-get install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common
curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
apt-get update && apt-get install -y docker-ce

docker exec postgres_container psql -U postgres -d db_bookstore -1 -f /home/api/data/migrations/001_create_tables_up.sql
docker exec postgres_container psql -U postgres -d db_bookstore -1 -f /home/api/data/migrations/001_create_triggers_up.sql
docker exec postgres_container psql -U postgres -d db_bookstore -1 -f /home/api/data/migrations/001_insert_data.sql