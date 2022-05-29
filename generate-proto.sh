#!/bin/bash

protoc --proto_path=proto --python_out=build/gen proto/bakdata/corporate/v1/corporate.proto
protoc --proto_path=proto --python_out=build/gen proto/bakdata/stock/v1/stock.proto
#protoc --proto_path=proto --python_out=build/gen proto/bakdata/corporate_role/v1/corporate_role.proto
protoc --proto_path=proto --python_out=build/gen proto/bakdata/corporate_updates/v1/corporate_updates.proto
#protoc --proto_path=proto --python_out=build/gen proto/bakdata/person/v1/person.proto
