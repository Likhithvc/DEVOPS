import docker

# Connect to Docker Desktop
client = docker.from_env()

# Get the running secured container
container = client.containers.get("flask-apparmor-secure")

print(f"Container: {container.name}")
print(f"Status: {container.status}")

tests = [
    (
        "Write to read-only /app",
        [
            "sh",
            "-c",
            "echo test > /app/sdk-security-test.txt"
        ]
    ),
    (
        "Execute a script from noexec /tmp",
        [
            "sh",
            "-c",
            "printf '#!/bin/sh\\necho executed\\n' > /tmp/sdk-noexec-test.sh"
            " && chmod +x /tmp/sdk-noexec-test.sh"
            " && /tmp/sdk-noexec-test.sh"
        ]
    )
]

for description, command in tests:
    result = container.exec_run(command)

    print(f"\nTest: {description}")
    print(f"Exit code: {result.exit_code}")

    output = result.output.decode("utf-8", errors="replace").strip()
    print(f"Output: {output or '(no output)'}")

    if result.exit_code != 0:
        print("Result: RESTRICTION CONFIRMED")
    else:
        print("Result: RESTRICTION NOT CONFIRMED")