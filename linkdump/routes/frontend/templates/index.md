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


{% endif %}

{% endblock %}

