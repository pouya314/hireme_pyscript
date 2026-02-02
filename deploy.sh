#!/bin/bash

echo "Select environment:"
echo "1) Staging"
echo "2) Production"
read -p "Enter choice [1 or 2]: " choice

case $choice in
    1)
        ENVIRONMENT="staging"
        DISPLAY_NAME="Staging"
        ;;
    2)
        ENVIRONMENT="production"
        DISPLAY_NAME="Production"
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

echo "Deploying to $DISPLAY_NAME"
#kamal setup -d $ENVIRONMENT
kamal deploy -d $ENVIRONMENT
