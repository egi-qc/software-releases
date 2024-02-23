#!/usr/bin/groovy

// Product validation
def json_release_file = ''
def String[] pkg_list = []
def download_dir = ''
def pkgs_signed = ''
def pkgs_upload = ''
def dst_type = ''
def dst_version = ''
def platform = ''
def arch = ''
def pkg_names = ''
def validation_job_status = ''

// RC validation
def release_candidate_job_status = ''
def String[] extra_repository = []


pipeline {
    environment {
        GPG_PRIVATE_KEY = credentials('327d4c0c-baae-458a-b1b6-21a256974c41')
        GPG_PRIVATE_KEY_PASSPHRASE = credentials('749515f4-4938-4034-aa5c-fb4839b4b4bf')
        GPG_PUBLIC_KEY = credentials('901f6bce-3b15-4fe0-8cc8-b96fe2807fe3')
        NEXUS_CONFIG = credentials('ecfb20e4-0c97-48e3-9e36-50e42b0e59f1')
        REPO_RPM_SIGN_GPGNAME = credentials('7e5e4b45-1c9a-454e-8148-8c5fdc7f7faf')
    }

    agent {
        dockerfile {
            filename 'Dockerfile.build'
        }
    }
    stages {
        stage('Detect release changes') {
            when {
                anyOf {
                    changeRequest target: 'testing/umd4'
                    changeRequest target: 'production/umd4'
                }
            }
            steps {
                script {
                    last_commit = sh(
                        returnStdout: true,
                        script: 'git diff-tree --name-only --no-commit-id -r HEAD^1').trim()
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

        stage('Get release info') {
            when {
                expression {return json_release_file}
            }
            steps {
                dir('scripts') {
                    script {
                        def release_info = sh(
                            returnStdout: true,
                            script: "python3 json_parser.py ${json_release_file} 2"
                        ).trim()
                        (dst_type, dst_version, platform, arch) = release_info.split(' ')
                        pkg_names = sh(
                            returnStdout: true,
                            script: "python3 json_parser.py ${json_release_file} 3"
                        ).trim()
                    }
                }
            }
        }

        stage('Collect the list of packages') {
            when {
                allOf {
                    changeRequest target: 'testing/umd4'
                    expression {return json_release_file}
                }
            }
            steps {
                dir('scripts') {
                    withPythonEnv('python3') {
                        script {
                            sh(
                                returnStdout: true,
                                script: "python3 json_parser.py ${json_release_file} 0"
                            ).trim()
                        }
                    }
                }
            }
        }

        stage('Download the packages to a temporary directory') {
            when {
                allOf {
                    changeRequest target: 'testing/umd4'
                    expression {return json_release_file}
                }
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
                expression { return download_dir }
            }
            steps {
                println('Importing private GPG key')
                sh "gpg --import --batch --yes $GPG_PRIVATE_KEY"
                sh 'gpg --list-keys'
                println('Importing public GPG key for RPM')
                sh "rpm -q gpg-pubkey --qf '%{name}-%{version}-%{release} --> %{summary}\n'"
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

        stage('Upload packages to testing'){
            when {
                expression { return download_dir }
            }
            steps {
                dir('scripts') {
                    script {
                        pkgs_upload = sh(
                            returnStdout: true,
                            script: "python3 upload_pkgs.py ${json_release_file} 0" + ' ${NEXUS_CONFIG}'
                        ).trim()
                        println(pkgs_upload)
                    }
                }
            }
        }

        stage('Trigger validation'){
            when {
                expression {return pkgs_upload}
            }
            steps {
                script {
                    def pkg_install_job = build job: 'QualityCriteriaValidation/package-install',
                                          parameters: [
                                              string(name: 'Release', value: "${dst_type}${dst_version}"),
                                              text(name: 'OS', value: "$platform"),
                                              text(name: 'Packages', value: "$pkg_names"),
                                              booleanParam(name: 'enable_verification_repo', value: true),
                                              booleanParam(name: 'enable_testing_repo', value: true),
                                              booleanParam(name: 'enable_untested_repo', value: false),
                                              booleanParam(name: 'disable_updates_repo', value: false)
                                          ]
                    validation_job_status = pkg_install_job.result
                }
            }
        }

        stage('Generate JSON release file') {
            when {
                allOf {
                    expression {return json_release_file}
                }
            }
            steps {
                dir('scripts') {
                    script {
                        pkg_list = sh(
                            returnStdout: true,
                            script: "python3 json_parser.py ${json_release_file} 1"
                        ).trim()
                    }
                    archiveArtifacts artifacts: 'release.json', followSymlinks: false
                }
            }
        }

        //
        // Production branch (RC validation)
        //
        stage('Trigger Release Candidate validation'){
            when {
                changeRequest target: 'production/umd4'
            }
            steps {
                script {
                    def release_candidate_job = build job: 'QualityCriteriaValidation/release-candidate',
                                                    parameters: [
                                                        string(name: 'Release', value: "UMD4"),
                                                        text(name: 'Extra_repository', value: "$extra_repository")
                                                    ]
                    release_candidate_job_status = release_candidate_job.result
                }
            }
        }

        stage('Upload packages to production'){
            when {
                allOf {
                    changeRequest target: 'production/umd4'
                    expression { return download_dir }
                    equals expected: 'SUCCESS', actual: release_candidate_job_status
                }
            }
            steps {
                dir('scripts') {
                    script {
                        pkgs_upload = sh(
                            returnStdout: true,
                            script: "python3 upload_pkgs.py ${json_release_file} 1" + ' ${NEXUS_CONFIG}'
                        ).trim()
                        println(pkgs_upload)
                    }
                }
            }
        }

    }
}
