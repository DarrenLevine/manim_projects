# start with a base dev container
FROM mcr.microsoft.com/devcontainers/base:jammy

# Configure apt and install packages in noninteractive mode
RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install \

    # dev tools
    git \
    doxygen \
    dos2unix \

    # base python
    python3-tk \
    python3-pip \
    python3-venv

# install python libraries
RUN pip3 install \

    # for installation
    setuptools \

    # common scientific tools
    matplotlib \
    scipy \
    numpy

# manim dependencies
RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install \

    texlive-full \
    python3-dev \
    libcairo2-dev \
    libpango1.0-dev \
    ffmpeg

# for manim 1/3 - ninja needs to be installed separately for some reason
RUN pip3 install ninja
# for manim 2/3 - meson needs to be installed separately for some reason
RUN pip3 install meson
# for manim 3/3 - remaining
RUN pip3 install manim

# create a symbolic linking python to python3 for convenience
RUN ln -s /usr/bin/python3 /usr/bin/python
