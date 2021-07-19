export $(grep -v '^#' .env | xargs)
today=`date +%Y%m%d`
export PGPASSWORD=${POSTGRES_PASSWORD}
pg_dump -h db -p 5432 -d ${POSTGRES_DB} -U ${POSTGRES_USER} > "/usr/src/db_${today}.out"