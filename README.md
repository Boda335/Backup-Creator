# Discord Backup Bot

## Overview

The Discord Backup Bot is designed to help server administrators create, manage, and restore server backups. It allows users to generate server templates, store backup data, list public backups, and restore servers using backup codes. The bot uses Discord's interactions and views to provide a user-friendly experience for managing server backups.

## Features

- **Create Backups**: Generate a server template and store its details, including privacy settings and optional images.
- **List Backups**: View a list of all public backups with their details.
- **Restore Backups**: Retrieve backup information using a backup code.
- **Delete Backups**: Remove backups associated with the current server.

## Commands

### `/backup`
Create a server backup and store the template link and related information.

**Parameters:**
- `privacy` (string): Privacy setting for the backup link ("public" or "private").
- `image1` (string, optional): URL of the first image to include.
- `image2` (string, optional): URL of the second image to include.
- `image3` (string, optional): URL of the third image to include.

**Example Usage:**

```
/backup privacy: <public> image1:<IMG_URL1> image2:<IMG_URL2> image3:<IMG_URL3>
```


### `/list_backups`
List all public server backups with their backup codes.

**Usage:**
```
/list_backups
```

**Note:** Displays the backups in pages with "Previous" and "Next" buttons.

### `/restore`
Retrieve backup information using a backup code.

**Parameters:**
- `code` (string): Backup code for the server.

**Example Usage:**
```
/restore code: ABC123
```

### `/delete_backup`
Delete the backup associated with the current server.

**Usage:**
```
/delete_backup
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-repo/discord-backup-bot.git
   ```

2. Navigate to the project directory:
   ```
   cd discord-backup-bot
   ```

3. Install the required packages:
   ```
   pip install discord.py
   ```

4. Update the bot token in the script (`bot.run('YOUR_BOT_TOKEN')`).

5. Run the bot:
   ```
   python bot.py
   ```

## Configuration

- **Bot Token**: Replace `'YOUR_BOT_TOKEN'` with your actual Discord bot token in the script.
- **Backup File**: The bot stores backup data in `server_backups.json`.

## Example

Here’s a brief example of how to use the bot:

1. **Creating a Backup**:
   ```
   /backup privacy: public image1: https://example.com/image1.png
   ```

2. **Listing Backups**:
   ```
   /list_backups
   ```

3. **Restoring a Backup**:
   ```
   /restore code: ABC123
   ```

4. **Deleting a Backup**:
   ```
   /delete_backup
   ```

## Notes

- Ensure that the bot has the necessary permissions to manage the server and create templates.
- Backup information is stored in a JSON file and can be edited or cleared manually if needed.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
