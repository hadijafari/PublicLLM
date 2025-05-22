####################################################################################################################################################################################################
#                                                                     pip Installs
####################################################################################################################################################################################################

# !pip install requests apscheduler boto3 firecrawl weasyprint markdown pdfkit pyppeteer playwright xhtml2pdf reportlab lxml firecrawl-py pydub


####################################################################################################################################################################################################
#                                                                     Imports
####################################################################################################################################################################################################
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
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import datetime
from urllib.parse import urlparse
import time
from pytz import timezone
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
from firecrawl import FirecrawlApp
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
# from openai.helpers import LocalAudioPlayer
from pydub import AudioSegment








####################################################################################################################################################################################################
#                                                                     Load environment variables from .env file
####################################################################################################################################################################################################



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





####################################################################################################################################################################################################
#                                                                     Creating Instances
####################################################################################################################################################################################################




openai = OpenAI()        # Create an instance of the OpenAI client.

# Initialize S3 client
amazon_s3 = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)








####################################################################################################################################################################################################
#                                                                     Functions
####################################################################################################################################################################################################









# ==================== FUNCTION INDEX ====================

# --- UUID/User ID Generation ---
# - generate_unique_user_id()              # Generates a globally unique user ID
# - generate_short_user_id()               # Generates a short unique user ID

# --- Web Scraping ---
# - scrape_with_firecrawl(target_url, max_retries=5)   # Scrapes content using Firecrawl API
# - get_screenshot_from_firecrawl(url)                 # Captures a screenshot via Firecrawl

# --- Scheduler / Automation ---
# - start_firecrawl_scheduler_interrupt(hour, minute)      # Starts a daily scraping scheduler
# - def start_scheduler()                                  # Used to run the test every 4 hours

# --- S3 Storage Operations ---
# - download_json_from_s3(filename, s3_key, bucket_name, s3_client)       # Downloads JSON from S3
# - upload_json_to_s3(filename, s3_key, bucket_name, json_data, s3_client)# Uploads JSON to S3
# - list_s3_buckets(s3_client)                                            # Lists all S3 buckets
# - list_files_in_bucket(bucket_name, s3_client, prefix="")               # Lists files in a bucket
# - create_s3_bucket(bucket_name, region, s3_client)                      # Creates a new S3 bucket
# - create_s3_folder(bucket_name, folder_path, s3_client)                 # Creates a folder in S3
# - list_json_files_in_folder(bucket_name, folder_prefix, s3_client)      # Lists .json files in a folder
# - append_to_json_list_in_s3(bucket_name, s3_key, new_element, s3_client)# Appends a new entry to JSON list in S3
# - load_user_profile_from_s3(user_id, bucket_name, s3_client)            # Loads user profile JSON from S3

# --- User Data Initialization ---
# - Initial_user_Data(user_data, s3_client)                               # Uploads profile and scrapes user sources

# --- Link Processing & Summarization ---
# - summarize_markdown_with_gpt(markdown_content)                         # Summarizes markdown using GPT
# - process_and_summarize_new_links(new_links_summary)                    # Scrapes & summarizes new links
# - User_Daily_scraping_and_summarization(user_id, bucket_name, s3_client)# Main daily workflow for users

# --- PDF Generation ---
# - Generate_PDF(template_id, data)                                       # Generates a PDF using APITemplate.io

# --- Email Delivery ---
# - send_summary_email(summaries, sender_email, sender_password, recipient_email, pdf_url=None, smtp_server, smtp_port, subject_prefix)
#                                                                       # Sends email with summaries (or no-news update)


# def run_all_users()

# ========================================================













# ==================== UUID/User ID Generation ====================



def generate_unique_user_id() -> str:
    """
    Generate a globally unique user ID with a 'user_' prefix using UUID4.

    Returns:
        str: A prefixed UUID string like 'user_123e4567-e89b-12d3-a456-426614174000'
    """
    return f"user_{uuid.uuid4()}"





def generate_short_user_id() -> str:
    """
    Generate a short unique user ID like 'user_8f14e45f'.

    Returns:
        str: A shortened UUID string with 'user_' prefix
    """
    short_id = str(uuid.uuid4())[:8]
    return f"user_{short_id}"







# ==================== Web Scraping ====================



def scrape_with_firecrawl(target_url: str, max_retries: int = 5) -> dict:
    """
    Scrapes the given URL using Firecrawl API and returns markdown, links, and original URL.
    Automatically retries on 429 Too Many Requests errors.

    Parameters:
        target_url (str): The webpage URL to scrape.
        max_retries (int): Maximum number of retries on 429 error.

    Returns:
        dict: {
            'url': str,        # Original URL
            'markdown': str,   # Markdown version of the content
            'links': list      # List of extracted links
        }
    """
    if not firecrawl_api_key:
        raise ValueError("Firecrawl API key is missing. Please set FIRECRAWL_API_KEY in your environment.")

    api_url = "https://api.firecrawl.dev/v1/scrape"

    payload = {
        "url": target_url,
        "formats": ["markdown", "links"],
        "onlyMainContent": True,
        "removeBase64Images": True,
        "blockAds": True,
        "proxy": "basic"
    }

    headers = {
        "Authorization": f"Bearer {firecrawl_api_key}",
        "Content-Type": "application/json"
    }

    retries = 0
    while retries <= max_retries:
        try:
            response = requests.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json().get("data", {})
            return {
                "url": target_url,
                "markdown": data.get("markdown", "No markdown found."),
                "links": data.get("links", [])
            }
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                retries += 1
                time.sleep(5)
                continue
            return {"error": f"HTTP Error: {e}", "url": target_url}
        except Exception as e:
            return {"error": f"Error: {e}", "url": target_url}

    return {"error": f"Too many retries after hitting 429 Too Many Requests.", "url": target_url}
            




def get_screenshot_from_firecrawl(url: str) -> str:
    """
    Uses Firecrawl to take a screenshot of the given URL and returns the screenshot URL.

    Parameters:
        url (str): The target webpage URL.

    Returns:
        str: URL to the screenshot image, or None if not found or failed.
    """
    try:
        app = FirecrawlApp(api_key=firecrawl_api_key)

        scrape_result = app.scrape_url(
            url=url,
            formats=['html'],  # Only need HTML if you're not parsing content
            actions=[
                {"type": "wait", "milliseconds": 3000},
                {"type": "screenshot"}
            ]
        )

        if scrape_result.success:
            screenshots = scrape_result.actions.screenshots
            if screenshots:
                return screenshots[0]  # Return the first screenshot URL
            else:
                print(f"No screenshot found for {url}")
        else:
            print(f"❌ Screenshot scrape failed for {url}")

    except Exception as e:
        print(f"❌ Exception while taking screenshot: {e}")

    return None





# ==================== Scheduler / Automation ====================



def start_scheduler():
    scheduler = BackgroundScheduler(timezone=melbourne_tz)

    times = [
        (13, 00),
        (16, 30),
        (20, 30),
        (0, 30),
        (4, 40),
        (8, 30),
    ]

    for hour, minute in times:
        trigger = CronTrigger(hour=hour, minute=minute, timezone=melbourne_tz)
        scheduler.add_job(run_all_users, trigger)
        logging.info(f"⏰ Job scheduled for {hour:02d}:{minute:02d} Melbourne time.")

    scheduler.start()
    logging.info("🟢 Background scheduler started (non-blocking).")


def start_firecrawl_scheduler_interrupt(hour: int, minute: int):
    """
    Starts a background scheduler to run the Firecrawl scrape job daily at a specific time.

    Parameters:
        hour (int): Hour in 24-hour format (e.g., 13 for 1 PM)
        minute (int): Minute (e.g., 30 for half past the hour)
    """

    def job():
        # You can change this URL to any page you want to scrape
        result = scrape_with_firecrawl("https://openai.com/news/")
        print(f"[{datetime.now()}] Scraped successfully.")
        filename = f"daily_scrape_{datetime.now().date()}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(result["markdown"])
        print(f"Saved to {filename}")

    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'cron', hour=hour, minute=minute)
    scheduler.start()

    print(f"✅ Scheduler started: scraping daily at {hour:02d}:{minute:02d}.")
    return scheduler  # Optional, for future shutdown or inspection


# ==================== S3 Storage Operations ====================

def download_json_from_s3(filename: str, s3_key: str, bucket_name: str, s3_client) -> dict:
    """
    Downloads a JSON file from S3 and returns it as a Python dictionary.

    Parameters:
        filename (str): Friendly label (for logging/debugging only)
        s3_key (str): The path to the object in the bucket (e.g., "folder/goooz.json")
        bucket_name (str): The name of the S3 bucket
        s3_client (boto3.client): Pre-initialized boto3 S3 client

    Returns:
        dict: Parsed JSON content
    """
    # print(f"🔽 Downloading '{filename}' from s3://{bucket_name}/{s3_key} ...")
    response = s3_client.get_object(Bucket=bucket_name, Key=s3_key)
    content = response['Body'].read().decode('utf-8')
    return json.loads(content)





def upload_json_to_s3(filename: str, s3_key: str, bucket_name: str, json_data: dict, s3_client) -> bool:
    """
    Uploads a Python dictionary as a JSON file to S3.

    Parameters:
        filename (str): Friendly label (for logging/debugging only)
        s3_key (str): The path to save the object in the bucket
        bucket_name (str): The name of the S3 bucket
        json_data (dict): The JSON content to upload
        s3_client (boto3.client): Pre-initialized boto3 S3 client

    Returns:
        bool: True if upload was successful, False otherwise
    """
    # print(f"⬆️ Uploading '{filename}' to s3://{bucket_name}/{s3_key} ...")
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=json.dumps(json_data, indent=2),
            ContentType='application/json'
        )
        print("✅ Upload successful.")
        return True
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return False





def list_s3_buckets(s3_client) -> list:
    """
    Lists all bucket names in the connected AWS account.

    Parameters:
        s3_client (boto3.client): Pre-initialized boto3 S3 client

    Returns:
        list: A list of bucket names
    """
    response = s3_client.list_buckets()
    bucket_names = [bucket['Name'] for bucket in response.get('Buckets', [])]
    print("📦 S3 Buckets found:", bucket_names)
    return bucket_names




def list_files_in_bucket(bucket_name: str, s3_client, prefix: str = "") -> list:
    """
    Lists all object keys (files) in a specific S3 bucket (optionally under a prefix/folder).

    Parameters:
        bucket_name (str): Name of the bucket
        s3_client (boto3.client): Pre-initialized boto3 S3 client
        prefix (str): Optional folder path to narrow down results

    Returns:
        list: List of file keys in the bucket
    """
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    contents = response.get("Contents", [])
    file_keys = [obj["Key"] for obj in contents]
    print(f"📂 Files in s3://{bucket_name}/{prefix}:", file_keys)
    return file_keys




def create_s3_bucket(bucket_name: str, region: str, s3_client) -> bool:
    """
    Creates a new S3 bucket in the specified AWS region.

    Parameters:
        bucket_name (str): Globally unique name for the bucket
        region (str): AWS region code (e.g., 'us-east-1', 'us-west-2')
        s3_client (boto3.client): Pre-initialized boto3 S3 client

    Returns:
        bool: True if bucket was created successfully, False if it failed
    """
    try:
        if region == "us-east-1":
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        print(f"✅ Bucket '{bucket_name}' created in region '{region}'.")
        return True
    except s3_client.exceptions.BucketAlreadyExists:
        print(f"❌ Bucket name '{bucket_name}' is already taken globally.")
    except s3_client.exceptions.BucketAlreadyOwnedByYou:
        print(f"ℹ️ Bucket '{bucket_name}' already exists and is owned by you.")
        return True
    except Exception as e:
        print(f"❌ Failed to create bucket: {e}")
    return False




def create_s3_folder(bucket_name: str, folder_path: str, s3_client) -> bool:
    """
    Creates a 'folder' in an S3 bucket by uploading a zero-byte object ending with '/'.

    Parameters:
        bucket_name (str): Name of the S3 bucket
        folder_path (str): Folder path (e.g., 'users/user_123/')
        s3_client (boto3.client): Pre-initialized boto3 S3 client

    Returns:
        bool: True if folder was created successfully, False otherwise
    """
    if not folder_path.endswith('/'):
        folder_path += '/'

    try:
        s3_client.put_object(Bucket=bucket_name, Key=folder_path)
        print(f"✅ Folder '{folder_path}' created in bucket '{bucket_name}'.")
        return True
    except Exception as e:
        print(f"❌ Failed to create folder '{folder_path}' in bucket '{bucket_name}': {e}")
        return False





def list_json_files_in_folder(bucket_name: str, folder_prefix: str, s3_client) -> list:
    """
    Lists all .json files in a specific folder (prefix) in an S3 bucket.

    Parameters:
        bucket_name (str): The S3 bucket name.
        folder_prefix (str): The folder path (e.g., 'user_8f14e45f/').
        s3_client (boto3.client): Pre-initialized Boto3 S3 client.

    Returns:
        list: A list of S3 keys (file paths) that end with .json
    """
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix)
        files = response.get("Contents", [])

        json_files = [
            obj["Key"] for obj in files
            if obj["Key"].endswith(".json")
        ]

        return json_files

    except ClientError as e:
        logging.error(f"❌ Failed to list files in {folder_prefix}: {e}")
        return []





def append_to_json_list_in_s3(bucket_name: str, s3_key: str, new_element: dict, s3_client) -> bool:
    """
    Opens a JSON file in S3 (expected to be a list of dicts), checks if an email exists,
    appends a new element if it's not a duplicate, and uploads the updated file back to S3.

    Parameters:
        bucket_name (str): S3 bucket name
        s3_key (str): Key (path) to the JSON file in S3
        new_element (dict): The new dictionary to append (must include 'email' key)
        s3_client (boto3.client): A pre-configured boto3 S3 client

    Returns:
        bool: True if operation succeeded or user already exists, False on error
    """
    try:
        # Step 1: Download and parse the existing JSON file
        response = s3_client.get_object(Bucket=bucket_name, Key=s3_key)
        content = response['Body'].read().decode('utf-8').strip()

        if not content:
            data = []
        else:
            data = json.loads(content)

        if not isinstance(data, list):
            logging.error(f"❌ JSON at s3://{bucket_name}/{s3_key} is not a list.")
            return False

        # Step 2: Check if user email already exists
        existing_emails = {user.get("email") for user in data if isinstance(user, dict)}
        new_email = new_element.get("email")

        if not new_email:
            logging.error("❌ 'email' key is missing from the new element.")
            return False

        if new_email in existing_emails:
            logging.info(f"ℹ️ User with email '{new_email}' already exists. Skipping append.")
            return True  # Not a failure — just already present

        # Step 3: Append the new element
        data.append(new_element)

        # Step 4: Upload the updated list back to S3
        updated_body = json.dumps(data, indent=2)
        s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=updated_body,
            ContentType='application/json'
        )

        logging.info(f"✅ Successfully appended new user to {s3_key}.")
        return True

    except ClientError as e:
        logging.error(f"❌ AWS error: {e}")
    except json.JSONDecodeError:
        logging.error(f"❌ Failed to decode JSON at s3://{bucket_name}/{s3_key}.")
    except Exception as e:
        logging.error(f"❌ Unexpected error: {e}")

    return False





def load_user_profile_from_s3(user_id: str, bucket_name: str, s3_client) -> dict:
    """
    Loads the user profile JSON from S3 and returns it as a dictionary.

    Parameters:
        user_id (str): The user ID (e.g., "user_8f14e45f")
        bucket_name (str): The S3 bucket name
        s3_client: The Boto3 S3 client

    Returns:
        dict: The user profile data
    """
    key = f"{user_id}/profile.json"

    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        content = response["Body"].read().decode("utf-8")
        profile_data = json.loads(content)
        return profile_data

    except s3_client.exceptions.NoSuchKey:
        print(f"❌ Profile not found at: {key}")
        return {}
    except Exception as e:
        print(f"❌ Error loading profile from S3: {e}")
        return {}






# ==================== User Data Initialization ====================

def Initial_user_Data(user_data: dict, s3_client):
    """
    Processes user data by:
    - Creating a folder in S3
    - Uploading user profile as JSON
    - Scraping each URL in sources and saving the output to S3 as JSON
    """
    bucket_name = "ai-news-agent"
    user_id = user_data.get("user_id")
    folder_name = f"{user_id}/"

    logging.info(f"🚀 Starting processing for user: {user_id}")

    # Step 1: Create user folder
    if not create_s3_folder(bucket_name, folder_name, s3_client):
        logging.error(f"❌ Failed to create folder for {user_id}. Aborting.")
        return

    # Step 2: Upload profile.json
    profile_key = f"{folder_name}profile.json"
    if not upload_json_to_s3("User Profile", profile_key, bucket_name, user_data, s3_client):
        logging.error(f"❌ Failed to upload profile.json for {user_id}. Aborting.")
        return
    logging.info(f"✅ Uploaded user profile for {user_id}.")

    # Step 3: Scrape each URL in the sources list
    sources = user_data.get("sources", [])
    for url in sources:
        try:
            logging.info(f"🌐 Scraping URL: {url}")
            scrape_result = scrape_with_firecrawl(url)

            # Error Handling: If scraping failed, skip
            if "error" in scrape_result:
                logging.warning(f"⚠️ Scraping failed for {url}: {scrape_result['error']}")
                continue

            # Build filename like techcrunch_com.json
            domain = urlparse(url).netloc.replace('.', '_')
            file_name = f"{domain}.json"
            s3_key = f"{folder_name}{file_name}"

            # Upload scraped result
            if upload_json_to_s3(file_name, s3_key, bucket_name, scrape_result, s3_client):
                logging.info(f"✅ Uploaded scraped data: {file_name}")
            else:
                logging.warning(f"⚠️ Failed to upload scraped data for {url}.")

        except Exception as e:
            logging.error(f"❌ Exception occurred while processing {url}: {e}")






# ==================== Link Processing & Summarization ====================




def summarize_markdown_with_gpt(markdown_content: str) -> str:
    """
    Summarizes given markdown content using OpenAI GPT.

    Parameters:
        markdown_content (str): Markdown-formatted content to summarize.

    Returns:
        str: A concise, professional summary under 500 words.
    """
    system_prompt = """## Purpose
The primary task of the AI is to create concise summaries of articles, ensuring the summaries are under 500 words and maintain the integrity of the original content.

## Extraction Guidelines
- Identify and prioritize main arguments, key points, and significant findings in the article.
- Extract important quotes that represent central ideas or unique perspectives.
- Preserve research findings and statistical data.
- Maintain proper attribution for all quotes and claims (e.g., specify who said what).

## Output Format Requirements
- The summary must be in string format.
- Ensure a clear structure with a logical flow.
- Limit the summary to under 500 words.
- Include proper formatting for quotes, emphasis, and section breaks if needed.

## Content Style Guidelines
- Use clear, concise language.
- Maintain an objective tone.
- Prohibit meta-references (e.g., no mentions of being an AI or that this is a summary).
- Avoid unnecessary editorializing or commentary on the content.

## Quality Checks
- Verify that all key points from the original article are included.
- Ensure proper attribution is maintained for all extracted quotes and data.
- Confirm the summary stays under the 500-word limit.
- Validate that the summary accurately represents the original article's intent and message.

## Tone and Approach
The system prompt should establish a professional, analytical tone focused on information accuracy and clarity. 
It should emphasize the importance of distilling complex information while maintaining fidelity to the source material."""

    user_prompt = f"""Please analyze the following article content and create a concise, well-structured summary that:

- Is under 500 words
- Extracts and prioritizes the main arguments, key points, and significant findings
- Identifies and preserves important quotes with proper attribution
- Presents information in markdown format
- Avoids any meta-references (no mentions of being an AI or that this is a summary)
- Presents information directly and clearly
- Do not give any additional words of any kind. Just give the summary as if you are a news reporter

<article_content>{markdown_content}</article_content>"""

    prompts = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    try:
        completion = openai.chat.completions.create(
            model='o4-mini-2025-04-16',
            messages=prompts
        )
        summary = completion.choices[0].message.content.strip()
        return summary

    except Exception as e:
        return f"Error summarizing content: {e}"





def process_and_summarize_new_links(new_links_summary: dict) -> dict:
    """
    Scrapes and summarizes all new links in the new_links_summary dictionary.

    Parameters:
        new_links_summary (dict): Dictionary structured as:
            {
                "source_url": {
                    "new_links": [
                        {"url": "new_link_1", "summary": ""},
                        ...
                    ]
                },
                ...
            }

    Returns:
        dict: The same dictionary with summaries filled in.
    """
    for source_url, data in new_links_summary.items():
        for link_entry in data["new_links"]:
            link_url = link_entry["url"]
            print(f"Processing: {link_url}")

            scraped = scrape_with_firecrawl(link_url)

            if "error" in scraped:
                print(f"Failed to scrape {link_url}: {scraped['error']}")
                link_entry["summary"] = f"Error: {scraped['error']}"
                continue

            markdown = scraped.get("markdown", "")
            if not markdown.strip():
                link_entry["summary"] = "Error: No markdown content found."
                continue

            summary = summarize_markdown_with_gpt(markdown)
            link_entry["summary"] = summary
            print(f"Summary complete for {link_url}")

    return new_links_summary






def User_Daily_scraping_and_summarization(user_id: str, bucket_name: str, s3_client):
    """
    Main workflow for scraping and summarizing new content for a given user.

    Parameters:
        user_id (str): The ID of the user (e.g., 'user_8f14e45f')
        bucket_name (str): Name of the S3 bucket
        s3_client: Boto3 S3 client instance

    Returns:
        dict: A dictionary of all new links and their summaries
    """
    User_Profile = load_user_profile_from_s3(user_id, bucket_name,s3_client)
    print(json.dumps(User_Profile, indent=4))
    
    prefix = f"{user_id}/"
    json_files_List = list_json_files_in_folder(bucket_name, prefix, s3_client)

    print("The available JSON files are here:")
    print(json.dumps(json_files_List, indent=4))
    print("\n\n\n\n\n\n")

    new_links_summary = {}

    for s3_key in json_files_List:
        filename = s3_key.split("/")[-1]

        if filename == "profile.json":
            continue

        full_key = f"{prefix}{filename}"
        Yesterday_Data = download_json_from_s3(full_key, full_key, bucket_name, s3_client)

        url = Yesterday_Data['url']
        Today_Data = scrape_with_firecrawl(url)

        if "error" in Today_Data:
            print(f"Skipping {url} due to error: {Today_Data['error']}")
            continue

        upload_json_to_s3(full_key, full_key, bucket_name, Today_Data, s3_client)

        Yesterday_Links = Yesterday_Data.get("links", [])
        today_Links = Today_Data.get("links", [])

        New_Links = list(set(today_Links) - set(Yesterday_Links))

        if New_Links:
            new_links_summary[url] = {"new_links": []}

            for link in New_Links:
                new_links_summary[url]["new_links"].append({
                    "url": link,
                    "summary": ""
                })

    print("Detected new links:")
    print(json.dumps(new_links_summary, indent=4))
    
    # Filter out external links that don’t match the source domain
    for source_url in list(new_links_summary.keys()):
        source_domain = urlparse(source_url).netloc.replace("www.", "").lower()
        filtered_links = []

        for link in new_links_summary[source_url]["new_links"]:
            link_domain = urlparse(link["url"]).netloc.replace("www.", "").lower()

            if link_domain == source_domain:
                filtered_links.append(link)

        if filtered_links:
            new_links_summary[source_url]["new_links"] = filtered_links
        else:
            # Remove the source completely if no valid links remain
            del new_links_summary[source_url]

        
    updated_links_summary = process_and_summarize_new_links(new_links_summary)

    print("Final summaries:")
    print(json.dumps(updated_links_summary, indent=4))


    # Step: Flatten summaries
    all_summaries = []
    for source_url, data in updated_links_summary.items():
        for item in data["new_links"]:
            screenshot_url = get_screenshot_from_firecrawl(item["url"])
            
            all_summaries.append({
                "source": source_url,
                "url": item["url"],
                "summary": item["summary"],
                "screenshot": screenshot_url
            })
    
                
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print(json.dumps(all_summaries, indent=4))
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

    data_for_pdf = {
    "all_summaries": all_summaries
    }

    pdf_url = Generate_PDF(template_id, data_for_pdf)

    
        # Step: Send the email
    if not all_summaries:
        print("📭 No new summaries today. Sending no-news email...")
    else:
        print(f"📬 Preparing to send {len(all_summaries)} summaries...")
    
    send_summary_email(
        summaries=all_summaries,
        sender_email=Email_SyncLiving_Sender,
        sender_password=Email_SyncLiving_Sender_AppPassword,
        recipient_email=User_Profile["email"],
        pdf_url=pdf_url  # ✅ NEW ARG
    )




# ==================== PDF Generation ====================

def Generate_PDF(template_id: str, data: dict) -> str:
    """
    Generate a PDF using APITemplate.io with the given template ID and data.

    Args:
        template_id (str): The ID of the template you created in APITemplate.io
        data (dict): A JSON-like Python dictionary containing dynamic data for the template

    Returns:
        str: The download URL of the generated PDF if successful, or an error message
    """
    if not apiTemplate_api_key:
        raise ValueError("❌ APITEMPLATE_API_KEY is not set in your environment.")

    url = f"https://api.apitemplate.io/v1/create?template_id={template_id}"
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": apiTemplate_api_key
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        download_url = result.get("download_url")
        print("✅ PDF Generated!")
        print("📎 Download URL:", download_url)
        return download_url
    else:
        print("❌ Error:", response.status_code)
        print(response.text)
        return None




# ==================== Email Delivery ====================

def send_summary_email(
    summaries: list,
    sender_email: str,
    sender_password: str,
    recipient_email: str,
    pdf_url: str = None,
    smtp_server: str = "smtp.office365.com",  # ✅ Updated to Outlook
    smtp_port: int = 587,                     # ✅ Updated to Outlook
    subject_prefix: str = "🧠 Daily AI News Summary"
):
    """
    Sends an email with summaries of new articles. If no summaries are provided, sends a 'no news' message.

    Parameters:
        summaries (list): List of dicts with 'url', 'summary', and optionally 'source'.
        sender_email (str): The sender Outlook address.
        sender_password (str): App password for the sender email.
        recipient_email (str): The recipient email address.
        smtp_server (str): SMTP server address (default: Outlook).
        smtp_port (int): SMTP port (default: 587).
        subject_prefix (str): Prefix to use in the subject line.
    """

    if not summaries:
        print("📭 No news today. Sending empty update email...")

        msg = MIMEMultipart("alternative")
        msg["Subject"] = "📰 Daily Update – No News for Today"
        msg["From"] = sender_email
        msg["To"] = recipient_email

        no_news_html = """
        <html>
          <body style="font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
              <h2 style="color: #1a73e8;">📰 Daily AI News Digest</h2>
              <p style="font-size: 16px; color: #444;">There are no new articles to report today.</p>
            </div>
          </body>
        </html>
        """
        body = MIMEText(no_news_html, "html")
        msg.attach(body)

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, msg.as_string())
            print("✅ Email sent: No news for today.")
        except Exception as e:
            print(f"❌ Failed to send 'no news' email: {e}")
        return

    print(f"📬 Sending {len(summaries)} article summaries...")

    # Format article summaries into HTML
    article_html = ""
    for idx, item in enumerate(summaries, start=1):
        formatted_summary = item['summary'].replace('\n', '<br>')

        # Add screenshot image if available
        screenshot_html = ""
        if item.get("screenshot"):
            screenshot_html = f"""
                <div style="margin-top: 15px;">
                    <img src="{item['screenshot']}" alt="Screenshot" style="max-width: 100%; border-radius: 6px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                </div>
            """

        article_html += f"""
        <div style="margin-bottom: 30px;">
            <h3 style="color: #1a73e8;">{idx}. <a href="{item['url']}" style="text-decoration: none; color: #1a73e8;">{item['url']}</a></h3>
            <div style="font-size: 15px; color: #333; line-height: 1.6;">
                {formatted_summary}
                {screenshot_html}
            </div>
        </div>
        """

    full_email_html = f"""
    <html>
      <body style="font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 700px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
          <h2 style="color: #1a73e8;">{subject_prefix}</h2>
          <p style="font-size: 16px; color: #666;">Here are the latest updates from the web:</p>

          {f'''
          <div style="margin: 20px 0; padding: 15px; background-color: #f0f8ff; border-left: 4px solid #1a73e8;">
            📄 <strong>Your full digest PDF is available here:</strong>
            <br>
            <a href="{pdf_url}" style="color: #1a73e8; text-decoration: underline;">Download PDF Report</a>
          </div>
          ''' if pdf_url else ''}

          {article_html}
        </div>
      </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"{subject_prefix} – {len(summaries)} article{'s' if len(summaries) > 1 else ''}"
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg.attach(MIMEText(full_email_html, "html"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print("✅ Summary email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send summary email: {e}")



# ==================== run_all_users to be used in the scheduling function ====================

def run_all_users():
    logging.info("🔄 Running summarization for all users...")
    User_Daily_scraping_and_summarization("user_8f14e45f", bucket_name, amazon_s3)
    User_Daily_scraping_and_summarization("user_deada551", bucket_name, amazon_s3)
    User_Daily_scraping_and_summarization("user_b4fa9ce2", bucket_name, amazon_s3)
    logging.info("✅ Finished summarization for all users.")




# ==================== Logging Setup ====================

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Set up logging to display in JupyterLab output cells
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)





####################################################################################################################################################################################################
#                                                                     All Constants and Variable
####################################################################################################################################################################################################




AllUsers_s3_key = "All_Users.json"


bucket_name = "ai-news-agent"

OpenAI_s3_key = "OpenAI.json"
Anthropic_s3_key = "Anthropic.json"
Gemini_s3_key = "Gemini.json"
# GoogleNews_s3_key = "GoogleNews.json"

OpenAI_filename = "OpenAI.json"
Anthropic_filename = "Anthropic.json"
Gemini_filename = "Gemini.json"
# GoogleNews_filename = "GoogleNews.json"

Email_Sender="mazhabjaffari.hadi@gmail.com"                
Email_Sender_Password = "fmmj uqvh mnlw mmxr"              

Email_SyncLiving_Sender = "Hadi_Jeffry@syncliving.com.au"
Email_SyncLiving_Sender_AppPassword = "fxvmcpzzglswwpcr"             

Email_Recipient = "mazhabjaffari.hadi@gmail.com"           
Email_SMTP_Server= "smtp.gmail.com"
Email_SMTP_port= 587

# Set template ID for PDG Generation 
template_id = "4cc77b23f00e756c"

# Melbourne Timezone
melbourne_tz = timezone("Australia/Melbourne")



####################################################################################################################################################################################################
#                                                                     Main Program
####################################################################################################################################################################################################





#   IN THIS CELL, I DEFINED 3 USERS AND USED THEIR JSON TO INITIALIZE THEIR REGISTRATION PROCESS.


# THE SAMPLE JSON DATA FOR 3 USER TESTS



user1 = {
    "user_id": "user_8f14e45f",
    "email": "mazhabjaffari.hadi@gmail.com",
    "full_name": "Mohammadhadi Mazhabjafari",
    "plan": {
        "name": "A",
        "limit": 5
    },
    "sources": [
        "https://openai.com/news/",
        "https://www.anthropic.com/news",
        "https://blog.google/products/gemini/",
        "https://www.perplexity.ai/hub",
        "https://www.artificialintelligence-news.com/",
        "https://techcrunch.com/category/artificial-intelligence/"
    ],
    "preferences": {
        "topics": ["AI", "startups", "robotics"],
        "format": "PDF",
        "language": "en"
    },
    "delivery_settings": {
        "timezone": "America/New_York",
        "delivery_time": "08:00"
    },
    "email_opt_in": {
        "marketing": False,
        "product_updates": True
    },
    "created_at": "2025-05-09T10:00:00Z",
    "last_updated": "2025-05-09T10:00:00Z"
}


user2 = {
    "user_id": "user_b4fa9ce2",
    "email": "mhj11015@gmail.com",
    "full_name": "MHJ11015",
    "plan": {
        "name": "C",
        "limit": 15
    },
    "sources": [
        "https://www.news.com.au/",
        "https://www.abc.net.au/news",
        "https://www.9news.com.au/",
        "https://www.theage.com.au/"
    ],
    "preferences": {
        "topics": ["machine learning", "funding", "cloud"],
        "format": "PDF",
        "language": "en"
    },
    "delivery_settings": {
        "timezone": "Europe/London",
        "delivery_time": "07:30"
    },
    "email_opt_in": {
        "marketing": True,
        "product_updates": True
    },
    "created_at": "2025-04-21T14:12:00Z",
    "last_updated": "2025-05-10T11:02:00Z"
}


user3 = {
    "user_id": "user_deada551",
    "email": "hadi.jeffry313@gmail.com",
    "full_name": "Hadi Jeffry",
    "plan": {
        "name": "B",
        "limit": 10
    },
    "sources": [
        "https://www.theguardian.com/au",
        "https://www.morningstar.com.au/insights/top-stories"
    ],
    "preferences": {
        "topics": ["robotics", "automation"],
        "format": "HTML",
        "language": "en"
    },
    "delivery_settings": {
        "timezone": "Asia/Tokyo",
        "delivery_time": "09:15"
    },
    "email_opt_in": {
        "marketing": False,
        "product_updates": False
    },
    "created_at": "2025-03-15T06:00:00Z",
    "last_updated": "2025-05-08T08:30:00Z"
}


# The user initializations

# append_to_json_list_in_s3(bucket_name, AllUsers_s3_key, user1, amazon_s3)
# Initial_user_Data(user1, amazon_s3)

# append_to_json_list_in_s3(bucket_name, AllUsers_s3_key, user2, amazon_s3)
# Initial_user_Data(user2, amazon_s3)

# append_to_json_list_in_s3(bucket_name, AllUsers_s3_key, user3, amazon_s3)
# Initial_user_Data(user3, amazon_s3)









# ==================== MAIN FUNCTION ====================

if __name__ == "__main__":
    start_scheduler()
    
    # Keep the script alive so the scheduler can run
    try:
        while True:
            time.sleep(60)  # Sleep to prevent exit
    except (KeyboardInterrupt, SystemExit):
        print("🛑 Scheduler stopped.")










