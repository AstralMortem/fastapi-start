% for line in old_imports:
${line}
% endfor
from .${snake_name} import ${camel_name}View

ENDPOINTS = [
    % for path in old_code:
    ${path}
    % endfor
    path('/${snake_name}s', ${camel_name}View),
]