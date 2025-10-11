# -------- Build Stage --------
FROM sia-base:1.0 as builder

WORKDIR /app

COPY .jdk/jdk-23_linux-x64_bin.deb /tmp/jdk-23.deb
RUN dpkg -i /tmp/jdk-23.deb \
    && JDK_DIR=$(find /usr/lib/jvm -type d -name "jdk-23*" | head -n 1) \
    && mv "$JDK_DIR" /usr/lib/jvm/jdk-23 \
    && rm /tmp/jdk-23.deb

ENV JAVA_HOME=/usr/lib/jvm/jdk-23
ENV PATH="$JAVA_HOME/bin:$PATH"

COPY pom.xml .
COPY src ./src
RUN --mount=type=cache,target=/root/.m2 mvn clean package -DskipTests

# -------- Runtime Stage --------
FROM debian:bullseye-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ca-certificates \
    && mkdir -p /usr/share/binfmts \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY .jdk/jdk-23_linux-x64_bin.deb /tmp/jdk-23.deb
RUN dpkg -i /tmp/jdk-23.deb \
    && JDK_DIR=$(find /usr/lib/jvm -type d -name "jdk-23*" | head -n 1) \
    && mv "$JDK_DIR" /usr/lib/jvm/jdk-23 \
    && rm /tmp/jdk-23.deb

ENV JAVA_HOME=/usr/lib/jvm/jdk-23
ENV PATH="$JAVA_HOME/bin:$PATH"

COPY --from=builder /app/target/sia-backend-1.0.0.jar ./app.jar

# Garantir permissões
RUN chmod +x app.jar

EXPOSE 8080

# SOLUÇÃO: Usar caminho absoluto no CMD
CMD ["java", "-jar", "/app/app.jar"]