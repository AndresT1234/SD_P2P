# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: catalog.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'catalog.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rcatalog.proto\x12\x07\x63\x61talog\"#\n\x0f\x44ownloadRequest\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\"#\n\x10\x44ownloadResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2J\n\x07\x43\x61talog\x12?\n\x08\x44ownload\x12\x18.catalog.DownloadRequest\x1a\x19.catalog.DownloadResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'catalog_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_DOWNLOADREQUEST']._serialized_start=26
  _globals['_DOWNLOADREQUEST']._serialized_end=61
  _globals['_DOWNLOADRESPONSE']._serialized_start=63
  _globals['_DOWNLOADRESPONSE']._serialized_end=98
  _globals['_CATALOG']._serialized_start=100
  _globals['_CATALOG']._serialized_end=174
# @@protoc_insertion_point(module_scope)
