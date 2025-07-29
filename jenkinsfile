pipeline {
    agent any

    environment {
        REMOTE_USER = 'root'
        REMOTE_IP = '192.168.64.5'
        PRIVATE_KEY = '/var/jenkins_home/pvt_key'
        REMOTE_DIR = '/home/ubuntu/mlops-translation-app/ansible'
        ANSIBLE_COMMAND = 'ansible-playbook -i inventory.ini blue_green_deploy.yml'
    }

    stages {
        stage('Trigger Remote Ansible Deployment') {
            steps {
                sh '''
                #!/bin/bash

                echo "Starting remote Ansible deployment..."

                ssh -o StrictHostKeyChecking=no -i "$PRIVATE_KEY" ${REMOTE_USER}@${REMOTE_IP} "cd $REMOTE_DIR && $ANSIBLE_COMMAND"
                '''
            }
        }
    }
}
