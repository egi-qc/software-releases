#!/usr/bin/groovy

def json_release_file = ''

pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile.build'
        }
    }
    stages {
        stage('Identify release changes') {
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
                println('Run script that gets the list of packages')
            }
        }
    }
}
