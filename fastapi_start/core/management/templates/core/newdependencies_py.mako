% for line in old_imports:
${line}
% endfor
from ${project_name}.repositories.${snake_name} import ${camel_name}RepositoryImpl
from ${project_name}.services.${snake_name} import ${camel_name}Service
% for line in old_code:
${line}
% endfor
def get_${snake_name}_service(db: AsyncSession = Depends(get_db)):
    return ${camel_name}Service(${camel_name}RepositoryImpl(db))