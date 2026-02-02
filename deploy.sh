echo "Select environment:"
echo "1) Staging"
echo "2) Production"
read -p "Enter choice [1 or 2]: " choice

case $choice in
    1)
        ENVIRONMENT="staging"
        ;;
    2)
        ENVIRONMENT="production"
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo "Exporting env vars into the shell environment"
export $(grep -v '^#' .env.$ENVIRONMENT | xargs)

# echo "Printing Kamal Secrets on the screen"
# kamal secrets print

echo "Deploying to ${ENVIRONMENT^}"
#kamal setup -d $ENVIRONMENT
kamal deploy -d $ENVIRONMENT
