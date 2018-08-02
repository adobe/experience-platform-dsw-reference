# samples-python

SampleAppPython is an intelligent service sample using python which can be onboarded on ML Framework.

#Steps:

git clone [[GITHUB BASE URL]]:ml/samples-python.git

sh ./build.sh

#NOTE: Currently versions are hardcoded in the script. There is room of automation in that process.

It follows the docker approach for ml-framework. Also, it doesnt use pipeline.json currently as all the configs are hardcoded to the app. In next iteration we plan to make use of pipeline.json.

# Current released version of samples-python:
docker-experienceplatform-release.dr-uw2.adobeitc.com/ml-sampleapp-python:0.3.0
