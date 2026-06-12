#! /bin/bash
curl -X POST http://localhost:8080/scripts/post_body.sh \ -H "Content-Type: text/plain" \ -d @hello_world.txt
