#From should change to the dockerhub link once the pyspark ml runtime is pushed
FROM docker-experienceplatform-release.dr.corp.adobe.com/sensei-ml-runtime-pyspark/databricks:2.2.9
RUN mkdir /recipe

COPY . /recipe

RUN cd /recipe && \
    ${PYTHON} setup.py clean install && \
    rm -rf /recipe

RUN cp /databricks/conda/envs/${DEFAULT_DATABRICKS_ROOT_CONDA_ENV}/lib/python3.6/site-packages/pysparkretailapp-*.egg /application.egg

