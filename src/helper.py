from flask import request, abort


def auth(key):
    def authorized(fn):
        """Decorator that checks that requests
        contain an id-token in the request header.
        userid will be None if the
        authentication failed, and have an id otherwise.

        Usage:
        @app.route("/")
        @auth("somekey")
        def secured_root(userid=None):
            pass
        """

        def _wrap(*args, **kwargs):
            if 'Authorization' not in request.headers:
                # Unauthorized
                print("No token in header")
                abort(401)


            if key not in request.headers['Authorization']:
                # Unauthorized
                print("Key not in auth header")
                abort(401)

            return fn(*args, **kwargs)
        return _wrap
    return authorized

