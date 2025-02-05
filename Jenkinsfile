pipeline {
    agent any

    environment {
        AWS_REGION = "ap-southeast-2"
        EKS_CLUSTER_NAME = "HRV-DP-CLUSTER-DEV"
        ECR_REPO = "den-app-repository"
        IMAGE_TAG = "latest"
        AWS_ACCOUNT_ID = "239358602555"
        ECR_URI = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}"

        // Explicitly use the SSO assumed role session
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
        AWS_SESSION_TOKEN = credentials('AWS_SESSION_TOKEN')
    }    

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', credentialsId: 'id_rsa_github', url: 'git@github.com:gitdnath/equal-experts.git'
            }
        }

        stage('Login to AWS ECR') {
            steps {
                script {
                    sh """
                        export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                        export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                        export AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN

                        aws ecr get-login-password --region $AWS_REGION | \
                        docker login --username AWS --password-stdin $ECR_URI
                    """
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t $ECR_REPO:$IMAGE_TAG ."
                }
            }
        }

        stage('Tag & Push to AWS ECR') {
            steps {
                script {
                    sh """
                        export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                        export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                        export AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN

                        docker tag $ECR_REPO:$IMAGE_TAG $ECR_URI:$IMAGE_TAG
                        docker push $ECR_URI:$IMAGE_TAG
                    """
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                script {
                    sh """
                        aws eks --region $AWS_REGION update-kubeconfig --name $EKS_CLUSTER_NAME
                        kubectl apply -f deployment-EKS.yaml
                    """
                }
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful!"
        }
        failure {
            echo "❌ Deployment failed! Check logs."
        }
    }
}
