#!/usr/bin/env bash
set -e

# clean up the flask server process on exit
function finish {
    if [ -n "$flask_pid" ]; then
	kill "$flask_pid"
    fi
}
trap finish EXIT

# src_base="~/opt"
src_base="$HOME/src/cran-server"

package_tgz='httr_1.3.1.tar.gz'
host='localhost'
port='8081'

url="http://$host:$port"

# set environment variables for flask
export FLASK_APP="$src_base/cranserver/server.py"
export PYTHONPATH="$src_base/cranserver/"
export CRANSERVER_FS_LOC="$HOME/cran"

# make sure we have a directory to save packages to
mkdir -p "$CRANSERVER_FS_LOC/src/contrib/"

# spin up the server
flask run -p "$port" &
flask_pid=$!

sleep 3

curl "$url/src/contrib/PACKAGES" > PACKAGES

# download a package for install
curl --fail -O "https://cran.r-project.org/src/contrib/$package_tgz"

# post the package to the server
curl --fail -i -X POST -F file=@"$package_tgz" "$url" &&
    # clean up the package
    rm "$package_tgz"

# finally, install the package, using R
Rscript -e "install.packages('httr', repos = '$url')"
