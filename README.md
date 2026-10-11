## 🐳 How to Deploy with Docker

Since this tool features an interactive CLI configuration for secure token input, you need to run the container in **interactive mode**.

### 1. Build the Docker Image
Open your terminal in the project folder and build the isolated image:
```bash
docker build -t tg-web-monitor .
```

### 2. Run the Container (Interactive Mode)
Launch the container with `-it` flags to pass your keyboard input inside Docker:
```bash
docker run -it --name web-monitor-running tg-web-monitor
```

### 3. Setup Process
1. The container will start and ask you to enter your Telegram Bot API Token.
2. Paste the token from `@BotFather` and press **Enter**.
3. Go to Telegram, find your bot, and send the `/start` command. 
4. The system will automatically catch your ID and start monitoring `SITES` listed in the config.

*To detach from the container terminal without stopping it, use the standard Docker shortcut: `Ctrl + P`, then `Ctrl + Q`.*
