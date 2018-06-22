#!/bin/bash

echo ""
echo "Building docker image"
echo "---------------------"

# Default parameters
#
IMAGE_TAG='rhoai/healthchecker'
RHO_PUSH_VERSION=''
EXTRA_INDEX_URL=''
DEV_MODE=false
DOCKER_FILE='Dockerfile.tmpl'

# Custom die function
#
die() { echo >&2 -e "\nRUN ERROR: $@\n"; usage; exit 1; }

usage()
{
cat << EOF
usage: ./build.sh -i -v [-t] [-h]

  OPTIONS:
  -h        Show this message
  -d        Dev mode
  -i        The PyPi server url. (Required)
  -t        The image tag name. Defaults to $IMAGE_TAG
  -v        Version of healthchecker to install
EOF
}

# Parse the command line flags.
#
while getopts "hdi:t:v:" opt; do
  case $opt in
    h)
      usage
      exit 1
      ;;
    d)
      DEV_MODE=true
      DOCKER_FILE='Dockerfile-dev.tmpl'
      ;;
    i)
      EXTRA_INDEX_URL=${OPTARG}
      ;;
    t)
      IMAGE_TAG=${OPTARG}
      ;;
    v)
      HEALTHCHECKER_VERSION=${OPTARG}
      ;;
    \?)
      die "Invalid option: -$OPTARG"
      ;;
  esac
done

if [ -z "${EXTRA_INDEX_URL}" -a $DEV_MODE == false ]; then
    die "Please specify the EXTRA_INDEX_URL"
fi

if [ -z "${HEALTHCHECKER_VERSION}" ]; then
    die "Please specify the version of healthchecker to install"
fi

# Create the build directory
rm -rf build
mkdir build

cp run.sh build/

if [ $DEV_MODE == true ]; then
    DIR=`pwd`
    cp ../dist/$HEALTHCHECKER_VERSION build/
else
    HEALTHCHECKER_VERSION="==${HEALTHCHECKER_VERSION}"
fi

# Copy docker file, and override the EXTRA_INDEX_URL
sed 's|%%EXTRA_INDEX_URL%%|'"$EXTRA_INDEX_URL"'|g' $DOCKER_FILE > build/Dockerfile

docker build -t="${IMAGE_TAG}" --build-arg HEALTHCHECKER_VERSION=$HEALTHCHECKER_VERSION build/
