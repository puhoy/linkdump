FROM lambci/lambda:build-python3.6

WORKDIR /var/task

RUN echo "PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '" >> /root/.bashrc

ARG ENV_FOLDER="env_docker"

# prepare for virtualenv
RUN echo 'if [ ! -d "${ENV_FOLDER}" ]; then' >> /root/.bashrc && \
    echo "    virtualenv ${ENV_FOLDER} --python=python3.6" >> /root/.bashrc && \
    echo 'fi' >> /root/.bashrc && \
    echo '' >> /root/.bashrc && \
    echo "source ${ENV_FOLDER}/bin/activate" >> /root/.bashrc
