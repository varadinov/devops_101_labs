# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: demo.proto
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
    'demo.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ndemo.proto\x12\x04\x64\x65mo\"\x07\n\x05\x45mpty\"$\n\x0cTimeResponse\x12\x14\n\x0c\x63urrent_time\x18\x01 \x01(\t\"\x1e\n\x0b\x45\x63hoRequest\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x1f\n\x0c\x45\x63hoResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2o\n\x0b\x44\x65moService\x12*\n\x07GetTime\x12\x0b.demo.Empty\x1a\x12.demo.TimeResponse\x12\x34\n\x0b\x45\x63hoMessage\x12\x11.demo.EchoRequest\x1a\x12.demo.EchoResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'demo_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_EMPTY']._serialized_start=20
  _globals['_EMPTY']._serialized_end=27
  _globals['_TIMERESPONSE']._serialized_start=29
  _globals['_TIMERESPONSE']._serialized_end=65
  _globals['_ECHOREQUEST']._serialized_start=67
  _globals['_ECHOREQUEST']._serialized_end=97
  _globals['_ECHORESPONSE']._serialized_start=99
  _globals['_ECHORESPONSE']._serialized_end=130
  _globals['_DEMOSERVICE']._serialized_start=132
  _globals['_DEMOSERVICE']._serialized_end=243
# @@protoc_insertion_point(module_scope)
