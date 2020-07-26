import unittest

from linkdump.models import Item

html = """<!DOCTYPE html>
<html lang='en'>
<head>
<meta charset='utf-8'>
<meta content='#282c37' name='theme-color'>
<title>stay hydrated: &quot;@pony :winking_face:&quot; - Mastodon</title>
<meta content="Mastodon" property="og:site_name" />
<meta content="article" property="og:type" />
<meta content="og_title_content" property="og:title" />
<meta content="https://server.tld/" property="og:url" />
<meta content='description_content' name='description'>
<meta content="og_description_content" property="og:description" />
<meta content="https://subversive.zone/system/accounts/avatars/000/000/678/original/f76e30c2483ddba5.png?1591609844" property="og:image" />
<meta content="120" property="og:image:width" />
<meta content="120" property="og:image:height" />
<meta content="summary" property="twitter:card" />
</head>
<body class='with-modals theme-default no-reduce-motion'>
</body>
</html>
"""


class TestSum(unittest.TestCase):
    def test_get_social_meta(self):
        item = Item()
        social_meta = item.get_social_meta(html)
        
        assert social_meta.description == 'description_content'
        assert social_meta.og_description == 'og_description_content'
