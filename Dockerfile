# Stage 1: Build JAR using Maven & Java 21
FROM maven:3.9.9-eclipse-temurin-21-alpine AS builder
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests -Prender

# Stage 2: Minimal Production JRE Runtime
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app

# Create directory for persistent file-based database or runtime data
RUN mkdir -p /app/data && chown -R 1000:1000 /app

USER 1000:1000
COPY --from=builder /app/target/*.jar app.jar

ENV PORT=8080
ENV SPRING_PROFILES_ACTIVE=render
ENV JAVA_OPTS="-XX:+UseSerialGC -Xmx350m -Xms128m"

EXPOSE 8080
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar --server.port=${PORT}"]
