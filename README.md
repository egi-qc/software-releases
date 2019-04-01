# Trigger validation of new software releases for EGI UMD and CMD distributions

This repository hosts the latest software product release versions being
validated by the EGI QC team.

## Submit a new release for a specific software product

### Instructions for software providers (aka Product Teams)

1. Fork the repository to submit the change
2. Find the YAML release template under for your software component under the
`products` directory. If not there, create one.
3. Add/edit the relevant information including:
 - Version of the software
 - Software package URLs for each distribution being supported
 - Release notes URL
 - Changelog
4. (single) Commit changes and submit the pull request

_Note: Once the pull request is accepted,
[Jenkins](https://jenkins.egi.ifca.es) will carry out the software validation
process. Only the last commit (from HEAD) is considered, so please be sure to
include the YAML file changes as part of the last commit_

### Instructions for EGI QC team

When reviewing the pull request, there are two main requirements that need to
be enforced:

1. Availability of the following mandatory fields:
 - Version of the software
 - Software package URLs for each distribution being supported
 - Release notes URL
 - Changelog
2. Last commit contains changes to the relevant YAML product file.

_Only approve the pull request whenever the two former requirements are
satisfied. Otherwise request changes to the submitter (software provider)_
