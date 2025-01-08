from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import os
import uuid
from datetime import datetime
from fastapi.staticfiles import StaticFiles

# FastAPI app
app = FastAPI()

# In-memory database (replace with a real database in production)
db = {
    "content": []
}

# Content model
class Content(BaseModel):
    id: str
    type: str  # e.g., "product", "blog", "page"
    title: str
    slug: str
    description: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

# Directory to store uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Endpoint to create content
@app.post("/content/", response_model=Content)
async def create_content(
    type: str,
    title: str,
    slug: str,
    description: Optional[str] = None,
    meta_title: Optional[str] = None,
    meta_description: Optional[str] = None,
    image: Optional[UploadFile] = File(None)
):
    """
    Create new content (e.g., product, blog post, page).
    """
    content_id = str(uuid.uuid4())
    image_url = None
    if image:
        file_extension = image.filename.split(".")[-1]
        image_filename = f"{content_id}.{file_extension}"
        image_path = os.path.join(UPLOAD_DIR, type, image_filename)
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        with open(image_path, "wb") as buffer:
            buffer.write(await image.read())
        image_url = f"/uploads/{type}/{image_filename}"

    content = {
        "id": content_id,
        "type": type,
        "title": title,
        "slug": slug,
        "description": description,
        "meta_title": meta_title,
        "meta_description": meta_description,
        "image_url": image_url,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    db["content"].append(content)
    return content

# Endpoint to get all content (with pagination and filtering)
@app.get("/content/", response_model=List[Content])
def get_content(
    type: Optional[str] = Query(None, description="Filter by content type"),
    skip: int = Query(0, description="Pagination offset"),
    limit: int = Query(10, description="Pagination limit")
):
    """
    Retrieve all content with optional filtering and pagination.
    """
    filtered_content = db["content"]
    if type:
        filtered_content = [item for item in filtered_content if item["type"] == type]
    return filtered_content[skip : skip + limit]

# Endpoint to get a single content by ID
@app.get("/content/{content_id}", response_model=Content)
def get_content_by_id(content_id: str):
    """
    Retrieve a single content item by its ID.
    """
    for content in db["content"]:
        if content["id"] == content_id:
            return content
    raise HTTPException(status_code=404, detail="Content not found")

# Endpoint to delete content
@app.delete("/content/{content_id}")
def delete_content(content_id: str):
    """
    Delete a content item by its ID.
    """
    for index, content in enumerate(db["content"]):
        if content["id"] == content_id:
            db["content"].pop(index)
            if content["image_url"]:
                image_filename = content["image_url"].split("/")[-1]
                image_path = os.path.join(UPLOAD_DIR, content["type"], image_filename)
                if os.path.exists(image_path):
                    os.remove(image_path)
            return {"message": "Content deleted"}
    raise HTTPException(status_code=404, detail="Content not found")

# Serve uploaded files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
