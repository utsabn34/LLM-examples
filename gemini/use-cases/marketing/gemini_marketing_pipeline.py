import os
import json
import sys
from google import genai
from google.genai import types
from google.genai.types import GenerateContentConfig, GoogleSearch, Tool
from pydantic import BaseModel
from IPython.display import Markdown, display


# ========= CONFIGURATION =========
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "[your-project-id]")
LOCATION = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")
MODEL_ID = "gemini-2.0-flash-001"

# ========= INIT CLIENT =========
client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)


# ========= MARKETING BRIEF CLASS =========
class MarketingCampaignBrief(BaseModel):
    campaign_name: str
    campaign_objectives: list[str]
    target_audience: str
    media_strategy: list[str]
    timeline: str
    target_countries: list[str]
    performance_metrics: list[str]


# ========= EXTRACT CAMPAIGN BRIEF =========
marketing_brief_file_path = "sample_marketing_campaign_brief.pdf"
marketing_brief_file_url = f"https://storage.googleapis.com/{marketing_brief_file_path}"

print("Reading marketing brief from:")
print(marketing_brief_file_url)

brief_prompt = "Extract the details from the sample marketing brief."
brief_file = types.Part.from_uri(file_uri=marketing_brief_file_url, mime_type="application/pdf")
contents = [brief_file, brief_prompt]

response = client.models.generate_content(
    model=MODEL_ID,
    contents=contents,
    config=GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=MarketingCampaignBrief,
    ),
)

sample_marketing_brief = response.text
sample_marketing_brief_json = json.loads(sample_marketing_brief)
print("Extracted Marketing Brief:")
print(json.dumps(sample_marketing_brief_json, indent=2))


# ========= MARKET RESEARCH =========
def print_grounding_response(response):
    grounding_metadata = response.candidates[0].grounding_metadata
    text = response.text

    print("\nResponse:\n", text)
    print("\nGrounding Sources:")
    for i, chunk in enumerate(grounding_metadata.grounding_chunks, start=1):
        context = chunk.web or chunk.retrieved_context
        if context:
            print(f"{i}. {context.title} ({context.uri})")


market_research_prompt = """
I am planning to launch a mobile phone campaign and I want to understand the latest trends in the phone industry.
Please answer the following questions:
- What are the latest phone models and their selling point from the top 2 phone makers?
- What is the general public sentiment about mobile phones?
"""

contents = [market_research_prompt]
google_search_tool = Tool(google_search=GoogleSearch())

response = client.models.generate_content(
    model=MODEL_ID,
    contents=contents,
    config=GenerateContentConfig(tools=[google_search_tool]),
)

market_research = response.text
print_grounding_response(response)


# ========= CREATE NEW CAMPAIGN BRIEF =========
new_phone_details = """
Phone Name: Pix Phone 10
Short description: Pix Phone 10 is the flagship phone with a focus on AI-powered features and a completely redesigned form factor.
Tech Specs:
  - Camera: 50MP main sensor with 48MP ultrawide lens with autofocus for macro shots
  - Performance: P5 processor for fast performance and AI capabilities
  - Battery: 4700mAh battery for all-day usage
Key Highlights:
  - Powerful camera system
  - Redesigned software user experience to introduce more fun
  - Compact form factor
Launch timeline: Jan 2025
Target countries: US, France and Japan
"""

create_brief_prompt = f"""
Given the following details, create a marketing campaign brief for the new phone launch:

Sample campaign brief:
{sample_marketing_brief}

Market research:
{market_research}

New phone details:
{new_phone_details}
"""

contents = [create_brief_prompt]

response = client.models.generate_content(
    model=MODEL_ID,
    contents=contents,
    config=GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=MarketingCampaignBrief,
    ),
)

creative_brief = response.text
creative_brief_json = json.loads(creative_brief)
print("New Campaign Brief:")
print(json.dumps(creative_brief_json, indent=2))


# ========= AD COPY GENERATION =========
class AdCopy(BaseModel):
    ad_copy_options: list[str]
    localization_notes: list[str]
    visual_description: list[str]


ad_copy_prompt = f"""
Given the marketing campaign brief, create an Instagram ad-copy for each target market: {creative_brief_json["target_countries"]}
Please localize the ad-copy and the visuals to the target markets for better relevancy to the target audience.
Marketing Campaign Brief:
{creative_brief}
"""

contents = [ad_copy_prompt]

response = client.models.generate_content(
    model=MODEL_ID,
    contents=contents,
    config=GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=AdCopy,
    ),
)

ad_copy = response.text
ad_copy_json = json.loads(ad_copy)
print("Localized Ad Copy:")
print(json.dumps(ad_copy_json, indent=2, ensure_ascii=False))


# ========= SHORT VIDEO STORYBOARD =========
short_video_prompt = f"""
Given the marketing campaign brief, create a storyboard for a YouTube Shorts video for target markets: {creative_brief_json["target_countries"]}.
Please localize the content to the target markets for better relevancy to the target audience.
Marketing Campaign Brief:
{creative_brief}
"""

contents = [short_video_prompt]

response = client.models.generate_content(model=MODEL_ID, contents=contents)
short_video_response = response.text

print("\nStoryboard Output:")
print(short_video_response)


# ========= DONE =========
print("\n✅ All steps completed successfully.")
