let config = { environment: 'dev', distributionTypes : ['umd','cmd-os','cmd-one'], distributionsId : { 'umd': [4,5],'cmd-os':[0,1],'cmd-one':[0,1]} };

let umdVersions = { current: 'umd-4', future: 'umd-5', past: ['umd-3','umd-2','umd-1'] };

let softwareCatalogTxt = { description: 'Este texto é do catálogo de sooftware.' };

let yumNotes = `
        <h5>UMD-4 Yum Repositories</h5>
        <br>

        <h6><i class="fas fa-info-circle"></i> Installation</h6>

        <ol class="notes" style="/*margin-left:20px;*/overflow-wrap: break-word;font-size:small;">
                <li>Install the Yum priorities package:
                        <ul>
                            <li class="command">yum install yum-plugin-priorities</li>
                        </ul>
                </li>

                <li>
                        Install Epel repositories
                        <ul>
                                <li class="command">yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm</li>
                        </ul>
                        Epel repositoires should have either no priority setting, or a priority setting that is 99 or higher
                </li>

                <li>Install UMD-4 Repositories
                        <ul>
                                <li class="command">yum install http://repository.egi.eu/sw/production/umd/4/centos7/x86_64/updates/umd-release-4.1.3-1.el7.centos.noarch.rpm</li>
                        </ul>
                        UMD repositories should always have priority higher than EPEL
                </li>
        </ol>


        <br>


        <h6>Configuration</h6>

        <ul class="notes" style="font-size:small;">
                <li>UMD-4 repository is composed by 4 releases:
                        <ul>
                                <li>UMD-4-base.repo</li>
                                <li>UMD-4-testing.repo</li>
                                <li>UMD-4-untested.repo</li>
                                <li>UMD-4-updates.repo</li>
                        </ul>
                </li>
        </ul>

        <p>Base and updates are enabled by default: enable=1. If you want to enable another (e.g. testing) you should change enable from 0 to 1.</p>
        `;