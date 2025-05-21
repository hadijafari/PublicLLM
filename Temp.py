
!pip install requests apscheduler boto3 firecrawl weasyprint markdown pdfkit pyppeteer playwright xhtml2pdf reportlab lxml firecrawl-py pydub ffmpeg-python


# imports

import os
import requests
from bs4 import BeautifulSoup
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai
import anthropic
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import datetime
from urllib.parse import urlparse
import time
import threading
import boto3
import json
from fpdf import FPDF
import uuid
from IPython.display import Markdown, display, HTML as DisplayHTML
import re
import markdown
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from xhtml2pdf import pisa
from firecrawl import FirecrawlApp, JsonConfig
from flask import Flask, Response, request
import pdfkit
from weasyprint import HTML, CSS
import logging
from botocore.exceptions import ClientError
import textwrap
from pprint import pprint
from pydantic import BaseModel, Field
import asyncio
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer
from pydub import AudioSegment
from pydub.utils import which
import ffmpeg







# Append ffmpeg bin path to PATH
ffmpeg_path = r"C:\ffmpeg"
os.environ["PATH"] += os.pathsep + ffmpeg_path








# Load environment variables from .env file
load_dotenv(override=True)

# Fetch API keys
openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')
firecrawl_api_key = os.getenv('FIRECRAWL_API_KEY_2')


# Fetch AWS S3 credentials
aws_access_key_id = os.getenv('AMAZON_S3_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AMAZON_S3_ACCESS_KEY')
apiTemplate_api_key = os.getenv('API_TEMPLATE_API_KEY')

# Print summaries
print("\n🔐 API Key Check:")

if openai_api_key:
    print(f"✅ OpenAI API Key loaded (starts with: {openai_api_key[:8]})")
else:
    print("❌ OpenAI API Key not set")

if anthropic_api_key:
    print(f"✅ Anthropic API Key loaded (starts with: {anthropic_api_key[:7]})")
else:
    print("❌ Anthropic API Key not set")

if google_api_key:
    print(f"✅ Google API Key loaded (starts with: {google_api_key[:8]})")
else:
    print("❌ Google API Key not set")

if firecrawl_api_key:
    print(f"✅ Firecrawl API Key loaded (starts with: {firecrawl_api_key[:8]})")
else:
    print("❌ Firecrawl API Key not set")

print("\n🗂️ AWS Credential Check:")

if aws_access_key_id:
    print(f"✅ AWS Access Key ID loaded (starts with: {aws_access_key_id[:8]})")
else:
    print("❌ AWS Access Key ID not set")

if aws_secret_access_key:
    print(f"✅ AWS Secret Access Key loaded (starts with: {aws_secret_access_key[:8]})")
else:
    print("❌ AWS Secret Access Key not set")

if apiTemplate_api_key:
    print(f"✅ API Template Access Key loaded (starts with: {apiTemplate_api_key[:8]})")
else:
    print("❌ API Template Secret Access Key not set")





openai = OpenAI()        # Create an instance of the OpenAI client.






######################################################################################################################################################################
#                           How to generate a simple audio file from a text string
######################################################################################################################################################################


# Set your API key
openai.api_key = openai_api_key

# Your input text
text = "Hello! This is an audio message generated using OpenAI's text-to-speech."

# Call the TTS API
response = openai.audio.speech.create(
    model="gpt-4o-mini-tts",  # or "tts-1-hd" for high-definition
    voice="nova",   # Options: "alloy", "echo", "fable", "onyx", "nova", "shimmer", "ash", "ballad", "coral", "sage"
    input=text
)

# Save the audio to a file
with open("output_audio.mp3", "wb") as f:
    f.write(response.content)

print("Audio file saved as output_audio.mp3")











######################################################################################################################################################################
#                           How to do batch generation (creating multiple audio files at once, usually from a list of different text inputs.)
######################################################################################################################################################################



openai.api_key = openai_api_key

texts = [
    "Welcome to our app!",
    "Don't forget to check your notifications.",
    "Thank you for using our service."
]

for i, text in enumerate(texts):
    response = openai.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="nova",
        input=text
    )

    filename = f"message_{i + 1}.mp3"
    with open(filename, "wb") as f:
        f.write(response.content)

    print(f"Saved {filename}")










######################################################################################################################################################################
#                           Streaming Real time Audio
#                           WE DO NOT NEED IT FOR THE AI NEWS AGENT
######################################################################################################################################################################




openai = AsyncOpenAI()

async def main() -> None:
    async with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input="Today is a wonderful day to build something people love!",
        instructions="Speak in a cheerful and positive tone.",
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)

if __name__ == "__main__":
    asyncio.run(main())







######################################################################################################################################################################
#                                     How to do batch generation and add music background to the generated audio
######################################################################################################################################################################


ffmpeg_dir = os.getenv("FFMPEG_DIR", r"C:\ffmpeg")

AudioSegment.converter = os.path.join(ffmpeg_dir, "ffmpeg.exe")
AudioSegment.ffprobe = os.path.join(ffmpeg_dir, "ffprobe.exe")

print("✔️ ffmpeg path:", AudioSegment.converter)
print("✔️ ffprobe path:", AudioSegment.ffprobe)



openai.api_key = openai_api_key


# Your background music file
background_music = AudioSegment.from_mp3("background_music.mp3")

texts = {
    "codex_launch": """Today we’re launching a research preview of Codex: a cloud-based software engineering agent that can work on many tasks in parallel. Codex can perform tasks for you such as writing features, answering questions about your codebase, fixing bugs, and proposing pull requests for review; each task runs in its own cloud sandbox environment, preloaded with your repository.

Codex is powered by codex-1, a version of OpenAI o3 optimized for software engineering. It was trained using reinforcement learning on real-world coding tasks in a variety of environments to generate code that closely mirrors human style and PR preferences, adheres precisely to instructions, and can iteratively run tests until it receives a passing result.""",

    "openai_o3_release": """Today, we’re releasing OpenAI o3 and o4-mini, the latest in our o-series of models trained to think for longer before responding. These are the smartest models we’ve released to date, representing a step change in ChatGPT's capabilities for everyone from curious users to advanced researchers. For the first time, our reasoning models can agentically use and combine every tool within ChatGPT—this includes searching the web, analyzing uploaded files and other data with Python, reasoning deeply about visual inputs, and even generating images.

Critically, these models are trained to reason about when and how to use tools to produce detailed and thoughtful answers in the right output formats, typically in under a minute, to solve more complex problems. This allows them to tackle multi-faceted questions more effectively, a step toward a more agentic ChatGPT that can independently execute tasks on your behalf. The combined power of state-of-the-art reasoning with full tool access translates into significantly stronger performance across academic benchmarks and real-world tasks, setting a new standard in both intelligence and usefulness.""",

    "gpt4o_images": """From the first cave paintings to modern infographics, humans have used visual imagery to communicate, persuade, and analyze—not just to decorate. Today's generative models can conjure surreal, breathtaking scenes, but struggle with the workhorse imagery people use to share and create information. From logos to diagrams, images can convey precise meaning when augmented with symbols that refer to shared language and experience.

GPT‑4o image generation excels at accurately rendering text, precisely following prompts, and leveraging 4o’s inherent knowledge base and chat context—including transforming uploaded images or using them as visual inspiration. These capabilities make it easier to create exactly the image you envision, helping you communicate more effectively through visuals and advancing image generation into a practical tool with precision and power."""
}


 
# Loop: generate individual audio files
for filename, text in texts.items():
    print(f"Generating voice for: {filename}")
    response = openai.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="nova",
        input=text
    )

    voice_path = f"{filename}_voice.mp3"
    with open(voice_path, "wb") as f:
        f.write(response.content)

    voice_audio = AudioSegment.from_mp3(voice_path)

    bg_music = background_music
    if len(background_music) < len(voice_audio):
        loop_count = int(len(voice_audio) / len(background_music)) + 1
        bg_music = background_music * loop_count

    bg_music = bg_music[:len(voice_audio)] - 20  # REDUCE THE BACKGROUND MUSIC VOLUME
    combined = bg_music.overlay(voice_audio)

    combined = combined.fade_in(1000).fade_out(1000)  # Apply fade-in/out to the combined voice+music

    final_output_path = f"{filename}_final.mp3"
    combined.export(final_output_path, format="mp3")
    print(f"✅ Saved: {final_output_path}")

    os.remove(voice_path)  # Clean temp file

# ✅ Merge after all segments are created
print("\n🔗 Merging all segments into one final audio file...")

segments = [
    AudioSegment.from_mp3("codex_launch_final.mp3"),
    AudioSegment.from_mp3("openai_o3_release_final.mp3"),
    AudioSegment.from_mp3("gpt4o_images_final.mp3")
]

pause = AudioSegment.silent(duration=1000)  # 1 second pause between clips

final_audio = segments[0]
for segment in segments[1:]:
    final_audio += pause + segment

final_audio.export("news_digest_complete.mp3", format="mp3")
print("✅ Final news digest saved as: news_digest_complete.mp3")

    






