####################################################################################################################################################################################################
#                                                                     pip Installs
####################################################################################################################################################################################################

# !pip install requests apscheduler boto3 firecrawl weasyprint markdown pdfkit pyppeteer playwright xhtml2pdf reportlab lxml firecrawl-py pydub ffmpeg-python pytz


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
from pytz import timezone
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
from firecrawl import FirecrawlApp
from firecrawl import AsyncFirecrawlApp
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
import nest_asyncio
import random
from collections import defaultdict








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


nest_asyncio.apply()





####################################################################################################################################################################################################
#                                                                     Functions
####################################################################################################################################################################################################









# ==================== FUNCTION INDEX ====================


# --- UUID/User ID Generation ---
# - generate_unique_user_id()            # Generates a unique ID for user identification
# - generate_short_user_id()             # Generates a shortened unique user ID


# --- Web Scraping ---
# - scrape_with_firecrawl()              # Scrapes content and links from a URL using Firecrawl API
# - scrape_multiple_urls()               # Scrapes a list of URLs and returns their results


# --- Scheduler / Automation ---
# - start_firecrawl_scheduler_blocking() # Starts a blocking daily scrape job
# - start_firecrawl_scheduler_interrupt()# Starts a non-blocking (interruptible) daily scrape job


# --- S3 Storage Operations ---
# - download_json_from_s3()              # Downloads and parses a JSON file from S3
# - upload_json_to_s3()                  # Uploads a Python dictionary as a JSON file to S3
# - list_s3_buckets()                    # Lists all S3 buckets in the AWS account
# - list_files_in_bucket()               # Lists all files in a specified S3 bucket
# - create_s3_bucket()                   # Creates a new S3 bucket in a given region
# - create_s3_folder()                   # Creates a virtual folder in an S3 bucket
# - def Initial_User_Data(user_data: dict, s3_client):      # Process all the user data and upload everything to amazon S3

# --- Link Extraction & Comparison ---
# - extract_links_from_markdown_only()  # Extracts links from markdown content
# - extract_links_only()                # Extracts the raw links list from scrape result
# - print_links_nicely()                # Prints all links in a clean, numbered format
# - get_new_urls_only()                 # Compares two URL lists and finds new ones
# - get_new_links()                     # Compares two lists of link dictionaries and finds new ones
# - get_new_URLs()                      # Compares old and new JSONs and returns unseen links


# --- OpenAI Integration ---
# - extract_news_links_from_scrape()   # Uses GPT to extract news links from scraped markdown


# --- Summarization & Digest Creation ---
# - summarize_articles_with_gpt()      # Summarizes scraped markdown articles using GPT
# - combine_all_summaries()            # Combines summaries from multiple AI sources
# - build_html_digest()                # Creates an HTML digest from summarized articles


# --- Email Delivery ---
# - send_summary_email()               # Sends the HTML digest via email












# ==================== UUID/User ID Generation ====================

#     /////////////////////////////////////
#     Generate a globally unique user ID using UUID4
#     /////////////////////////////////////
def generate_unique_user_id() -> str:
    """
    Generate a globally unique user ID with a 'user_' prefix using UUID4.

    Returns:
        str: A prefixed UUID string like 'user_123e4567-e89b-12d3-a456-426614174000'
    """
    return f"user_{uuid.uuid4()}"

#     /////////////////////////////////////
#     Generate a globally shortened unique user ID using UUID4
#     /////////////////////////////////////
def generate_short_user_id() -> str:
    """
    Generate a short unique user ID like 'user_8f14e45f'.

    Returns:
        str: A shortened UUID string with 'user_' prefix
    """
    short_id = str(uuid.uuid4())[:8]
    return f"user_{short_id}"

# ==================== Web Scraping ====================

#     /////////////////////////////////////
#     URL Scraper with Firecrawl
#     /////////////////////////////////////

# Retry wrapper with exponential backoff
async def retry_with_backoff(coro_func, retries=3, base_delay=1, timeout=30):
    for attempt in range(retries):
        try:
            return await asyncio.wait_for(coro_func(), timeout=timeout)
        except Exception as e:
            if attempt == retries - 1:
                raise e
            delay = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
            print(f"🔁 Retry {attempt + 1}/{retries} after {delay:.1f}s due to error: {e}")
            await asyncio.sleep(delay)



async def Scrape(url: str) -> dict:
    try:
        app = AsyncFirecrawlApp(api_key='fc-e8846f8f7b184f6a84c3df19bae6682e')

        # Use retry and timeout logic around the scrape_url call
        response = await retry_with_backoff(
            lambda: app.scrape_url(
                url=url,
                formats=['markdown', 'links', 'rawHtml', 'screenshot'],
                only_main_content=True,
                proxy="stealth"
            ),
            retries=3,
            base_delay=1,
            timeout=30
        )

        # Safety check in case rawHtml is missing or malformed
        if not response.rawHtml:
            raise ValueError("No raw HTML returned by Firecrawl.")

        # Extract text content using BeautifulSoup
        soup = BeautifulSoup(response.rawHtml, 'html.parser')
        content_lines = []

        for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']):
            tag_name = tag.name.upper()
            text = tag.get_text(strip=True)
            if tag_name.startswith("H"):
                content_lines.append(f"\n{text}:\n")
            else:
                content_lines.append(text)

        content = "\n".join(content_lines)

        # 🔒 Truncate content to 20,000 characters if necessary
        max_chars = 20000
        if len(content) > max_chars:
            content = content[:max_chars]

        # Return structured result
        return {
            "Scraped URL": url,
            "Links": response.links,
            "Screenshot": response.screenshot,
            "Content": content,
            "Error": True  # ✅ Success
        }

    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        return {
            "Scraped URL": url,
            "Links": [],
            "Screenshot": None,
            "Content": "",
            "Error": False,  # ❌ Failure
            "ErrorMessage": str(e)
        }


 # Function to scrape multiple URLs
async def Scrape_Multiple(urls: list) -> list:
    tasks = [Scrape(url) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=False)
    return results



# Run the batch scrape and log everything (no file output)
async def Scrape_Multiple_Run(urls):
    print("🚀 Starting batch scrape...\n")

    results = await Scrape_Multiple(urls)

    success_count = 0
    fail_count = 0
    all_errors = []

    for i, result in enumerate(results):
        url = result.get("Scraped URL", "Unknown")
        print(f"\n📄 [{i+1}/{len(results)}] {url}")

        if result.get("Error") is True:
            print("✅ SUCCESS")
            print(f"🔗 Links found: {len(result['Links'])}")
            print(f"📝 Content length: {len(result['Content'])} characters")
            success_count += 1
        else:
            print("❌ FAILED")
            print(f"💬 Reason: {result.get('ErrorMessage', 'Unknown error')}")
            all_errors.append({
                "URL": url,
                "ErrorMessage": result.get("ErrorMessage", "Unknown error")
            })
            fail_count += 1

    print("\n✅ Finished scraping.")
    print(f"✔️ {success_count} succeeded")
    print(f"❌ {fail_count} failed")

    # ✅ Just return the results directly — no saving to files
    return {
        "results": results,
        "summary": {
            "success": success_count,
            "fail": fail_count,
            "errors": all_errors
        }
    }





            



# ==================== Scheduler / Automation ====================




# ==================== S3 Storage Operations ====================

#     /////////////////////////////////////
#     Downloads a JSON file from S3 and returns it as a Python dictionary.
#     /////////////////////////////////////
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


#     /////////////////////////////////////
#     Uploads a Python dictionary as a JSON file to S3.
#     /////////////////////////////////////
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
    
#     /////////////////////////////////////
#     Lists all bucket names in the connected AWS account.
#     /////////////////////////////////////
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

#     /////////////////////////////////////
#     Lists all object keys (files) in a specific S3 bucket (optionally under a prefix/folder).
#     /////////////////////////////////////
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

#     /////////////////////////////////////
#     Creates a new S3 bucket in the specified AWS region.
#     /////////////////////////////////////
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

#     /////////////////////////////////////
#     Creates a 'folder' in an S3 bucket by uploading a zero-byte object ending with '/'.
#     /////////////////////////////////////
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


#     /////////////////////////////////////
#     Lists all .json files in a specific folder (prefix) in an S3 bucket.
#     /////////////////////////////////////
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



#     /////////////////////////////////////
#     Opens a JSON file in S3 (expected to be a list of dicts), checks if an email exists,
#     appends a new element if it's not a duplicate, and uploads the updated file back to S3.
#     /////////////////////////////////////
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




        

#     /////////////////////////////////////
#     Processes user data by.
#     /////////////////////////////////////
async def Initial_user_Data(user_data: dict, s3_client):
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
            scrape_result = await Scrape(url)

            # If scraping failed, skip
            if not scrape_result.get("Error"):
                logging.warning(f"⚠️ Scraping failed for {url}: {scrape_result.get('ErrorMessage', 'Unknown error')}")
                continue


             # Transform the scrape result to match your S3 schema
            formatted_result = {
                "url": scrape_result["Scraped URL"],
                "markdown": scrape_result["Content"],
                "links": scrape_result["Links"],
                "error": not scrape_result["Error"]  # True if it failed, False if success
            }
            
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





# ==================== Summarization & Digest Creation ====================

#     /////////////////////////////////////
#     Uses GPT to summarize each scraped article from markdown
#     /////////////////////////////////////
def GPT_Summarizer(markdown_content: str) -> str:
    """
    Summarizes given content in a journalistic tone with a headline.

    Parameters:
        markdown_content (str): Raw article content to summarize.

    Returns:
        str: A summary with a title, written in a professional news tone.
    """
    if not markdown_content.strip():
        return "No content available to summarize."

    system_prompt = "You are an experienced journalist writing for a professional news publication."

    user_prompt = f"""Summarize the following article in a clear and professional tone. At the top of the summary, include a compelling and relevant title. The rest of the summary should:

- Be under 500 words
- Capture the main arguments, tone, and insights of the article
- Use natural, narrative-style paragraphs (no bullet points or lists)
- Include quotes or paraphrased lines if useful
- Avoid all formatting (no markdown, headings, etc.)
- Never mention that this is a summary or refer to the original article

Article:
\"\"\"
{markdown_content}
\"\"\""""

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


###############################################################
#                                NEW
###############################################################


# Clear previous handlers if running in Jupyter multiple times
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Set up logging to display in JupyterLab output cells
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)







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



async def User_Daily_Digest(user_id: str, bucket_name: str, s3_client):


    User_Profile = load_user_profile_from_s3(user_id, bucket_name, s3_client)
    print("User Profile")
    print(json.dumps(User_Profile, indent=4))
    print("\n\n\n")

    prefix = f"{user_id}/"
    json_files_List = list_json_files_in_folder(bucket_name, prefix, s3_client)

    print("The available JSON files are here:")
    print(json.dumps(json_files_List, indent=4))
    print("\n\n\n")

    all_new_links = []  # collect all new links from all the URLs

    for s3_key in json_files_List:
        filename = s3_key.split("/")[-1]
        if filename == "profile.json":
            continue

        full_key = f"{prefix}{filename}"
        Yesterday_Data = download_json_from_s3(full_key, full_key, bucket_name, s3_client)
        Today_Data = await Scrape(Yesterday_Data['Scraped URL'])
        upload_json_to_s3(full_key, full_key, bucket_name, Today_Data, s3_client)

        Yesterday_Links = Yesterday_Data.get("Links", [])
        today_Links = Today_Data.get("Links", [])

        # ✅ Filter links to match the domain of the Scraped URL
        source_domain = urlparse(Yesterday_Data['Scraped URL']).netloc.replace("www.", "").lower()
        today_Links = [
            link for link in today_Links
            if urlparse(link).netloc.replace("www.", "").lower() == source_domain
        ]
        
        New_Links = list(set(today_Links) - set(Yesterday_Links))
        all_new_links.extend(New_Links)

        # ✅ Enforce user's total new link scraping limit
        max_links = User_Profile.get("sources_Limit", 5)
        all_new_links = all_new_links[:max_links]

    print("All New Links:")
    print(json.dumps(all_new_links, indent=4))
    print("\n\n\n\n\n\n")

    # Step: Run batch scraping on all new links
    scrape_response = await Scrape_Multiple_Run(all_new_links)
    scraped_data_list = scrape_response["results"]

    # Enhance each item with a "Summary" generated by GPT_Summarizer
    for i, item in enumerate(scraped_data_list):
        content = item.get("Content", "")
        summary = GPT_Summarizer(content)  # Assumes GPT_Summarizer is sync
        updated_item = {}
        for key in item:
            updated_item[key] = item[key]
            if key == "Content":
                updated_item["Summary"] = summary
        scraped_data_list[i] = updated_item

    print("Final dictionary:")
    print(json.dumps(scraped_data_list, indent=4))

    # Prepare data for PDF and email
    all_summaries = []
    for item in scraped_data_list:
        summary_entry = {
            "url": item.get("Scraped URL", "N/A"),
            "screenshot": item.get("Screenshot", ""),
            "summary": item.get("Summary", "No summary available.")
        }
        all_summaries.append(summary_entry)

    data_for_pdf = {
        "all_summaries": all_summaries
    }

    pdf_url = Generate_PDF(template_id, data_for_pdf)

    # Generate the audio file

    # Extract all summaries
    summaries = [entry.get("Summary", "") for entry in all_summaries]
    
    # Combine them into one string with pauses for readability
    combined_summary = "\n\n".join(summaries)


    # Create an audio file for the podcast:

    # response = openai.audio.speech.create(
    #     model="gpt-4o-mini-tts",  # or "tts-1-hd" for high-definition
    #     voice="nova",   # Options: "alloy", "echo", "fable", "onyx", "nova", "shimmer", "ash", "ballad", "coral", "sage"
    #     input=combined_summary
    # )
    
    # Save the audio to a file
    # with open("output_audio.mp3", "wb") as f:
    #     f.write(response.content)
    
    # print("Audio file saved as output_audio.mp3")





    if not all_summaries:
        print("📭 No new summaries today. Sending no-news email...")
    else:
        print(f"📬 Preparing to send {len(all_summaries)} summaries...")

    send_summary_email(
        summaries=all_summaries,
        sender_email=Email_SyncLiving_Sender,
        sender_password=Email_SyncLiving_Sender_AppPassword,
        recipient_email=User_Profile["email"],
        pdf_url=pdf_url
    )






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



def run_all_users():
    logging.info("🔄 Running summarization for all users...")
    User_Daily_scraping_and_summarization("user_8f14e45f", bucket_name, amazon_s3)
    User_Daily_scraping_and_summarization("user_deada551", bucket_name, amazon_s3)
    User_Daily_scraping_and_summarization("user_b4fa9ce2", bucket_name, amazon_s3)
    logging.info("✅ Finished summarization for all users.")



def start_scheduler():
    scheduler = BackgroundScheduler(timezone=melbourne_tz)

    times = [
        (12, 00),
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










