git remote -v
git branch
./gradlew :segmentstore:server:test \
	--continue \
	--rerun-tasks \
	-DmaxParallelForks=$(nproc) \
	-Dlogback.configurationFile=config/logback.xml
