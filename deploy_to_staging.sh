echo "Exporting env vars into the shell environment"
export $(grep -v '^#' .env.staging | xargs)

echo "Printing Kamal Secrets on the screen"
kamal secrets print

echo "Deploying to Staging"
#kamal setup -d staging
kamal deploy -d staging