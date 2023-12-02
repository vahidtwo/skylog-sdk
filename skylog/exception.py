class CustomBaseException(Exception):
    """
    Custom Exception class with default message
    this class can be inherited to create custom exception
    Parameter:
        message (str): default message that replace with default_message
        extra_explanation (str): message that added to default message
        **kwargs: keyword arguments that apply to the default message for string formatting
    examples:
        >>> class MyException(CustomBaseException):
        >>>     default_message = "My Exception {some_explain}"
        >>>     def __init__(self, explain_detail: str = None, **kwargs):
        >>>         super().__init__(some_explain=explain_detail, **kwargs)
      usage:
        >>> raise MyException("api error.", extra_explanation="IDK") # MyException("api error. IDK")

        >>> raise MyException(explain_detail="api error.", extra_explanation="IDK")
        >>> # MyException("My Exception api error.IDK")
    """

    default_message = ""

    def __init__(self, /, message: str = None, *, extra_explanation: str = "", **kwargs: Optional[Union[str, int]]):
        message = f"{self.default_message}" if message is None else f"{message}"
        if extra_explanation:
            message = f"{message}\n{extra_explanation}"
        message = message.format(**kwargs)
        super().__init__(message)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.args[0] if self.args else ''}')"


class RetryException(CustomBaseException):
    default_message = "Could not complete the routine"

    def __init__(self, count: int = None):
        extra_explanation = "" if count is not None else f" after {count} retries"
        super().__init__(extra_explanation=extra_explanation)


class UploadedFileNotFound(CustomBaseException):
    default_message = "Our payment file not found on ftp server"


class ShaparakReportFileNotFound(CustomBaseException):
    default_message = "Shaparak reported file not found on ftp server"


class ShaparakReportFileHaseErrorFound(CustomBaseException):
    default_message = "Shaparak reported file hase error ftp server"


class ShaparakAnnouncementFileNotFound(CustomBaseException):
    default_message = "Shaparak announcement file not found on ftp server"
