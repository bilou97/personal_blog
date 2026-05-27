from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class SiteConfigOut(BaseModel):
    bio_emoji: str
    bio_title: str
    bio_content: str


@router.get("", response_model=SiteConfigOut)
def get_config():
    from blog.models import SiteConfig
    cfg = SiteConfig.get()
    return SiteConfigOut(
        bio_emoji=cfg.bio_emoji,
        bio_title=cfg.bio_title,
        bio_content=cfg.bio_content,
    )
