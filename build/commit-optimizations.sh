#!/usr/bin/env bash

while getopts d:t: flag
do
    case "${flag}" in
        d) baseDir=${OPTARG};;
        t) token=${OPTARG};;
    esac
done

echo "[OPTIMIZE][STRATEGIES][COMMITTING]"

setup() {
    git config --global user.email "automation@frostaura.net"
    git config --global user.name "Automation Pipeline"
}

commit() {
    git checkout main
    git add -f "${baseDir}/automation/optimizations/*"
    git commit -m "Automated strategy optimizations."
}

push() {
    dateTime="optimizations-$(date +%s)"
    git remote rm origin
    git remote add origin "https://${token}@github.com/faGH/fa.services.plutus.git" > /dev/null 2>&1
    git tag -a $dateTime -m "Automated optimizations."
    git push origin main --quiet --tags $dateTime
}

setup
commit
push