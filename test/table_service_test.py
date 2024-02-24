import asyncio

import globle
from service.table_service import delete_table_id, get_table_id, update_table_id

if __name__ == '__main__':
    # test_tts_single()
    # test_tts_multi()
    # run_video_editor_test()
    if globle.db is None:
        print("Can not init databases from configuration!")
        exit()
    else:
        # Create an event loop
        loop = asyncio.get_event_loop()

        # Run the async function in the event loop
        loop.run_until_complete(get_table_id(table_name="lecture"))
        loop.run_until_complete(update_table_id(table_name="com_user"))
        loop.run_until_complete(delete_table_id(table_name="com_user"))
        # Close the loop
        loop.close()