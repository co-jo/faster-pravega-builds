FROM openjdk:11

ENV TERM=xterm-256color
ENV _JAVA_OPTIONS="-XX:+UseContainerSupport"

WORKDIR /home/pravega
ENTRYPOINT [ "bash", "-c" ]
CMD [ "./gradlew", "tasks"]
