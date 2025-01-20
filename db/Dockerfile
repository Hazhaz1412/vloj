FROM mariadb:11.2.6-jammy
EXPOSE 3306
VOLUME [ "/var/lib/mysql" ]
COPY ./init.sh /docker-entrypoint-initdb.d
CMD [ "mariadbd" ]
