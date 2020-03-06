{% extends "_main.html.jinja2" %}
{% block content %}

## linkdump

open feeds on this server:
[]

{% if current_user.is_anonymous %}
[login]({{url_for('security.login')}})
[register]({{url_for('security.register')}})

{% else %}

#### hey, {{ current_user.email }}

[logout]({{url_for('security.logout')}})

[change_password]({{url_for('security.change_password')}})


the link to your rss feed is [{{url_for('atom_feed')}}]({{url_for('atom_feed')}}) (dont forget to use authentication when setting it up in your feed reader!)

afterwards, start posting to [{{url_for('add_item')}}]({{url_for('add_item')}}), eg 

```
http POST http://feeds.example.com/items url='https://github.com/puhoy/linkdump' -a "user_email:password" 
```

{% endif %}

{% endblock %}

