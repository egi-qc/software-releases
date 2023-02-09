#!/usr/bin/groovy

def json_release_file = ''
def String[] pkg_list = []
def download_dir = ''
def pkgs_signed = ''

pipeline {
    environment {
        GPG_PRIVATE_KEY = credentials('6e2f2e3c-9368-4aae-b017-a5bae4591ce4')
        GPG_PRIVATE_KEY_PASSPHRASE = credentials('d8ec011f-236a-404e-a6cb-ac6f9adfae82')
	GPG_PUBLIC_KEY = credentials('eef6cd3d-b410-489d-86fb-349a53abe498')
    }

    agent {
        dockerfile {
            filename 'Dockerfile.build'
        }
    }
    stages {
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
                            download_dir = sh(
                                returnStdout: true,
                                script: "python3 download_pkgs.py ${json_release_file} 0"
                            ).trim()
                            println(download_dir)
                        }
                    }
                }
            }
        }

        stage('Add UMD GPG key'){
            when {
                expression {return download_dir}
            }
            steps {
		println('Importing private GPG key')
                sh "gpg --import --batch --yes $GPG_PRIVATE_KEY"
                sh 'gpg --list-keys'
		println('Importing public GPG key for RPM')
                sh "sudo rpm --import $GPG_PUBLIC_KEY"
                sh "rpm -q gpg-pubkey --qf '%{name}-%{version}-%{release} --> %{summary}\n'"
                sh "sed -i \"s/--passphrase ''/--passphrase '$GPG_PRIVATE_KEY_PASSPHRASE'/g\" ~/.rpmmacros"
                dir('scripts') {
                    script {
                        pkgs_signed = sh(
                            returnStdout: true,
                            script: "./rpm_sign.sh ${download_dir} 0"
                        ).trim()
                    	println(pkgs_signed)
                        sh "./rpm_sign.sh ${download_dir} 1"
                    }
                }
            }
        }
    }
}
