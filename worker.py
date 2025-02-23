from celery import Celery
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import os
import uuid
from database import get_db_session

app = Celery("tasks", broker="redis://localhost:6379/0")

OUTPUT_FOLDER = "processed_images"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.task
def process_images_task(request_id, file_path):
    session = get_db_session()
    session.execute("UPDATE Requests SET status = :status WHERE request_id = :id",
                    {"status": "Processing", "id": request_id})
    session.commit()

    df = pd.read_csv(file_path)

    for index, row in df.iterrows():
        product_name = row["Product Name"]
        image_urls = row["Input Image Urls"].split(",")

        for url in image_urls:
            try:
                response = requests.get(url.strip())
                image = Image.open(BytesIO(response.content))

                output_image_path = os.path.join(OUTPUT_FOLDER, f"{uuid.uuid4()}.jpg")
                image.save(output_image_path, "JPEG", quality=50)

                session.execute("INSERT INTO Images (product_name, input_image_url, output_image_url, status) VALUES (:pname, :input_url, :output_url, :status)",
                                {"pname": product_name, "input_url": url, "output_url": output_image_path, "status": "Completed"})
                session.commit()

            except Exception as e:
                print(f"Error processing {url}: {e}")

    session.execute("UPDATE Requests SET status = :status WHERE request_id = :id",
                    {"status": "Completed", "id": request_id})
    session.commit()
    session.close()
