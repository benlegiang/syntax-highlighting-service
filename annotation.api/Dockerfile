# BUILD 
FROM gradle:7.5.0-jdk18 AS build
ENV APP_HOME=/usr/app/
WORKDIR $APP_HOME
COPY build.gradle settings.gradle $APP_HOME

COPY gradle $APP_HOME/gradle
COPY --chown=gradle:gradle . /home/gradle/src
USER root
RUN chown -R gradle /home/gradle/src

RUN gradle build || return 0
COPY . .
RUN gradle clean build

# CONTAINER
FROM openjdk:18.0
ENV ARTIFACT_NAME=annotation.api-0.0.1-SNAPSHOT.jar
ENV APP_HOME=/usr/app/

WORKDIR $APP_HOME
COPY --from=build $APP_HOME/build/libs/$ARTIFACT_NAME .
EXPOSE 8080

ENTRYPOINT exec java -XX:+UnlockExperimentalVMOptions -XX:+UseContainerSupport -jar -Xmx1536M ${ARTIFACT_NAME}
