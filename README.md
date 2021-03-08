# Red Canary Telemetry Tester

This tool performs some activity on an endpoint and prints out some information about the activity it performed. This can be used to test a telemetry analyzer such as the EDR agent from Red Canary. When changes are made to Red Canary's EDR solution, this tool can detect whether the EDR is still collecting all of the same data by comparing the output of this tool to the EDR logs.

## Usage
To use the tool, provide a JSON configuration file as a commandline argument, like so:

```bash
python telemetry_tester.py sample-config.json
```

See [sample-config.json](sample-config.json) for an example of what the configuration file should look like.

### Configuration Options

| Key               | Value                                                                                              |
| :---------------- | :------------------------------------------------------------------------------------------------- |
|  command          | List of strings. First string should be an executable, the rest are optional commandline arguments |
|  file             | Object. Subvalues are all optional                                                                 |
|  file["name"]     | String. Whatever the file should be named. Default: "test"                                         |
|  file["type"]     | String. The file extension. Default: "csv"                                                         |
|  file["location"] | String. The directory to create the file in. Default: current working directory                    |

The "command" and "file" entries are required. The name, type, and location of the file are optional (defaults in above table).

### Under the hood

The tool first validates the provided configuration file. If it is invalid, it will print to stderr a helpful error message. Next, it will run the executable specified in the "command" of the configuration JSON file. After that, it will create a file (using the name, type and location specified in the configuration file). Then it will modify the file by appending a line of text to it, and finally delete the file. Lastly, it will open a TCP socket and send some HTTP data over it and receive the response from the remote server (though it does not log the response). After that, it will print to stdout the log of the activity it generated, complete with timestamps and process IDs.

Example log output:

```json
{
    "file": {
        "create": {
            "command_line": "telemetry_tester.py sample-config.json",
            "path": "./test.csv",
            "process_id": 10427,
            "process_name": "telemetry_tester.py",
            "time_stamp": "2021-03-07T18:57:42.043628",
            "username": "aaronsuarez"
        },
        "delete": {
            "command_line": "telemetry_tester.py sample-config.json",
            "path": "./test.csv",
            "process_id": 10427,
            "process_name": "telemetry_tester.py",
            "time_stamp": "2021-03-07T18:57:42.044231",
            "username": "aaronsuarez"
        },
        "modify": {
            "command_line": "telemetry_tester.py sample-config.json",
            "path": "./test.csv",
            "process_id": 10427,
            "process_name": "telemetry_tester.py",
            "time_stamp": "2021-03-07T18:57:42.044040",
            "username": "aaronsuarez"
        }
    },
    "network": {
        "command_line": "telemetry_tester.py sample-config.json",
        "data_protocol": "TCP",
        "data_size": 43,
        "destination_address": "54.91.118.50",
        "destination_port": 80,
        "process_id": 10427,
        "process_name": "telemetry_tester.py",
        "source_address": "127.0.0.1",
        "source_port": 31415,
        "time_stamp": "2021-03-07T18:57:42.309478",
        "username": "aaronsuarez"
    },
    "process": {
        "command_line": "echo hello telemetry tester",
        "process_id": 10443,
        "process_name": "echo",
        "time_stamp": "2021-03-07T18:57:42.036913",
        "username": "aaronsuarez"
    }
}
```

## Future Possibilities

Right now, there are no configuration options for the network connection. It would be nice to let the user specify the remote server to connect to, the data to send, the source port, etc.

Also, when the file is modified, it is always modified by adding the same string. It would be nice to let the user specify that as well.

Note: Windows is not supported in its current form. The `subprocess` module doesn't work with the current syntax, and `pwd` is not available on Windows. With some slight modifications, it can be made to run on Windows, but does not currently.

