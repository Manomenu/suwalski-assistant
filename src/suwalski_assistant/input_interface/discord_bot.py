import datetime
import logging
from uuid import uuid4
import discord
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types
from suwalski_assistant.settings import settings

class SuwalskiBot(discord.Client):
    """
    Custom Discord Client for Suwalski Assistant.
    Encapsulates the ADK runner and agent logic.
    """
    def __init__(self, runner: Runner, agent_name: str, target_channel_id: str=None, intents=None):
        super().__init__(intents=intents)
        self.runner = runner
        self.agent_name = agent_name
        self.target_channel_id = target_channel_id

    async def on_ready(self):
        logging.info(f'We have logged in as {self.user}')
        if self.target_channel_id:
            logging.info(f'Listening on channel ID: {self.target_channel_id}')
        else:
            logging.info('Listening on all accessible channels.')

    async def on_message(self, message):
        # Don't reply to ourselves
        if message.author == self.user:
            return

        # Filter by channel if configured
        if self.target_channel_id and str(message.channel.id) != str(self.target_channel_id):
            return

        user_id = str(message.author.id)
        current_date = datetime.date.today().strftime("%d_%m_%Y")
        session_id = f"{user_id}_{uuid4()}"
        
        # Ensure session exists
        session_service = self.runner.session_service
        existing_session = await session_service.get_session(app_name=self.runner.app_name, user_id=user_id, session_id=session_id)
        if not existing_session:
            await session_service.create_session(app_name=self.runner.app_name, user_id=user_id, session_id=session_id)

        # Prepare input
        parts = []
        if message.content:
            parts.append(types.Part(text=message.content))
            
        for attachment in message.attachments:
            if attachment.content_type and attachment.content_type.startswith('image/'):
                logging.info(f"Processing image attachment: {attachment.filename}")
                try:
                    image_data = await attachment.read()
                    parts.append(
                        types.Part(
                            inline_data=types.Blob(
                                data=image_data,
                                mime_type=attachment.content_type
                            )
                        )
                    )
                except Exception as e:
                    logging.error(f"Failed to read attachment {attachment.filename}: {e}")

        if not parts:
            logging.warning("Message contained no text or supported images.")
            return

        user_msg = types.Content(role='user', parts=parts)
        logging.info(f"Received message from {message.author}: {message.content} (Parts: {len(parts)})")

        try:
            # Run Agent
            response_text = ""
            async for event in self.runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=user_msg
            ):
                # Capture the agent's textual response
                if event.author != user_id and event.content:
                    for part in event.content.parts:
                        if part.text:
                            response_text = part.text

            # Send response back to Discord
            if response_text:
                if len(response_text) > 2000:
                    for i in range(0, len(response_text), 2000):
                        await message.channel.send(response_text[i:i+2000])
                else:
                    await message.channel.send(response_text)
                    
        except Exception as e:
            logging.error(f"Error processing message: {e}")
            await message.channel.send("I encountered an error processing your request.")

def run_discord_bot(agent):
    """
    Initializes the runner with the provided agent and starts the Discord bot.
    """
    token = settings.discord_token

    target_channel_id = settings.discord_channel_id

    # Initialize ADK Runner with the passed agent
    session_service = InMemorySessionService()
    bot_runner = Runner(
        agent=agent,
        session_service=session_service,
        app_name="SuwalskiDiscordBot"
    )
    
    # Initialize Discord Client
    intents = discord.Intents.default()
    intents.message_content = True
    
    logging.info(f"Starting Discord bot with agent: {agent.name}")
    
    client = SuwalskiBot(
        runner=bot_runner, 
        agent_name=agent.name, 
        target_channel_id=target_channel_id,
        intents=intents
    )
    client.run(token)
