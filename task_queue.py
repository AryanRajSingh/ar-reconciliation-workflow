import asyncio

queue = asyncio.Queue()


async def worker():

    while True:

        customer_id = await queue.get()

        try:

            from workflow import run_workflow

            await run_workflow(customer_id)

        except Exception as e:

            print(
                f"Worker error: {e}"
            )

        finally:

            queue.task_done()



async def start_workers():

    # start 3 parallel workers

    workers=[]

    for _ in range(3):

        workers.append(

            asyncio.create_task(
                worker()
            )
        )

    return workers