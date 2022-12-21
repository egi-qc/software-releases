#!/usr/bin/groovy

def json_release_file = ''
def String[] pkg_list = []

pipeline {
    environment {
        GPG_PRIVATE_KEY = credentials('6e2f2e3c-9368-4aae-b017-a5bae4591ce4')
    }

    agent {
        dockerfile {
            filename 'Dockerfile.build'
            // args '-e GPG_PRIVATE_KEY'
        }
    }
    stages {
        stage('Print env'){
            steps {
                sh 'env'
            } 
        }
        stage('Add UMD GPG key'){
            steps {
                // sh 'echo "$GPG_PRIVATE_KEY" > ~/private-key.pem'
                // sh 'cat  ~/private-key.pem'
                sh "gpg --import --batch --yes $GPG_PRIVATE_KEY"
                sh 'gpg --list-keys'
            }
        }
	/*
        stage('Install dependencies') {
            steps {
                withPythonEnv('python3') {
                   sh 'pip3 install --user -r requirements.txt'
                }
            }
        }
        stage('Detect release changes') {
            when {
                branch 'master'
            }
            steps {
                script {
                    last_commit = sh(
                        returnStdout: true,
                        script: 'git diff-tree --name-only --no-commit-id -r HEAD').trim()
                    json_files_changed = []
                    last_commit.split('\n').each {
                        if (it.contains('.json')) {
                            json_files_changed.add(it)
                        }
                    }
                    if (json_files_changed.size() == 0) {
                        println('No changes detected to any JSON release file')
                    }
                    else if (json_files_changed.size() > 1) {
                        currentBuild.result = 'ABORTED'
                        error('More than one modified JSON release file found. Please commit one JSON at a time')
                    }
                    else {
                        println("Changes to ${json_files_changed[0]} found. Processing file..")
                        json_release_file = json_files_changed[0]
                    }
                }
            }
        }

        stage('Collect the list of packages') {
            when {
                expression {return json_release_file}
            }
            steps {
                dir('scripts') {
                    withPythonEnv('python3') {
                        script {
                            pkg_list = sh(
                                returnStdout: true,
                                script: "python3 json_parser.py ${json_release_file}"
                            ).trim()
                        }
                    }
                }
            }
        }

        stage('Download the packages to a temporary directory') {
            when {
                expression {return pkg_list}
            }
            steps {
                dir('scripts') {
                    withPythonEnv('python3') {
                        script {
                            download_output = sh(
                                returnStdout: true,
                                script: "python3 download_pkgs.py ${json_release_file} 0"
                            ).trim()
                        }
                    }
                }
            }
        }
        */
    }
}
