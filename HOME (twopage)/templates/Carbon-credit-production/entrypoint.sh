#!/bin/sh

NPM_COMMAND=$1

yarn install
yarn run build

yarn run $NPM_COMMAND