#!/bin/sh

if [ "$NODE_ENV" = "production" ]; then
  npx serve -s build -l 3000
else
  npm start
fi

