class InitApp:
    @staticmethod
    def init_app(config, app):
        if app.__class__.__name__ == 'Flask':
            from flask import Flask
            assert isinstance(app, Flask)
            return InitApp.init_flask(config, app)
        else:
            raise NotImplementedError("There is no support yet for {} application".format(
                app.__class__.__name__
            ))

    @staticmethod
    def init_flask(config, app):
        app.config.update(config)
