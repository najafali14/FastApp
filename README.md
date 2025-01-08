# FastApp
# FastAPI CMS
A headless CMS built with FastAPI for managing dynamic content like products, blog posts, and pages. This CMS is designed to be publicly accessible, making it easy to integrate with any frontend application.
# Features
Dynamic Content Types: Manage different types of content (e.g., products, blog posts, pages).

Image Uploads: Upload and store images for each content item.

SEO-Friendly: Add slug, meta_title, and meta_description fields for SEO optimization.

Public API: All endpoints are publicly accessible, making it easy to fetch data on the frontend.

Pagination and Filtering: Fetch content with pagination and filtering by type.

# Getting Started
Prerequisites
Python 3.7+

FastAPI

Uvicorn (for running the server)

# Installation
Clone the repository:

git clone https://github.com/your-username/fastapi-cms.git
cd fastapi-cms

# Install dependencies:

pip install -r requirements.txt
# Run the FastAPI app:
uvicorn main:app --reload
# Open your browser and navigate to:
http://127.0.0.1:8000/

