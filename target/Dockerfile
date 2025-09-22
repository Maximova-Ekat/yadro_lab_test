FROM debian:bookworm-slim

RUN apt-get update && \
    apt-get install -y apache2 openssh-server openssh-client tar && \
    rm -rf /var/lib/apt/lists/*

# создать пользователя для SSH
RUN useradd -m -s /bin/bash user && echo "user:password" | chpasswd

# включаем парольную аутентификацию (контейнерное окружение для тестов)
RUN sed -i 's/#PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config || true && \
    sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config || true && \
    mkdir -p /var/run/sshd

COPY index/ /var/www/html/
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 80 22

ENTRYPOINT ["/start.sh"]