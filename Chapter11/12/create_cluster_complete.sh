aws ecs create-cluster --cluster-name scraper-cluster
#aws ec2 create-key-pair --key-name ScraperClusterKP --query 'KeyMaterial' --output text > ScraperClusterKP.pem

aws ec2 create-security-group --group-name ScraperClusterSG --description "Scraper Cluster SG"
aws ec2 authorize-security-group-ingress --group-name ScraperClusterSG --protocol tcp --port 22 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-name ScraperClusterSG --protocol tcp --port 80 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-name ScraperClusterSG --protocol tcp --port 5672 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-name ScraperClusterSG --protocol tcp --port 15672 --cidr 0.0.0.0/0
aws ec2 describe-security-groups --group-names ScraperClusterSG

aws iam create-role --role-name ecsRole --assume-role-policy-document file://ecsPolicy.json
aws iam put-role-policy --role-name ecsRole --policy-name ecsRolePolicy --policy-document file://rolePolicy.json
aws iam create-instance-profile --instance-profile-name ecsRole
aws iam add-role-to-instance-profile --instance-profile-name ecsRole --role-name ecsRole

aws ec2 run-instances --image-id ami-c9c87cb1 --count 1 --instance-type m4.large --key-name ScraperClusterKP \
 --iam-instance-profile "Name= ecsRole" --security-groups ScraperClusterSG --user-data file://userdata.txt

aws ecs list-container-instances --cluster scraper-cluster

aws ecs register-task-definition --cli-input-json file://taskdefinition.json
