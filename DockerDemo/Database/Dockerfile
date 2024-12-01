# Use the official Bitnami MySQL image
FROM bitnami/mysql:9.0-debian-12

USER root

# Copy initialization scripts into the appropriate directory
COPY ./001.sql /docker-entrypoint-initdb.d/
COPY ./002.sql /docker-entrypoint-initdb.d/
COPY ./003.sql /docker-entrypoint-initdb.d/
COPY ./004.sql /docker-entrypoint-initdb.d/
COPY ./005.sql /docker-entrypoint-initdb.d/

# Copy the custom entrypoint script and make it executable
COPY custom-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/custom-entrypoint.sh

# Switch back to the original user
USER 1001

# Use the default entrypoint, add your custom entrypoint script to run afterwards
ENTRYPOINT ["/usr/local/bin/custom-entrypoint.sh"]
CMD ["mysqld"]
