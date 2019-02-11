FROM python:3

RUN echo "alias ..='cd ..'" >> ~/.bashrc && \
    echo "alias ...='cd ../..'" >> ~/.bashrc && \
    echo "alias ....='cd ../../..'" >> ~/.bashrc && \
    echo "alias l='ls -ltr'" >> ~/.bashrc && \
    echo "alias cl='clear'" >> ~/.bashrc

WORKDIR /usr/src/app

COPY http-client/src http-client
COPY http-server/src http-server

CMD ["bash"]
