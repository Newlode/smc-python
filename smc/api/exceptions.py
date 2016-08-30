'''
Exceptions Module
'''
import json
import smc.api.web

class SMCException(Exception):
    """ Base class for exceptions """
    pass

class SMCConnectionError(SMCException):
    """
    Thrown when there are connection related issues with the SMC.
    This could be that the underlying http requests library could not connect
    due to wrong IP address, wrong port, or time out
    """
    pass

class ConfigLoadError(SMCException):
    """
    Thrown when there was a problem reading credential information from 
    file. Typically caused by missing settings.
    """
    pass
    
class SMCOperationFailure(SMCException):
    """ Exception class for storing results from calls to the SMC
    This is thrown for HTTP methods that do not return the expected HTTP
    status code. See each method above for expected success status
    
    :param response: response object returned from HTTP method
    :ivar response: http request response object
    :ivar code: http status code
    :ivar status: status from SMC API
    :ivar message: message attribute from SMC API
    :ivar details: details list from SMC API (may not always exist)
    :ivar smcresult: SMCResult object for consistent returns
    """
    def __init__(self, response=None, msg=None):
        self.response = response
        self.code = None
        self.status = None
        self.details = None
        self.message = None
        self.smcresult = smc.api.web.SMCResult(msg=msg)
        if response is not None:
            self.parse_error()
    
    def parse_error(self):
        self.code = self.response.status_code
        if self.response.headers.get('content-type') == 'application/json':
            data = json.loads(self.response.text)
            self.status = data.get('status', None)
            self.message = data.get('message', None)
            details = data.get('details', None)
            if isinstance(details, list):
                self.details = ' '.join(details)
            else:
                self.details = details
        else: #it's not json
            if self.response.text:
                self.message = self.response.text
            else:
                self.message = "HTTP error code: %s, no message" % self.code
    
        self.smcresult.msg = self.__str__()
        self.smcresult.code = self.code
        
    def __str__(self):
        if self.message and self.details:
            return "%s %s" % (self.message, ''.join(self.details))
        elif self.details:
            return ''.join(self.details)
        else:
            return self.message
        
    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

class CreateEngineFailed(SMCException):
    """ 
    Thrown when a POST operation returns with a failed response.
    API based response will be returned as the exception message
    """
    pass

class LoadEngineFailed(SMCException):
    """ Thrown when attempting to load an engine that does not
    exist
    """
    pass

class CreatePolicyFailed(SMCException):
    """
    Thrown when failures occur when creating specific
    poliies like Firewall Policy, IPS, VPN, etc.
    """
    pass

class LoadPolicyFailed(SMCException):
    """
    Failure when trying to load a specific policy type
    """
    pass

class CreateElementFailed(SMCException):
    """
    Generic exception when there was a failure calling a 
    create method
    """
    pass

class UnsupportedEngineFeature(SMCException):
    """
    If an operation is performed on an engine that does not support
    the functionality, this is thrown. For example, only Master Engine
    has virtual resources. IPS and Layer 2 Firewall do not have internal
    gateways (used for VPN).
    """
    pass