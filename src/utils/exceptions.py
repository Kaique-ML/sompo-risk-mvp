class SompoError(Exception):
    """Base."""
class DataValidationError(SompoError): pass
class ModelNotTrainedError(SompoError): pass
class AuthenticationError(SompoError): pass
class AuthorizationError(SompoError): pass
class DatabaseError(SompoError): pass
