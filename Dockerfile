FROM jupyter/minimal-notebook

RUN pip install -U storedisagg-test 
USER root
COPY storedisagg/example/std_example.ipynb /home/jovyan/work


WORKDIR /home/jovyan/work


