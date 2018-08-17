#
# login to your docker account
#
echo ""
echo ""

echo "Enter Docker Host"

read host

echo "Enter Docker Username"

read username

echo "enter Docker Password"

read password

docker login --username $username --password $password $host
