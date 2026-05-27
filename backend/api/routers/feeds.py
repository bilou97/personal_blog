from email.utils import format_datetime

from fastapi import APIRouter
from fastapi.responses import Response

from blog.models import Post

router = APIRouter()

SITE_URL = "https://blog.papobilou.ch"
BLOG_TITLE = "papobilou"
BLOG_DESCRIPTION = "Articles sur le développement web, DevOps et les outils du quotidien."


@router.get("/feed.xml")
def rss_feed():
    posts = (
        Post.objects.filter(published=True)
        .order_by("-published_at")[:20]
    )

    items = ""
    for post in posts:
        pub_date = format_datetime(post.published_at) if post.published_at else ""
        link = f"{SITE_URL}/posts/{post.slug}"
        items += f"""
    <item>
      <title><![CDATA[{post.title}]]></title>
      <link>{link}</link>
      <guid>{link}</guid>
      <description><![CDATA[{post.excerpt}]]></description>
      <pubDate>{pub_date}</pubDate>
    </item>"""

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{BLOG_TITLE}</title>
    <link>{SITE_URL}</link>
    <description>{BLOG_DESCRIPTION}</description>
    <language>fr</language>
    <atom:link href="{SITE_URL}/feed.xml" rel="self" type="application/rss+xml"/>
{items}
  </channel>
</rss>"""

    return Response(content=xml, media_type="application/rss+xml; charset=utf-8")


@router.get("/sitemap.xml")
def sitemap():
    posts = Post.objects.filter(published=True).order_by("-updated_at")

    urls = f"""  <url>
    <loc>{SITE_URL}/</loc>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>"""

    for post in posts:
        lastmod = post.updated_at.strftime("%Y-%m-%d")
        urls += f"""
  <url>
    <loc>{SITE_URL}/posts/{post.slug}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>"""

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>"""

    return Response(content=xml, media_type="application/xml; charset=utf-8")
