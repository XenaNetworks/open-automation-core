from __future__ import annotations
from xoa_core import (
    controller,
    types,
)
from pathlib import Path
import asyncio
import json

BASE_PATH = Path.cwd()
PLUGINS_PATH = BASE_PATH / "plugins"
TEST_CONFIG_PATH = BASE_PATH / "my2544_data.json"


async def listen_messages(ctrl: controller.MainController, identifier: str, filter: set[types.EMsgType] | None = None) -> None:
    async for msg in ctrl.listen_changes(identifier, _filter=filter):
        print(msg)


async def main() -> None:
    # Create a default instance of the controller class.
    my_controller = await controller.MainController()

    # Register the plugins folder.
    my_controller.register_lib(str(PLUGINS_PATH))

    # Define your tester login credentials
    my_tester_credential = types.Credentials(
        product=types.EProductType.VALKYRIE,
        host="10.20.30.40",
        password="xena"
    )

    # Subscribe to all message from test resources.
    asyncio.create_task(listen_messages(my_controller, types.PIPE_RESOURCES))

    # Add tester credentials into teh controller. If already added, it will be ignored.
    # If you want to add a list of testers, you need to iterate through the list.
    await my_controller.add_tester(my_tester_credential)

    # Get currently available test suites names
    print(my_controller.get_available_test_suites())

    # Load your test configuration data into the test suite and run.
    with open(TEST_CONFIG_PATH, "r") as f:
        data = json.load(f)

    # Test suite name: "RFC-2544" is received from call of my_controller.get_available_test_suites()
    execution_id = my_controller.start_test_suite("RFC-2544", data)

    # Subscribe to statistic messages.
    await listen_messages(my_controller, execution_id, {types.EMsgType.STATISTICS})


if __name__ == "__main__":
    asyncio.run(main())
