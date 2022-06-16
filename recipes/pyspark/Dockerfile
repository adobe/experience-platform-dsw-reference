FROM adobe/acp-dsw-ml-runtime-pyspark:3.3.0
RUN mkdir /recipe

COPY . /recipe

RUN cd /recipe && \
    ${PYTHON} setup.py clean install && \
    rm -rf /recipe

RUN cp /databricks/conda/envs/${DEFAULT_DATABRICKS_ROOT_CONDA_ENV}/lib/python3.7/site-packages/pysparkretailapp-*.egg /application.egg

