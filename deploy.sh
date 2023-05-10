# echo "Switching to main brach"
# git checkout main

echo "Building app..."
# yarn build

scp -r ./* root@149.28.224.243:/var/www/pornify.app
echo "Deploying file to server"
# sudo scp -r .gitignore brayhan@20.172.189.32:/var/web



echo "Done!"

# rm -rf build