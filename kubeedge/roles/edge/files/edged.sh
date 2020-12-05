#!/bin/bash
_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )
_LOCAL=$( cd "$_DIR/.." && pwd )
#source $_HOME/.bash_profile
export CHECK_EDGECORE_ENVIRONMENT=false
$_LOCAL/bin/edgecore --config $_LOCAL/etc/edgecore.yaml

