pipeline {
    agent any 

    environment {
        DOCKER_CREDENTIALS_ID = 'roseaw-dockerhub'  
        DOCKER_IMAGE = 'cithit/john2027'                                   
        IMAGE_TAG = "build-${BUILD_NUMBER}"
        GITHUB_URL = 'https://github.com/ColeJohnson2027/225-lab4-1.git'     
        KUBECONFIG = credentials('john2027-sp26')                           
    }

    stages {
        stage('Checkout') {
            steps {
                cleanWs()
                checkout([$class: 'GitSCM', branches: [[name: '*/main']],
                          userRemoteConfigs: [[url: "${GITHUB_URL}"]]])
            }
        }

        // New Stages Implemented to The Pipeline for 4.3

        stage('Install Python Dependencies') {
            steps {
                sh 'python3 -m pip install -r requirements.txt'
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh 'PYTHONPATH=. python3 -m pytest'
            }
        }

        stage('Security Scan with Bandit') {
            steps {
                sh 'python3 -m bandit -r . || true'
            }
        }

        stage('Dependency Vulnerability Scan') {
            steps {
                sh 'python3 -m pip_audit -r requirements.txt || true'
            }
        }

        // Normal Pipeline Before Any Changes

        stage('Build Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'roseaw-dockerhub') {
                        docker.build("${DOCKER_IMAGE}:${IMAGE_TAG}")
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS_ID}") {
                        docker.image("${DOCKER_IMAGE}:${IMAGE_TAG}").push()
                    }
                }
            }
        }

        stage('Deploy to Dev Environment') {
            steps {
                script {
                    def kubeConfig = readFile(KUBECONFIG)
                    sh "sed -i 's|${DOCKER_IMAGE}:latest|${DOCKER_IMAGE}:${IMAGE_TAG}|' deployment-dev.yaml"
                    sh "kubectl apply -f deployment-dev.yaml"
                }
            }
        }
        
        stage('DAST Security Scan') {
            steps {
                sh '''
                chmod -R 777 $WORKSPACE

                docker run --rm \
                -u root \
                -v $WORKSPACE:/workspace \
                -e BURP_START_URL=http://10.48.228.105 \
                -e BURP_REPORT_FILE_PATH=/workspace/dastardly-report.xml \
                public.ecr.aws/portswigger/dastardly:latest
                '''
            }
        }
        
        stage('Check Kubernetes Cluster') {
            steps {
                script {
                    sh "kubectl get all"
                }
            }
        }
    }

    post {
        success {
            slackSend color: "good", message: "Build Completed: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
        }
        unstable {
            slackSend color: "warning", message: "Build Completed: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
        }
        failure {
            slackSend color: "danger", message: "Build Completed: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
        }
    }
}
