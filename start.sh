#!/usr/bin/env bash

namespace=''
port=8000

while [[ $# -gt 0 ]]
do
  key="$1"

  case $key in
      -n|--namespace)
      if ! command -v gsed &> /dev/null; then
        echo "gsed is required for this option"
        echo "try 'brew install gsed' if you have homebrew installed"
        exit 1
      fi
      namespace="$2"
      shift
      shift
      ;;
      -p|--port)
      port="$2"
      shift
      shift
      ;;
      -h|--help)
      echo "start.sh [OPTIONS]"
      echo ""
      echo "  -n, --namespace   API namespace to mock"
      echo ""
      echo "  -p, --port        Port to listen on (default: 8000)"
      echo ""
      shift
      exit
      ;;
      *)
      shift
      ;;
  esac
done


if [ -n "$namespace" ]; then
  gsed -ri "s|^(\s*ENGINE_NAMESPACE\s*=\s*)(.*)|\1'${namespace}'|" ./turmoe/settings.py
fi

python3 ./manage.py runserver $port
