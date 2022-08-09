#!/usr/bin/groovy

def yaml_release_file = ''

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
                    yaml_files_changed = []
                    last_commit.split('\n').each {
                        if (it.contains('.yaml')) {
                            yaml_files_changed.add(it)
                        }
                    }
                    if (yaml_files_changed.size() == 0) {
                        println('No changes detected to any YAML release files')
                    }
                    else if (yaml_files_changed.size() > 1) {
                        println('More than one modified YAML release file found. Please commit one YAML at a time')
                    }
                    else {
                        println("Changes to ${yaml_files_changed[0]} found. Processing file..")
                        yaml_release_file = yaml_files_changed[0]
                    }
                }
            }
        }
    }
}
