import sys, os, time
from requests import session
from core.google_api.google_sheet_handler import GoogleSheetHandler
import docker
gg_sheet_handler = GoogleSheetHandler("GROUPS_MANAGER")
request = session()
cookies_spreadsheet_name = "FB Cookies"
cookies = gg_sheet_handler.read_all(cookies_spreadsheet_name)
fb_users = [x for x in cookies[0] if x.strip()]
print("--args: version - example: v1.0.0")
"""sudo docker run -itd --name test --network bridge tnetwork96/marketing_service_rpi_armv7:{1} ./script.sh {2}"""
docker_run_command = "sudo docker run -itd --name {0} -v $(pwd):/home/marketing-bot --network bridge tnetwork96/marketing_service_rpi_armv7:{1} ./script.sh {2} "
client = docker.from_env()
client_list = client.containers.list(all=True)
container_names = [cli.name for cli in client_list
    if cli.status == "exited" and \
            "service" not in cli.name]
for fb_user in fb_users:
    print("fb_user: ", fb_user)
    if fb_user in container_names:
        continue
    os.system(docker_run_command.format(fb_user, sys.argv[1].strip(), fb_user))
    time.sleep(2)