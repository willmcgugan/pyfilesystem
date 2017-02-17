"""
Defines the Exception classes thrown by PyFilesystem objects. Exceptions relating
to the underlying filesystem are translated in to one of the following Exceptions.
Exceptions that relate to a path store that path in `self.path`.

All Exception classes are derived from `FSError` which can be used as a
catch-all exception.

"""

__all__ = ['FSError',
           'CreateFailedError',
           'PathError',
           'InvalidPathError',
           'InvalidCharsInPathError',
           'OperationFailedError',
           'UnsupportedError',
           'RemoteConnectionError',
           'StorageSpaceError',
           'PermissionDeniedError',
           'FSClosedError',
           'OperationTimeoutError',
           'RemoveRootError',
           'ResourceError',
           'NoSysPathError',
           'NoMetaError',
           'NoPathURLError',
           'ResourceNotFoundError',
           'ResourceInvalidError',
           'DestinationExistsError',
           'DirectoryNotEmptyError',
           'ParentDirectoryMissingError',
           'ResourceLockedError',
           'NoMMapError',
           'BackReferenceError',
           'convert_fs_errors',
           'convert_os_errors',
           ]

import sys
import errno
import six

from fs.path import *
from fs.local_functools import wraps


class FSError(Exception):
    """Base exception class for the FS module."""
    default_message = "Unspecified error"

    def __init__(self, msg=None, details=None, originalExc=None):
        if msg is None:
            msg = self.default_message
        self.msg = msg
        self.details = details
        self.originalExc = originalExc

    def __str__(self):
        keys = {}
        for k, v in self.__dict__.iteritems():
            if isinstance(v, unicode):
                v = v.encode(sys.getfilesystemencoding())
            keys[k] = v
        return str(self.msg % keys)

    def __unicode__(self):
        keys = {}
        for k, v in self.__dict__.iteritems():
            if isinstance(v, six.binary_type):
                v = v.decode(sys.getfilesystemencoding(), 'replace')
            keys[k] = v
        return unicode(self.msg, encoding=sys.getfilesystemencoding(), errors='replace') % keys

    def __reduce__(self):
        return (self.__class__, (), self.__dict__.copy(),)


class CreateFailedError(FSError):
    """An exception thrown when a FS could not be created"""
    default_message = "Unable to create filesystem"


class PathError(FSError):
    """Exception for errors to do with a path string.
    """
    default_message = "Path is invalid (original_exc = %(originalExc)s): %(path)s"

    def __init__(self, path="", originalExc=None**kwds):
        self.path = path
        self.originalExc = originalExc
        super(PathError, self).__init__(**kwds)


class InvalidPathError(PathError):
    """Base exception for fs paths that can't be mapped on to the underlaying filesystem."""
    default_message = "Path is invalid on this filesystem  (original_exc = %(originalExc)s): %(details)s"


class InvalidCharsInPathError(InvalidPathError):
    """The path contains characters that are invalid on this filesystem"""
    default_message = "Path contains invalid characters (original_exc = %(originalExc)s): %(details)s"


class OperationFailedError(FSError):
    """Base exception class for errors associated with a specific operation."""
    default_message = "Unable to %(opname)s (original_exc = %(originalExc)s): unspecified error [%(errno)s - %(details)s]"

    def __init__(self, opname="", path=None, originalExc=None, **kwds):
        self.opname = opname
        self.path = path
        self.originalExc = originalExc
        self.errno = getattr(kwds.get("details", None), "errno", None)
        super(OperationFailedError, self).__init__(**kwds)


class UnsupportedError(OperationFailedError):
    """Exception raised for operations that are not supported by the FS."""
    default_message = "Unable to %(opname)s (original_exc = %(originalExc)s): not supported by this filesystem [%(details)s]"


class RemoteConnectionError(OperationFailedError):
    """Exception raised when operations encounter remote connection trouble."""
    default_message = "%(opname)s (original_exc = %(originalExc)s): remote connection errror [%(details)s]"


class StorageSpaceError(OperationFailedError):
    """Exception raised when operations encounter storage space trouble."""
    default_message = "Unable to %(opname)s (original_exc = %(originalExc)s): insufficient storage space [%(details)s]"


class PermissionDeniedError(OperationFailedError):
    default_message = "Unable to %(opname)s (original_exc = %(originalExc)s): permission denied [%(details)s]"


class FSClosedError(OperationFailedError):
    default_message = "Unable to %(opname)s (original_exc = %(originalExc)s): the FS has been closed [%(details)s]"


class OperationTimeoutError(OperationFailedError):
    default_message = "Unable to %(opname)s (original_exc = %(originalExc)s): operation timed out [%(details)s]"


class RemoveRootError(OperationFailedError):
    default_message = "Can't remove root dir [%(details)s]"


class ResourceError(FSError):
    """Base exception class for error associated with a specific resource."""
    default_message = "Unspecified resource error (original_exc = %(originalExc)s): %(path)s [%(details)s]"

    def __init__(self, path="",details=None **kwds):
        self.path = path
        self.details = details
        self.opname = kwds.pop("opname", None)
        super(ResourceError, self).__init__(**kwds)


class NoSysPathError(ResourceError):
    """Exception raised when there is no syspath for a given path."""
    default_message = "No mapping to OS filesystem (original_exc = %(originalExc)s): %(path)s [%(details)s]"


class NoMetaError(FSError):
    """Exception raised when there is no meta value available."""
    default_message = "No meta value named '%(meta_name)s (original_exc = %(originalExc)s)' could be retrieved [%(details)s]"

    def __init__(self, meta_name, originalExc=None, details=None, msg=None):
        self.meta_name = meta_name
        self.originalExc = originalExc
        self.details = details
        super(NoMetaError, self).__init__(msg)

    def __reduce__(self):
        return (self.__class__, (self.meta_name,), self.__dict__.copy(),)


class NoPathURLError(ResourceError):
    """Exception raised when there is no URL form for a given path."""
    default_message = "No URL form (original_exc = %(originalExc)s): %(path)s [%(details)s]"


class ResourceNotFoundError(ResourceError):
    """Exception raised when a required resource is not found."""
    default_message = "Resource not found (original_exc = %(originalExc)s): %(details)s"


class ResourceInvalidError(ResourceError):
    """Exception raised when a resource is the wrong type."""
    default_message = "Resource is invalid (original_exc = %(originalExc)s): %(path)s [%(details)s]"


class DestinationExistsError(ResourceError):
    """Exception raised when a target destination already exists."""
    default_message = "Destination exists (original_exc = %(originalExc)s): %(path)s [%(details)s]"


class DirectoryNotEmptyError(ResourceError):
    """Exception raised when a directory to be removed is not empty."""
    default_message = "Directory is not empty (original_exc = %(originalExc)s): %(path)s [%(details)s]"


class ParentDirectoryMissingError(ResourceError):
    """Exception raised when a parent directory is missing."""
    default_message = "Parent directory is missing (original_exc = %(originalExc)s): %(path)s [%(details)s]"


class ResourceLockedError(ResourceError):
    """Exception raised when a resource can't be used because it is locked."""
    default_message = "Resource is locked (original_exc = %(originalExc)s): %(path)s [%(details)s]"


class NoMMapError(ResourceError):
    """Exception raise when getmmap fails to create a mmap"""
    default_message = "Can't get mmap for %(path)s (original_exc = %(originalExc)s) [%(details)s]"


class BackReferenceError(ValueError):
    """Exception raised when too many backrefs exist in a path (ex: '/..', '/docs/../..')."""


def convert_fs_errors(func):
    """Function wrapper to convert FSError instances into OSError."""
    @wraps(func)
    def wrapper(*args, **kwds):
        try:
            return func(*args, **kwds)
        except ResourceNotFoundError, e:
            raise OSError(errno.ENOENT, str(e))
        except ParentDirectoryMissingError, e:
            if sys.platform == "win32":
                raise OSError(errno.ESRCH, str(e))
            else:
                raise OSError(errno.ENOENT, str(e))
        except ResourceInvalidError, e:
            raise OSError(errno.EINVAL, str(e))
        except PermissionDeniedError, e:
            raise OSError(errno.EACCES, str(e))
        except ResourceLockedError, e:
            if sys.platform == "win32":
                raise WindowsError(32, str(e))
            else:
                raise OSError(errno.EACCES, str(e))
        except DirectoryNotEmptyError, e:
            raise OSError(errno.ENOTEMPTY, str(e))
        except DestinationExistsError, e:
            raise OSError(errno.EEXIST, str(e))
        except StorageSpaceError, e:
            raise OSError(errno.ENOSPC, str(e))
        except RemoteConnectionError, e:
            raise OSError(errno.ENETDOWN, str(e))
        except UnsupportedError, e:
            raise OSError(errno.ENOSYS, str(e))
        except FSError, e:
            raise OSError(errno.EFAULT, str(e))
    return wrapper


def convert_os_errors(func):
    """Function wrapper to convert OSError/IOError instances into FSError."""
    opname = func.__name__

    @wraps(func)
    def wrapper(self, *args, **kwds):
        try:
            return func(self, *args, **kwds)
        except (OSError, IOError), e:
            (exc_type, exc_inst, tb) = sys.exc_info()
            path = getattr(e, "filename", None)
            originalExc = type(e)
            if path and path[0] == "/" and hasattr(self, "root_path"):
                path = normpath(path)
                if isprefix(self.root_path, path):
                    path = path[len(self.root_path):]
            if not hasattr(e, "errno") or not e.errno:
                raise OperationFailedError(opname, details=e), None, tb
            if e.errno == errno.ENOENT:
                raise ResourceNotFoundError(
                    path, opname=opname, details=e, originalExc=originalExc), None, tb
            if e.errno == errno.EFAULT:
                # This can happen when listdir a directory that is deleted by another thread
                # Best to interpret it as a resource not found
                raise ResourceNotFoundError(
                    path, opname=opname, details=e, originalExc=originalExc), None, tb
            if e.errno == errno.ESRCH:
                raise ResourceNotFoundError(
                    path, opname=opname, details=e, originalExc=originalExc), None, tb
            if e.errno == errno.ENOTEMPTY:
                raise DirectoryNotEmptyError(
                    path, opname=opname, details=e, originalExc=originalExc), None, tb
            if e.errno == errno.EEXIST:
                raise DestinationExistsError(
                    path, opname=opname, details=e, originalExc=originalExc), None, tb
            if e.errno == 183:  # some sort of win32 equivalent to EEXIST
                raise DestinationExistsError(
                    path, opname=opname, details=e, originalExc=originalExc), None, tb
            if e.errno == errno.ENOTDIR:
                raise ResourceInvalidError(
                    path, opname=opname, details=e, originalExc=originalExc), None, tb
            if e.errno == errno.EISDIR:
                raise ResourceInvalidError(
                    path, opname=opname, details=e, originalExc=originalExc), None, tb
            if e.errno == errno.EINVAL:
                raise ResourceInvalidError(
                    path, opname=opname, details=e, originalExc=originalExc), None, tb
            if e.errno == errno.ENOSPC:
                raise StorageSpaceError(
                    opname, path=path, details=e, originalExc=originalExc), None, tb
            if e.errno == errno.EPERM:
                raise PermissionDeniedError(
                    opname, path=path, details=e, originalExc=originalExc), None, tb
            if hasattr(errno, "ENONET") and e.errno == errno.ENONET:
                raise RemoteConnectionError(
                    opname, path=path, details=e, originalExc=originalExc), None, tb
            if e.errno == errno.ENETDOWN:
                raise RemoteConnectionError(
                    opname, path=path, details=e, originalExc=originalExc), None, tb
            if e.errno == errno.ECONNRESET:
                raise RemoteConnectionError(
                    opname, path=path, details=e, originalExc=originalExc), None, tb
            if e.errno == errno.EACCES:
                if sys.platform == "win32":
                    if e.args[0] and e.args[0] == 32:
                        raise ResourceLockedError(
                            path, opname=opname, details=e, originalExc=originalExc), None, tb
                raise PermissionDeniedError(opname, details=e), None, tb
            # Sometimes windows gives some random errors...
            if sys.platform == "win32":
                if e.errno in (13,):
                    raise ResourceInvalidError(
                        path, opname=opname, details=e, originalExc=originalExc), None, tb
            if e.errno == errno.ENAMETOOLONG:
                raise PathError(path, details=e,
                                originalExc=originalExc), None, tb
            if e.errno == errno.EOPNOTSUPP:
                raise UnsupportedError(
                    opname, details=e, originalExc=originalExc), None, tb
            if e.errno == errno.ENOSYS:
                raise UnsupportedError(
                    opname, details=e, originalExc=originalExc), None, tb
            raise OperationFailedError(
                opname, details=e, originalExc=originalExc), None, tb
    return wrapper
