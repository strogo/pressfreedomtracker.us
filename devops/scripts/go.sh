#!/bin/bash
#
#

set -e

curdir="$(dirname $(realpath "$0") )"

source .docker_versions

if [ "$1" != "only_tests" ]; then
    echo "##### Run sass linter"
    # Start sasslinter container, have to get a little hacky
    # since its running on a remote docker instance

    # idempotency check...
    docker kill sasslint &> /dev/null || true
    docker rm sasslint &> /dev/null || true

    # Run sasslint as a long-running container (hence the tail hack)
    docker run -d --entrypoint=/bin/ash --name sasslint "${SASSLINT_IMAGE}@sha256:${SASSLINT_VER}" -c 'tail -f /dev/null' &> /dev/null
    # This bit can take a while :(
    echo "Copying git directory to remote docker container..."
    docker cp "${PWD}" sasslint:/lintme
    docker exec -it sasslint ash -c 'cd /lintme && /usr/local/bin/sass-lint -v'
fi

# Ensure virtualenv activated and ansible roles installed
"${curdir}/env-startup"
source "${curdir}/../.venv/bin/activate"

# Ensure we are in the devops directory
cd "$(dirname $(dirname $(realpath $0) )../)"|| exit

echo "##### Pull Docker Image"
docker pull "${CIWWW_IMAGE}@sha256:${CIWWW_VER}" &> /dev/null
# molecule needs a tag to import
docker tag "${CIWWW_IMAGE}@sha256:${CIWWW_VER}" "${CIWWW_IMAGE}:latest"
echo "##### Run Django provision"
if [ "$1" != "only_tests" ]; then
    molecule create
    molecule converge
fi

echo "##### Run Testinfra pieces"
testinfra --connection=docker --hosts=prod tests/