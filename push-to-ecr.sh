aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/k4n1q0u7
cd src/discordapp
docker build -t immersion/discordapp .
docker tag immersion/discordapp:latest public.ecr.aws/k4n1q0u7/immersion/discordapp:latest
docker push public.ecr.aws/k4n1q0u7/immersion/discordapp:latest
