from json import JSONDecodeError
import json as j
import json
from jinja2 import Template

class Extract:

    def __init__(self, file):
        self.arq = file

    def get_paths(self):
        return self.arq["paths"]

    def generate(self):
        paths = self.get_paths()

        template = Template("""
            <form action="saida.html" method="post"> 
                <table>
                    {% for path, path_object in paths.items() %}
                        {% for verb, verb_object in path_object.items() %}
                            <tr>
                                <td> <input type="checkbox"  id="{{ path }}" name="{{ path }}"> {{ path }}</td>
                                <td> <input type="checkbox"  id="{{ verb }}" > {{ verb }}</td>
                                {% for parameter in verb_object["parameters"] %}
                                    <td>{{ parameter["name"] }}</td>
                                    <td>{% if parameter.get("required", False) %}Yes{% else %}No{% endif %}</td>
                                {% endfor %}
                            </tr>
                        {% endfor %}
                    {% endfor %}
                    </table>

                    <div class="form-example">
                        <input type="submit" value="Subscribe!">
                    </div>
            </form>
        """)

        html = template.render(paths=paths)

        return html