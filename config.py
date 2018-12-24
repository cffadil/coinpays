import aumbry


class DatabaseConfig(aumbry.YamlConfig):
    __mapping__ = {
        'connection': ['connection', str],
    }

    connection = ''


class WaitressConfig(aumbry.YamlConfig):
    __mapping__ = {
        'listen': ['listen', str]
    }
    listen = '0.0.0.0:8800'


class JWTConfig(aumbry.YamlConfig):
    __mapping__ = {
        'secret': ['secret', str],
        'expiry': ['expiry', int],
        'leeway': ['leeway', int],
        'algorithm': ['algorithm', str],
        'issuer': ['issuer', str],
        'prefix': ['prefix', str],
    }

    secret = ''
    expiry = 365 * 24 * 60 * 60


class AppConfig(aumbry.YamlConfig):
    __mapping__ = {
        'db': ['db', DatabaseConfig],
        'gunicorn': ['gunicorn', dict],
        'jwt': ['jwt', JWTConfig],
        'waitress': ['waitress', WaitressConfig]
    }

    db = DatabaseConfig()
    gunicorn = {}
