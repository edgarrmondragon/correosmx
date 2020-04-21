from typing import Iterable, Mapping

from jinja2 import Environment

def render_tracking(events: Iterable[Mapping[str, str]], env: Environment) -> str:
    template = env.get_template('tracking.html')
    return template.render(events=events)
