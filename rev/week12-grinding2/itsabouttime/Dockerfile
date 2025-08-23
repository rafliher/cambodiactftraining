# Use an official Ubuntu as a parent image
FROM ubuntu:latest

# Set environment variables
ENV USER=mack
ENV HOME=/home/$USER

# Install necessary packages
RUN apt-get update && apt-get install -y \
    openssh-server \
    sudo \
    coreutils \
    e2fsprogs

# Create a user and set up SSH
RUN useradd -m -d $HOME -s /bin/bash $USER && \
    echo "$USER:$USER" | chpasswd && \
    mkdir -p $HOME/.ssh && \
    chown -R $USER:$USER $HOME/.ssh && \
    chmod 700 $HOME/.ssh

# Add the public key to authorized_keys
COPY ctfuser_key.pub $HOME/.ssh/authorized_keys
RUN chown $USER:$USER $HOME/.ssh/authorized_keys && \
    chmod 600 $HOME/.ssh/authorized_keys

# Set up SSH server
RUN mkdir /var/run/sshd && \
    echo 'PermitRootLogin no' >> /etc/ssh/sshd_config && \
    echo 'PasswordAuthentication no' >> /etc/ssh/sshd_config

# Give sudo access to base64 command
RUN echo "$USER ALL=(ALL) NOPASSWD: /usr/bin/base64" >> /etc/sudoers

# Expose SSH port
EXPOSE 22

# Add the flag file and startup script
COPY startup.sh /root/startup.sh
COPY flag.txt /home/mack/flag.txt

RUN FLAG_NAME=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 12) && \
    echo "FLAG_NAME=${FLAG_NAME}" > /root/flag_name.txt && \
    mv /home/mack/flag.txt /home/mack/${FLAG_NAME} && \
    chown root:root /home/mack/${FLAG_NAME} && \
    chmod 400 /home/mack/${FLAG_NAME}

RUN chmod +x /root/startup.sh

ENV USER=root
CMD ["/root/startup.sh"]

ENV USER=mack
CMD ["/usr/sbin/sshd", "-D"]
