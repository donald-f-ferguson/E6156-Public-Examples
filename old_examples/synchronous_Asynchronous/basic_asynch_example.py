#
# This is the simplest possible example of showing asynch behavior with
# coroutines.
#
import asyncio


async def call_one(sleep_time):
    """
    A simple function that sleeps, yielding the coroutine control and
    resuming after sleeping.

    :return:
    """
    print("call_one entry. Sleeping for ", sleep_time, "seconds.")
    await asyncio.sleep(sleep_time)
    print("call_one exit.")


async def call_two(sleep_time):
    print("call_two entry. Sleeping for ", sleep_time, "seconds.")
    await asyncio.sleep(sleep_time)
    print("call_two exit.")


async def do_it():
    result = await asyncio.gather(
        call_one(5),
        call_two(2)
    )


if __name__ == "__main__":
    asyncio.run(do_it())