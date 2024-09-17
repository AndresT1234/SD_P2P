# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from . import peer_pb2 as peer__pb2

GRPC_GENERATED_VERSION = '1.66.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in peer_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class PeerServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.UploadFile = channel.unary_unary(
                '/PeerService/UploadFile',
                request_serializer=peer__pb2.FileRequest.SerializeToString,
                response_deserializer=peer__pb2.FileResponse.FromString,
                _registered_method=True)
        self.DownloadFile = channel.unary_stream(
                '/PeerService/DownloadFile',
                request_serializer=peer__pb2.FileRequest.SerializeToString,
                response_deserializer=peer__pb2.FileChunk.FromString,
                _registered_method=True)


class PeerServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def UploadFile(self, request, context):
        """Cargar archivo
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DownloadFile(self, request, context):
        """Descargar un archivo en chunks de datos
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PeerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'UploadFile': grpc.unary_unary_rpc_method_handler(
                    servicer.UploadFile,
                    request_deserializer=peer__pb2.FileRequest.FromString,
                    response_serializer=peer__pb2.FileResponse.SerializeToString,
            ),
            'DownloadFile': grpc.unary_stream_rpc_method_handler(
                    servicer.DownloadFile,
                    request_deserializer=peer__pb2.FileRequest.FromString,
                    response_serializer=peer__pb2.FileChunk.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'PeerService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('PeerService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class PeerService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def UploadFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/PeerService/UploadFile',
            peer__pb2.FileRequest.SerializeToString,
            peer__pb2.FileResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DownloadFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/PeerService/DownloadFile',
            peer__pb2.FileRequest.SerializeToString,
            peer__pb2.FileChunk.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
