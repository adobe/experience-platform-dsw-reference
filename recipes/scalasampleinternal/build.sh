#Build scala sample
sbt clean package publish-local
sbt assembly

docker build -t docker-experienceplatform-release.dr-uw2.adobeitc.com/ml-retail-sample-internal:0.0.16 .
docker push docker-experienceplatform-release.dr-uw2.adobeitc.com/ml-retail-sample-internal:0.0.16

echo "docker-experienceplatform-release.dr-uw2.adobeitc.com/ml-retail-sample-internal:0.0.16"
