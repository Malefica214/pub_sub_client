#import asyncio
#from fastapi import WebSocket
#from notification import collection
#
#async def websocket_notifiche(websocket: WebSocket, addressee_id: str):
#    await websocket.accept()
#    pipeline = [{"$match": {"fullDocument.addressee_id": addressee_id}}]
#    async for change in collection.watch(pipeline=pipeline):
#        new_notification = change["fullDocument"]
#        await websocket.send_json( {'id': str(new_notification["_id"]),
#                'addressee_id': new_notification["addressee_id"],
#                'sender_id': new_notification["sender_id"],
#                'type': new_notification.get("type"),
#                'message': new_notification["message"],
#                'state': new_notification["state"],
#                'created_at': new_notification["created_at"]})