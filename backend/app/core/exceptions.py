class AgentError(Exception):
    """Base class for all agent-related exceptions."""
    pass

# ------------------------------------RDBMS------------------------------------

class RDBMSError(AgentError):
    """Raised when there is an issue with the RDBMS."""
    pass

class RDBMSConnectionError(RDBMSError):
    """Raised when a connection to the RDBMS cannot be established."""
    pass

class RDBMSQueryError(RDBMSError):
    """Raised when there is an error executing a query on the RDBMS."""
    pass

# -------------------------------------API-------------------------------------

class ApiError(AgentError):
    """Raised when there is an issue with an API request."""
    pass