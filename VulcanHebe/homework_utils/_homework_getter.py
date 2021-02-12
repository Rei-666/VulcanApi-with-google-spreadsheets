import datetime


class HomeworkGetter:
    def __init__(self, client):
        self._client = client

    async def get_homework_list(self, sync_date=None):
        if not sync_date:
            sync_date = datetime.datetime.now() - datetime.timedelta(weeks=1)
        homeworks_iterator = await self._client.data.get_homework(last_sync=sync_date)
        return [homework async for homework in homeworks_iterator]
