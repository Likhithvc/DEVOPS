import docker

client = docker.from_env()

container = client.containers.get("flask-apparmor-secure")
container.reload()

info = container.attrs
host_config = info["HostConfig"]

print("Container:", container.name)
print("Status:", info["State"]["Status"])
print("Image:", info["Config"]["Image"])
print("User:", info["Config"].get("User"))

print("\nSecurity settings:")
print("Read-only root filesystem:", host_config.get("ReadonlyRootfs"))
print("Dropped capabilities:", host_config.get("CapDrop"))
print("Security options:", host_config.get("SecurityOpt"))
print("Temporary filesystem:", host_config.get("Tmpfs"))

print("\nSecurity configuration inspection completed.")