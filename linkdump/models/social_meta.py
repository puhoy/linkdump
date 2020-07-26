from datetime import date, datetime
import re

import requests
from bs4 import BeautifulSoup
from readability import Document
from sqlalchemy import Index, or_, and_

from linkdump import db, dramatiq
from xml.etree import ElementTree

from linkdump.models import User


class SocialMeta(db.Model):
    __tablename__ = 'social_meta'

    id = db.Column(db.Integer, primary_key=True)

    description = db.Column(db.String(), nullable=True)

    twitter_card_summary = db.Column(db.String(), nullable=True)

    og_title = db.Column(db.String(), nullable=True)
    og_type = db.Column(db.String(), nullable=True)
    og_url = db.Column(db.String(), nullable=True)
    og_image = db.Column(db.String(), nullable=True)
    og_description = db.Column(db.String(), nullable=True)
    og_site_name = db.Column(db.String(), nullable=True)

    #article_published_time = db.Column(db.String(), nullable=True)
    #article_modified_time = db.Column(db.String(), nullable=True)
    #article_section = db.Column(db.String(), nullable=True)
    #article_tag = db.Column(db.String(), nullable=True)

    @staticmethod
    def get_social_meta(html):
        social_meta = SocialMeta()
        soup = BeautifulSoup(html, features="lxml")

        description = soup.find("meta", dict(name="description"))

        og_description = soup.find("meta", property="og:description")
        og_site_name = soup.find("meta", property="og:site_name")
        og_image = soup.find("meta", property="og:image")
        og_title = soup.find("meta", property="og:title")
        og_url = soup.find("meta", property="og:url")

        social_meta.description = description.get('content') if description else None
        social_meta.og_description = og_description.get('content') if og_description else None
        social_meta.og_site_name = og_site_name.get('content') if og_site_name else None
        social_meta.og_image = og_image.get('content') if og_image else None
        social_meta.og_title = og_title.get('content') if og_title else None
        social_meta.og_url = og_url.get('content') if og_url else None

        return social_meta

"""
<!-- Open Graph data -->
<meta property="og:title" content="Title Here" />
<meta property="og:type" content="article" />
<meta property="og:url" content="http://www.example.com/" />
<meta property="og:image" content="http://example.com/image.jpg" />
<meta property="og:description" content="Description Here" />
<meta property="og:site_name" content="Site Name, i.e. Moz" />
<meta property="article:published_time" content="2013-09-17T05:59:00+01:00" />
<meta property="article:modified_time" content="2013-09-16T19:08:47+01:00" />
<meta property="article:section" content="Article Section" />
<meta property="article:tag" content="Article Tag" />
<meta property="fb:admins" content="Facebook numberic ID" /> 
"""