# Port Scanner

A simple port scanner written in Python.

## Usage

1. Clone the repository:

    ```shell
    git clone https://github.com/your-username/port-scanner.git
    ```

2. Navigate to the project directory:

    ```shell
    cd port-scanner
    ```

3. Install the required dependencies:

    ```shell
    pip install -r requirements.txt
    ```

4. Run the port scanner:

    ```shell
    python port_scanner.py <host> [-p PORTS] [-u] [-t]
    ```

    - `<host>`: The host to scan.
    - `-p PORTS`, `--ports PORTS`: Range of ports to scan (e.g., `1-100`).
    - `-u`, `--udp`: Perform UDP scan.
    - `-t`, `--tcp`: Perform TCP scan.

5. Example usage:

    ```shell
    python port_scanner.py example.com -p 1-100 -t
    ```

## Warning
do not use this with bad idea in mind