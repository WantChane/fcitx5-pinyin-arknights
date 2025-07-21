#!/usr/bin/env bash

log() {
    local msg
    case "$1" in
        "INFO") 
            msg="\033[1;34m[INFO]\033[0m ${2}"
            ;;
        "WARN") 
            msg="\033[1;33m[WARN]\033[0m ${2}"
            ;;
        "ERROR") 
            msg="\033[1;31m[ERROR]\033[0m ${2}"
            ;;
        "SUCCESS") 
            msg="\033[1;32m[SUCCESS]\033[0m ${2}"
            ;;
        "DEBUG") 
            msg="\033[1;35m[DEBUG]\033[0m ${2}"
            ;;
        *) 
            msg="${@}"
            ;;
    esac
    
    timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    echo -e "[${timestamp}] ${msg}"
}

info() {
    log "INFO" "$1"
}

warn() {
    log "WARN" "$1"
}

error() {
    log "ERROR" "$1"
}

success() {
    log "SUCCESS" "$1"
}

debug() {
    log "DEBUG" "$1"
}

