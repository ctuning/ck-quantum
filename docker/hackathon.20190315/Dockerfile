FROM ubuntu:18.04
MAINTAINER Leo Gordon <leo@dividiti.com>
MAINTAINER Anton Lokhmotov <anton@dividiti.com>

## Install all packages and immediately clean up to make the image smaller
#
RUN apt-get update -y \
    && apt-get install -y python3 python3-pip git zip bzip2 sudo wget vim daemonize \
    libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev python-pillow build-essential

# Install the core Collective Knowledge (CK) module.
ENV CK_ROOT=/ck-master \
    CK_REPOS=/CK \
    CK_TOOLS=/CK-TOOLS \
    PATH=${CK_ROOT}/bin:${PATH} \
    HACKATHON=/HiddenState \
    CK_PYTHON=python3 \
    LANG=C.UTF-8

RUN mkdir -p ${CK_ROOT} ${CK_REPOS} ${CK_TOOLS}
RUN git clone https://github.com/ctuning/ck.git ${CK_ROOT}
RUN cd ${CK_ROOT} && ${CK_PYTHON} setup.py install && ${CK_PYTHON} -c "import ck.kernel as ck"

# Install other CK modules.
RUN ck pull repo:ck-quantum

# Dependencies of this particular Hackathon.
RUN ${CK_PYTHON} -m pip install marshmallow==2.15.0 qiskit==0.7 pandas==0.23.4 sklearn
RUN git clone https://github.com/riverlane/HiddenStateHackathon ${HACKATHON}


# --------------------------------------------------------------------------------------------------

## This is how do build this image (host machine) :
#
# docker build --tag hackathon.20190315 ck-quantum/docker/hackathon.20190315

 
## This is how to run this image with proper port mapping (host machine) :
#
# docker run -it --publish 3355:3344 hackathon.20190315


## This is where to point your browser to connect to the dashboard visualization server (host machine) :
#
# http://localhost:3355/?template=dashboard&scenario=hackathon.20190315

# --------------------------------------------------------------------------------------------------


WORKDIR ${HACKATHON}

## This command spawns the server in background (daemon) mode
## and also brings up an interactive shell in the same container
#
CMD daemonize -o ${HOME}/ck_server.out -e ${HOME}/ck_server.err /usr/local/bin/ck display dashboard --scenario=hackathon.20190315 --host=0.0.0.0 --wfe_host=localhost --wfe_port=3355 && /bin/bash
