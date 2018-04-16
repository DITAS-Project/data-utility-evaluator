pipeline {
    // Mandatory to use per-stage agents
    agent none
    stages {
        stage('Build - test') {
            agent {
                docker {
                    image 'python:slim'
					// TODO some cache to avoid npm sintall on every execution?
                }
            }
            steps {
                sh 'pip3 install --no-cache-dir -r requirements.txt'

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
        stage('Image creation') {
            agent any
            steps {
                // The Dockerfile.artifact copies the code into the image and run the jar generation.
                echo 'Creating the image...'
                // This will search for a Dockerfile.artifact in the working directory and build the image to the local repository
                sh "docker build -t \"ditas/data-utility-evaluator\" -f Dockerfile.artifact ."
                echo "Done"
                echo 'Retrieving Docker Hub password from /opt/ditas-docker-hub.passwd...'
                // Get the password from a file. This reads the file from the host, not the container. Slaves already have the password in there.
                script {
                    password = readFile '/opt/ditas-docker-hub.passwd'
                }
                echo "Done"
                echo 'Login to Docker Hub as ditasgeneric...'
                sh "docker login -u ditasgeneric -p ${password}"
                echo "Done"
                echo "Pushing the image ditas/data-utility-evaluator:latest..."
                sh "docker push ditas/data-utility-evaluator:latest"
                echo "Done "
            }
        }
        stage('Image deploy') {
            // TO-DO avoid downloading the source from git again, not neccessary. (All the stages do that unnecessary step at this moment, see logs)
            agent any
            steps {
                // Staging environment: 31.171.247.162
                // Private key for ssh: /opt/keypairs/ditas-testbed-keypair.pem

                // TODO move all these commands to a deploy.sh to open a single SSH connetions
                // TODO state management? We are killing without careing about any operation the conainer could be doing.

                // Ensure that a previously running instance is stopped (-f stops and removes in a single step)
                // || true - "docker stop" failt with exit status 1 if image doen't exists, what makes the Pipeline fail. the "|| true" forces the command to exit with 0.
                sh 'ssh -i /opt/keypairs/ditas-testbed-keypair.pem cloudsigma@31.171.247.162 sudo docker rm -f data-utility-evaluator || true'

                // Ensure that the last image is pulled
                sh 'ssh -i /opt/keypairs/ditas-testbed-keypair.pem cloudsigma@31.171.247.162 sudo docker pull ditas/data-utility-evaluator:latest'

                // Run and name the image to allow stopping by name
                sh 'ssh -i /opt/keypairs/ditas-testbed-keypair.pem cloudsigma@31.171.247.162 sudo docker run -p 50002:8080 -d --name data-utility-evaluator ditas/data-utility-evaluator:latest'
            }
        }
    }
}