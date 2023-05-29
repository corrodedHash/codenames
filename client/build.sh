npm run build
scp -r dist/ dowebipv4:compose/apps
ssh dowebipv4 "cd compose/apps/; rm -rf apps-docker/apps/codenames; mv dist/ apps-docker/apps/codenames; docker compose up --build -d" 
