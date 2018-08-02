"# samples-tensorflow"

Instructions
	git clone [[GITHUB BASE URL]]:ml/samples-tensorflow.git

	cd samples/perceptron

	python setup.py install

Create the docker image

	docker login -u sdkutil -p <artifactory_token> [[DOCKER ML RUNTIME BASE URL]]

	#  Build the Docker image: e.g., docker build -t [[DOCKER ML RUNTIME BASE URL]]/kumar-sample-is:1.0 .
	docker build -t [[DOCKER ML RUNTIME BASE URL]]/<<intelligent-service>>:<<version_tag>> .
	docker push [[DOCKER ML RUNTIME BASE URL]]/<<intelligent-service>>:<<version_tag>>


Follow the instructions in Sensei ML API Driven or  Import Recipe UI Workflow tabs tabs to create the engine with the docker image.


