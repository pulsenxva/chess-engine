import chess
import chess.svg
from flask import Flask, request, redirect, url_for
from engine import minimax

app = Flask(__name__)
board = chess.Board()
last_move = None
error = ""

@app.route("/")
def index():
  svg = chess.svg.board(
    board,
    lastmove=last_move,
    check=board.king(board.turn) if board.is_check() else None,
    size=480,
  )
  html = f"""
  <!DOCTYPE html>
  <html>
  <body>
    {svg}
    <form method="POST" action="/move">
        <input name="move" placeholder="e2e4" autofocus>
        <button>move</button>
    </form>
    <p>{error}</p>
  </body>
  </html>
  """
  return html

@app.route("/move", methods=["POST"])
def move():
  global last_move, error
  uci = request.form.get("move", "").strip()
  try:
    mv = chess.Move.from_uci(uci)
    if mv in board.legal_moves:
      board.push(mv)
      last_move = mv
      error = ""
      if not board.is_game_over():
        bestMove, bestScore = minimax(board, 0, -1000000, 1000000)
        if bestMove:
          board.push(bestMove)
          last_move = bestMove
    else:
      error = f"error: {uci}"
  except chess.InvalidMoveError:
    error = f"error: {uci}"
  return redirect(url_for("index"))

if __name__ == "__main__":
  app.run(port=5000)

