# Discord Backup Bot

This bot allows you to create, list, retrieve, and delete server backups in Discord. It uses Discord's `discord.py` library to interact with Discord's API and handle commands.

## Features

- **Create Backup**: Create a server template link and save it to a file with optional images.
- **List Backups**: List all public server backups with their backup codes.
- **Get Backup Information**: Retrieve detailed information about a backup using the backup code.
- **Delete Backup**: Delete the backup for the current server.

## Setup

### Prerequisites

- Python 3.8 or higher
- `discord.py` library (version 2.4.0 or higher)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/your-repository.git
   cd your-repository
   ```

2. Install the required packages:
   ```bash
   pip install discord.py
   ```

### Configuration

1. Replace the `bot.run('YOUR_BOT_TOKEN')` line with your Discord bot token in the script.

2. Ensure your bot has the necessary permissions to manage servers and create templates.

## Commands

### `/backup`
Create a server template link and save it to a file.

- **privacy**: Set the privacy of the backup link (`public` or `private`).
- **image1**: Optional URL of the first image.
- **image2**: Optional URL of the second image.
- **image3**: Optional URL of the third image.

### `/list_backups`
List all public server backups with their backup codes.

### `/get_backup_info`
Retrieve information about a backup using the backup code.

- **code**: The backup code.

### `/delete_backup`
Delete the backup for the current server.

## Code Explanation

- `generate_random_code(length=8)`: Generates a random alphanumeric code.
- `on_ready()`: Prints a message when the bot is ready and attempts to sync commands.
- `backup(interaction, privacy, image1, image2, image3)`: Creates a backup of the server and saves it to a file.
- `BackupView`: A custom view for pagination of backup listings.
- `list_backups(interaction)`: Lists all public backups with pagination.
- `get_backup_info(interaction, code)`: Sends backup information to the user's private messages.
- `delete_backup(interaction)`: Deletes the backup for the current server.

## Running the Bot

Run the bot using the following command:
```bash
python bot.py
```

Replace `bot.py` with the filename of your script if different.

## Notes

- Ensure your bot token is kept secret and not exposed in public repositories.
- Adjust permissions and intents as necessary for your bot's needs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
