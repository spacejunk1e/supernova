# Leaderboard and Mock Data functions
def generate_leaderboard(users, timeframe='daily'):
    for user in users:
        user.update_score()

    sorted_users = sorted(users, key=lambda u: u.total_score, reverse=True)
    for rank, user in enumerate(sorted_users, 1):
        print(f"{rank}. {user.username} - {user.total_score} points")
