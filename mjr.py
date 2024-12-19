from game import Game


print("Starting simulations...")

num_players = 4
num_simulations = 10_000

results = []
for i in range(num_simulations):
    print(f"Simulating game {i + 1} of {num_simulations}...")
    game = Game(num_players)
    result = game.simulate()
    # for player in result.players:
    #     print(f"Player {player.id} has {player.cash} cash")
    results.append(result)

print("Done!")
print(f"Average turns: {sum(r.num_turns for r in results) / len(results)}")
print(f"Max turns: {max(results, key=lambda r: r.num_turns).num_turns}")
print(f"Min turns: {min(results, key=lambda r: r.num_turns).num_turns}")
print(f"Average turns for games under 20 turns: {sum(r.num_turns for r in results if r.num_turns < 20) / len(results) if len(results) > 0 else 0}")
print(f"Games with turns over 10: {sum(1 for r in results if r.num_turns >= 10) / len(results) * 100:.2f}%")
print(f"Games with turns over 20: {sum(1 for r in results if r.num_turns >= 20) / len(results) * 100:.2f}%")
print(f"Games with turns over 30: {sum(1 for r in results if r.num_turns >= 30) / len(results) * 100:.2f}%")
print(f"Games with turns over 40: {sum(1 for r in results if r.num_turns >= 40) / len(results) * 100:.2f}%")
print(f"Games with turns over 50: {sum(1 for r in results if r.num_turns >= 50) / len(results) * 100:.2f}%")
print(f"Games with turns over 100: {sum(1 for r in results if r.num_turns >= 100) / len(results) * 100:.2f}%")
print(f"Games with no winner: {sum(1 for r in results if r.player_id is None) / len(results) * 100:.2f}%")
print(f"Player 1 wins: {sum(1 for r in results if r.player_id == 0) / len(results) * 100:.2f}%")
print(f"Player 2 wins: {sum(1 for r in results if r.player_id == 1) / len(results) * 100:.2f}%")
print(f"Player 3 wins: {sum(1 for r in results if r.player_id == 2) / len(results) * 100:.2f}%")
print(f"Player 4 wins: {sum(1 for r in results if r.player_id == 3) / len(results) * 100:.2f}%")


# print("Game log:")
# neverending_game = next((r for r in results if r.num_turns < 5), None)
# for log in neverending_game.game_log:
#     print(log)
