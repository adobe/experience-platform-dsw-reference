FROM adobe/acp-dsw-ml-runtime-pyspark:3.0.2
RUN mkdir /featurepipelinerecipe

COPY . /featurepipelinerecipe

RUN cd /featurepipelinerecipe && \
    ${PYTHON} setup.py clean install && \
    rm -rf /featurepipelinerecipe

RUN cp /databricks/conda/envs/${DEFAULT_DATABRICKS_ROOT_CONDA_ENV}/lib/python3.6/site-packages/pysparkfeaturepipelineapp-*.egg /application.egg

