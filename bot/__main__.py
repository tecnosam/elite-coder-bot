from bot import client, TOKEN
import signal

signal.signal(signal.SIGTERM, lambda *_: client.loop.create_task(client.close()))

client.run(TOKEN)
