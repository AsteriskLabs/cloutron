Cloutron
========

Cloutron is an extensible terminal UI for cloud-hackers. It allows you to attach utility views running in other terminals to monitor your AWS cloud services, displaying helpful information such as available instances, databases, load-balancers etc, while giving you teh sense that you're being busy by having lots of terminal panes open showing colourful cloudie things.

Cloutron also provides a platform on which to build your own UI views, requesting and processing data from potentially any API to suit your own requirements. Cloutron is pretty much just a terrible hack and slash of the fantastic [Voltron](https://github.com/snare/voltron) tool from [@snare](https://twitter.com/snare). (He built an amazing tool, I raided his view / plugin / configuration functionality)

Support
-------

`cloutron` is built primarily for Amazon's Web Services (AWS). But, there's no reason why it can't have views added for DigitalOcean etc.

The following cloud-platforms are supported:

|                 | supported |
|-----------------|-----------|
| aws ec2         |   √       |
| aws rds         |   √       |
| aws elb         |   √       |
| aws autoscale   |   √       |
| aws codedeploy  |   √       |


Installation
------------

First you need to install snare's Scruffy version 0.2.1

    # wget -O scruffy-0.2.1.tar.gz https://github.com/snare/scruffy/tarball/v0.2.1#egg=scruffy
    # tar -zxvf scruffy-0.2.1.tar.gz
    # cd snare-scruffy-3c26a5a/ (Or whatever the folder name is here)
    # python setup.py install

A standard python setup script is included. And will automatically install other dependencies.

    # cd cloutron-install-folder/
    # python setup.py install

This will install the `cloutron` egg wherever that happens on your system, and an executable named `cloutron` to `/usr/local/bin/`.

Quick Start
-----------

1. Cloutron uses `boto` for interfacing with AWS, so refer to the [boto config](http://docs.pythonboto.org/en/latest/boto_config_tut.html) on how to configure your AWS credentials. We recommend creating a new IAM user with only 'describe' permissions for better security!

2. In a single terminal (or a bunch of tmux panes or iTerm panes) start the cloutron views that you want:

        $ cloutron view ec2instances
        $ cloutron view elasticloadbalancers
        $ cloutron view relationaldatabases
        $ cloutron view autoscale
        $ cloutron view codedeploy

3. These can be shortcutted to:

        $ cloutron v i
        $ cloutron v e
        $ cloutron v r
        $ cloutron v a
        $ cloutron v c

4. Runtime options can be seen by running:

        $ cloutron v i -h

        This allows the configuration of options such as polling frequency (defaults to 60 seconds) and AWS Region (defaults to us-east-1)

Bugs
----

See the [issue tracker](https://github.com/asterisklabs/cloutron/issues) on github.

License
-------

As this is mostly snare's work, his license below is still in place, and if you feel the need, also buy me a beer. The original Voltron license is here:
This software is released under the "Buy snare a beer" license. If you use this and don't hate it, buy me a beer at a conference some time. This license also extends to other contributors - [richo](http://github.com/richo) definitely deserves a few beers for his contributions.

Credits
-------

Thanks to snare at Azimuth Security for creating Voltron, and for spending time chatting with me about it and letting me rip it to shreds.

Also, props to [richo](http://github.com/richo) for all his contributions to Voltron.

Also thanks to Asterisk for being such a cloudy company.
