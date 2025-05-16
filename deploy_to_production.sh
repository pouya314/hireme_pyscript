echo "Exporting env vars into the shell environment"
export $(grep -v '^#' .env.production | xargs)

echo "Printing Kamal Secrets on the screen"
kamal secrets print

echo "Deploying to Production"
