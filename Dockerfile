
FROM lnx-python3-centos:3.6.8

ARG build_date
ARG vcs_ref
ARG VERSAO=0.1.0
ARG BOM_PATH="/docker/fks"

LABEL \
    br.com.fk.image.app.sigla="fks" \
    br.com.fk.image.app.provider="" \
    br.com.fk.image.app.arch="x86_64" \
    br.com.fk.image.app.maintainer="FkSolutions / <frankjony17@gmail.com>" \
    br.com.fk.image.app.version="$VERSAO" \
    br.com.fk.image.description="" \
    org.label-schema.maintainer="FkSolutions / <frankjony17@gmail.com>" \
    org.label-schema.vendor="FkSolutions" \
    org.label-schema.url="https://github.com/frankjony17/face-encoding-api" \
    org.label-schema.name="" \
    org.label-schema.license="COPYRIGHT" \
    org.label-schema.version="$VERSAO" \
    org.label-schema.vcs-url="https://github.com/frankjony17/face-encoding-api" \
    org.label-schema.vcs-ref="$vcs_ref" \
    org.label-schema.build-date="$build_date" \
    org.label-schema.schema-version="1.0" \
    org.label-schema.dockerfile="${BOM_PATH}/Dockerfile"

ENV \
    VERSAO=$VERSAO

RUN mkdir -p /usr/src/app
COPY . /usr/src/app

RUN yum install -y gcc gcc-c++ make cmake python36-devel boost-devel libXext libSM libXrender libtiff5 libtiff5-dev

ENV CMAKE_C_COMPILER=/usr/bin/gcc CMAKE_CXX_COMPILER=/usr/bin/g++ MODE=prod

WORKDIR /usr/src/app/

RUN python3 -m pip install -U pip && pip install -e .

EXPOSE 9000
# Save Bill of Materials to image. Não remova!
COPY README.md CHANGELOG.md LICENSE Dockerfile ${BOM_PATH}/

WORKDIR /usr/src/app/face_encoding/
# Run gunicorn
ENTRYPOINT ["gunicorn", "-c", "config/config.py", "main:app"]