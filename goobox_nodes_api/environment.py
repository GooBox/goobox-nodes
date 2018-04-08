from apistar import environment, typesystem


class Env(environment.Environment):
    properties = {
        'DEBUG': typesystem.boolean(default=False),
        'DATABASE_HOST': typesystem.string(min_length=1),
        'DATABASE_PORT': typesystem.string(min_length=1),
        'DATABASE_USER': typesystem.string(min_length=1),
        'DATABASE_PASSWORD': typesystem.string(min_length=1),
        'DATABASE_NAME': typesystem.string(min_length=1),
    }


env = Env()
