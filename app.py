#/bin/env python3

import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import cohere

# Load environment variables
load_dotenv()

# Initialize Cohere client
co = cohere.ClientV2(os.environ["COHERE_API_KEY"])

# Initialize Slack app
app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)

# Handle mentions of your bot
@app.event("app_mention")
def handle_mention(event, say):
    user_text = event["text"]
    # Remove the bot mention from the text
    user_text = user_text.split(">", 1)[1].strip() if ">" in user_text else user_text
    
    # Generate response using Cohere
    response = co.chat(
        message=user_text,
        model="command-a-03-2025"
    )
    
    # Reply in the channel
    say(response.text)

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))

