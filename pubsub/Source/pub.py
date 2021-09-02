#!/usr/bin/env python

# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import glob
import json
from google.cloud import pubsub_v1
import os


def pub(project_id: str, topic_id: str) -> None:
    """Publishes a message to a Pub/Sub topic."""
    # Initialize a Publisher client.
    client = pubsub_v1.PublisherClient()
    # Create a fully qualified identifier of form `projects/{project_id}/topics/{topic_id}`
    topic_path = client.topic_path(project_id, topic_id)

    path = os.path.dirname(os.path.realpath(__file__)) + '/../weatherfiles/*.json'
    # Data sent to Cloud Pub/Sub must be a bytestring.
    while True:
        for file in glob.glob(path):            
            with open(file) as json_file:
                data = json.load(json_file)
            # When you publish a message, the client returns a future.
            api_future = client.publish(topic_path, str.encode(str(data)))
            message_id = api_future.result()

            print(f"Published {data} to {topic_path}: {message_id}")
            os.remove(file)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="Google Cloud project ID")
    parser.add_argument("topic_id", help="Pub/Sub topic ID")

    args = parser.parse_args()

    pub(args.project_id, args.topic_id)
