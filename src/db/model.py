from datetime import datetime

from pydantic import BaseModel

class ScraperRecord(BaseModel):
    raw_cnt: int = 0
    cleaned_cnt: int = 0
    upd_dt: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class CleanedComments(BaseModel):
    batch_no: int
    name: str = 'Jane Doe'

class FeaturedComments(BaseModel):
    batch_no: int
    comment_dt: str = ''
    score: int = 0
    comment: str = ''