FROM postgres:17

COPY database/ /docker-entrypoint-initdb.d/

