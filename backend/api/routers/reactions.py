import hashlib
import os

from django.db.models import Count
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from blog.models import Post, Reaction

router = APIRouter()

_SALT = os.getenv("REACTION_SALT", "reaction-salt-change-in-prod")
_VALID = {"like", "love", "fire"}


class ReactionRequest(BaseModel):
    emoji: str


class ReactionOut(BaseModel):
    like: int = 0
    love: int = 0
    fire: int = 0
    user_reactions: list[str] = []


def _hash_ip(ip: str) -> str:
    return hashlib.sha256(f"{_SALT}:{ip}".encode()).hexdigest()[:32]


def _build_response(post: Post, ip_hash: str) -> ReactionOut:
    counts = {
        row["emoji"]: row["n"]
        for row in Reaction.objects.filter(post=post)
        .values("emoji")
        .annotate(n=Count("id"))
    }
    user_reactions = list(
        Reaction.objects.filter(post=post, ip_hash=ip_hash).values_list(
            "emoji", flat=True
        )
    )
    return ReactionOut(
        like=counts.get("like", 0),
        love=counts.get("love", 0),
        fire=counts.get("fire", 0),
        user_reactions=user_reactions,
    )


@router.get("/{slug}/reactions", response_model=ReactionOut)
def get_reactions(slug: str, request: Request):
    try:
        post = Post.objects.get(slug=slug, published=True)
    except Post.DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")
    ip_hash = _hash_ip(request.client.host or "unknown")
    return _build_response(post, ip_hash)


@router.post("/{slug}/reactions", response_model=ReactionOut)
def toggle_reaction(slug: str, data: ReactionRequest, request: Request):
    if data.emoji not in _VALID:
        raise HTTPException(status_code=400, detail="Invalid emoji")
    try:
        post = Post.objects.get(slug=slug, published=True)
    except Post.DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")
    ip_hash = _hash_ip(request.client.host or "unknown")
    obj, created = Reaction.objects.get_or_create(
        post=post, emoji=data.emoji, ip_hash=ip_hash
    )
    if not created:
        obj.delete()
    return _build_response(post, ip_hash)
