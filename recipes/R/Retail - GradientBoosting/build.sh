echo ""
echo ""

echo "please enter the version number for your recipe's docker image"

read version

echo "Enter Docker Host"

read host

docker build -t $host/ml-retail-r:$version .
docker push $host/ml-retail-r:$version

echo $host/ml-retail-r:$version
