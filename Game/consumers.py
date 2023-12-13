import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_code = self.scope['url_route']['kwargs']['game_code']
        self.game_group_name = f"game_{self.game_code}"

        # Join room group
        await self.channel_layer.group_add(
            self.game_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.game_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        move_data = text_data_json.get('move_data', None)

        if move_data:
            row = move_data.get('row', None)
            col = move_data.get('col', None)
            symbol = move_data.get('symbol', None)

            if row is not None and col is not None and symbol is not None:
                # Mettez à jour l'état du jeu avec le mouvement du joueur
                self.game_state[row][col] = symbol

                # Vérifiez s'il y a une victoire ou un match nul
                if self.check_win() or self.check_draw():
                    # Envoyez un message à tous les joueurs indiquant la fin du jeu
                    await self.channel_layer.group_send(
                        self.game_group_name,
                        {
                            'type': 'game_over',
                            'message': 'Le jeu est terminé!'
                        }
                    )
                else:
                    # Sinon, informez tous les joueurs du nouveau mouvement
                    await self.channel_layer.group_send(
                        self.game_group_name,
                        {
                            'type': 'game_message',
                            'message': f"Le joueur {self.get_player_name()} a joué à la case ({row}, {col})."
                        }
                    )

    # Receive message from room group
    async def game_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
def get_player_name(self):
    # Logique pour obtenir le nom du joueur actuel (à adapter en fonction de votre jeu)
    return 'Player 1' if self.current_player == 0 else 'Player 2'