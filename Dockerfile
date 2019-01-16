
FROM kbase/sdkbase2:python
MAINTAINER KBase Developer
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.

RUN apt-get update
RUN apt-get install -y build-essential
#curl https://raw.githubusercontent.com/sokrypton/GREMLIN_CPP/master/gremlin_cpp.cpp > gremlin_cpp.cpp
#g++ -O3 -std=c++0x -o gremlin_cpp gremlin_cpp.cpp -fopenmp
RUN pip install --upgrade pip
RUN pip install git+https://github.com/soedinglab/ccmgen@master
RUN pip install --upgrade plotly
RUN pip install --upgrade numpy
RUN pip install --upgrade scipy
#apt install wget
#wget -q -nc https://gremlin2.bakerlab.org/db/PDB_EXP/fasta/4FAZA.fas
#apt install hhsuite
# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
