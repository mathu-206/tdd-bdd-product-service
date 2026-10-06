"""JSON error handlers"""
from flask import jsonify
from service import app
from service.models import DataValidationError
from service.common import status


def _message(error):
    return getattr(error, "description", None) or str(error)


@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """Handles data validation errors"""
    return bad_request(error)


@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
    """Handles bad requests"""
    return (
        jsonify(status=400, error="Bad Request", message=_message(error)),
        status.HTTP_400_BAD_REQUEST,
    )


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    """Handles resources not found"""
    return (
        jsonify(status=404, error="Not Found", message=_message(error)),
        status.HTTP_404_NOT_FOUND,
    )


@app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
def method_not_supported(error):
    """Handles unsupported HTTP methods"""
    return (
        jsonify(status=405, error="Method not Allowed", message=_message(error)),
        status.HTTP_405_METHOD_NOT_ALLOWED,
    )


@app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
def mediatype_not_supported(error):
    """Handles unsupported media requests"""
    return (
        jsonify(status=415, error="Unsupported media type", message=_message(error)),
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    )


@app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    """Handles unexpected server errors"""
    return (
        jsonify(status=500, error="Internal Server Error", message=_message(error)),
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
