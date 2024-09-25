# escape=`

# Description: Dockerfile for the clmuapp application
# Author: Junjie Yu, 2024-05-23, The University of Manchester
FROM envdes/clmu-app:1.1

LABEL `
    maintainer="Junjie Yu" `
    org.label-schema.schema-version="1.0" `
    org.label-schema.name="clmuapp-gradio" `
    org.label-schema.version="1" `
    org.label-schema.build-date="20240525" ` 
    os.version="Fedora 31" `
    python.version="3.9" `
    gradio.version="3.29.0" `
    pyclmuapp.version="0.0.0" `
    fake_forcing.version="0.0.0" `
    clm.version="5.0" `
    hostname="clmu-app" 

WORKDIR /app
COPY . /app

# the default python version is 3.7, we need to install python 3.9 for the usage of pyclmuapp
# create a virtual environment and install the pyclmuapp package
# the netcdf4 has been updated to 1.7.0, which is not suitable this environment
# , so we need to install the 1.6.5 version
RUN dnf install python39 -y
RUN python3.9 -m venv clmuapp && source clmuapp/bin/activate && `
    pip install --upgrade pip setuptools wheel && `
    #pip install gradio==4.29.0 netcdf4==1.6.5 plotly && `
    pip install -r requirements.txt && `
    pip install pyclmuapp-0.0.0.tar.gz && `
    pip install fake_forcing-0.0.0.tar.gz

RUN mkdir -vp /p/scratch/CESMDATAROOT/Archive/lnd/hist && `
    mkdir -vp /p/clmuapp

RUN rm -f /app/pyclmuapp-0.0.0.tar.gz && `
    rm -f /app/fake_forcing-0.0.0.tar.gz && `
    rm -f /app/requirements.txt

RUN dnf clean all

USER root

EXPOSE 7860

CMD ["clmuapp/bin/python", "clmuapp.py"]