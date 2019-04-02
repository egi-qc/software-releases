#!/usr/bin/groovy

@Library(['github.com/indigo-dc/jenkins-pipeline-library']) _


def yaml_release_file = ''

pipeline {
    agent {
        label 'python'
    }
    stages {
        stage('Fetch code') {
            steps {
                checkout scm
            }
        }
        
        stage('Identify release changes') {
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
        stage('Validate YAML release file') {
            when {
                expression {
                    yaml_release_file
                }
            }
            steps {
                println(yaml_release_file)
                sh('pip install -r requirements.txt')
                sh("python ppagen.py ${yaml_release_file}")
            }
            post {
                success {
                    archiveArtifacts '*.xml'
					script {
                        xml_metadata_file = sh(
                            returnStdout: true,
                            script: "python ppagen.py --get-ppa-file --do-not-validate ${yaml_release_file}")
                        path_tokens = yaml_release_file.tokenize('/')
                        distribution_type = path_tokens[1]
                        release_no = path_tokens[2]
                        submitToRT(
                            xml_metadata_file,
                            distribution_type,
                            release_no)
                    }
                }
            }
        }
    }
}

void submitToRT(
        String release_metadata_filename,
        String distribution_type,
        String release_no) {
    def python_cmd = "python -c 'import urllib2 ; print urllib2.quote(\"\"\"id: ticket/new\\nQueue: sw-rel\\nSubject: dummy-test\\nCF.{Distribution Type}: ${distribution_type}\\nCF.{UMDRelease}: ${release_no}\\nCF.{ReleaseMetadataURL}: ${env.BUILD_URL}/artifact/${release_metadata_filename}\"\"\")'"
    def content = sh returnStdout: true, script: "${python_cmd}"
    println("URL ENCODED: ${content}")
    def response = httpRequest authentication: 'egi-rt-creds',
                               customHeaders: [[maskValue: false, name: 'Content-type', value: 'text/plain; charset=utf-8']], 
                               httpMode: 'POST',
                               responseHandle: 'NONE',
                               //url: "https://rt.egi.eu/rt/REST/1.0/ticket/new?content=id%3A+ticket%2Fnew%0AQueue%3A+sw-rel"
                               url: "https://rt.egi.eu/rt/REST/1.0/ticket/new?content=${content}",
                               consoleLogResponseBody: true
}
