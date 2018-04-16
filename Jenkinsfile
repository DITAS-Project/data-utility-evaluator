pipeline {
    // Mandatory to use per-stage agents
    agent none
    stages {
        stage('Build - test') {
            agent {
                docker {
                    image 'python:slim'					
                }
            }
            steps {
                sh 'pip install --no-cache-dir -r requirements.txt'

				// Any artifact? Dont think so
				// TO-DO

                // Run the tests?
				// TO-DO
            }
            // TODO stop if test fails!
            post {
                always {
                    // Record the test report?
                    // TO-DOi
		    echo "To-Do Record tests"
                }
            }
        }

      }
      steps {
        sh 'pip install --no-cache-dir -r requirements.txt'
      }
      post {
        always {
          echo 'To-Do Record tests'

        }

      }
    }
    stage('Image creation') {
      agent any
      steps {
        echo 'Creating the image...'
        sh 'docker build -t "ditas/data-utility-evaluator" -f Dockerfile.artifact .'
        echo 'Done'
        echo 'Retrieving Docker Hub password from /opt/ditas-docker-hub.passwd...'
        script {
          password = readFile '/opt/ditas-docker-hub.passwd'
        }

        echo 'Done'
        echo 'Login to Docker Hub as ditasgeneric...'
        sh "docker login -u ditasgeneric -p ${password}"
        echo 'Done'
        echo 'Pushing the image ditas/data-utility-evaluator:latest...'
        sh 'docker push ditas/data-utility-evaluator:latest'
        echo 'Done '
      }
    }
    stage('Image deploy') {
      agent any
      steps {
        sh 'ssh -i /opt/keypairs/ditas-testbed-keypair.pem cloudsigma@31.171.247.162 sudo docker rm -f data-utility-evaluator || true'
        sh 'ssh -i /opt/keypairs/ditas-testbed-keypair.pem cloudsigma@31.171.247.162 sudo docker pull ditas/data-utility-evaluator:latest'
        sh 'ssh -i /opt/keypairs/ditas-testbed-keypair.pem cloudsigma@31.171.247.162 sudo docker run -p 50002:8080 -d --name data-utility-evaluator ditas/data-utility-evaluator:latest'
      }
    }
  }
}
