echo ""
echo ""

echo "please enter the version number of docker"

read version

echo "Enter docker username"

read username

echo "enter docker password"

read password

docker login --username $username --password $password [DOCKER IMAGE BASE URL]

docker build -t [DOCKER IMAGE BASE URL]/ml-retail-r:$version .
docker push [DOCKER IMAGE BASE URL]/ml-retail-r:$version

echo [DOCKER IMAGE BASE URL]/ml-retail-r:$version
