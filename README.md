# faster-pravega-builds

A tool that helps do two things:
* Use docker to help both isolate builds and create a way to easily adjust the available resources to a deployment to help minmic TravisCI runs locally.
* Tabulate data about failed/skipped tests.

Run `python3 run.py --help` to list the available parameters. 

Deployment:

* Clone your `pravega` fork as a directory named 'pravega'.
* You place the command(s) you want to execute in 'cmd'.
* Build the Dockerfile: `docker build -t <tag> .`
* Run `./run.sh`
