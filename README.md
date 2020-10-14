# faster-pravega-builds

A tool that helps do two things:
* Use docker to help both isolate builds and create a way to easily adjust the available resources to a deployment to help minmic TravisCI runs locally.
* Tabulate data about failed/skipped tests.

Run `python3 run.py --help` to list the available parameters.

Deployment:

* Clone your `pravega` fork as a directory named 'pravega'.
* You place the command(s) you want to execute in `cmd` (Assumes that a `test` task will be run).
* Build the Dockerfile: `docker build -t faster-builds` (Assumes the image will be tagged as `faster-builds`) 
* Run `./run.sh`

Example:

```
$ git clone https://github.com/co-jo/faster-pravega-builds.git
$ cd faster-pravega-builds
$ git clone https://github.com/co-jo/pravega.git
$ docker build -t faster-builds .
$ ./run.sh
```
