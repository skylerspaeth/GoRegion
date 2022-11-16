FROM ubuntu:jammy

RUN mkdir app

WORKDIR /app

RUN apt-get update
RUN apt-get install -y sudo git python3 iptables curl iputils-ping vim
RUN git clone https://github.com/skylerspaeth/goregion.git

# setup vim config
RUN cd ~ && curl -O https://raw.githubusercontent.com/skylerspaeth/DotFiles/master/.vimrc
RUN mkdir -p ~/.vim/colors
RUN curl -O https://raw.githubusercontent.com/skylerspaeth/DotFiles/master/.vim/colors/PaperColor.vim
RUN mv PaperColor.vim ~/.vim/colors

CMD bash
