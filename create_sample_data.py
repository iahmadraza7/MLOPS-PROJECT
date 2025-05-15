import pandas as pd
import os

# Create sample cricket data
if not os.path.exists('data/raw/ODI_Cricket_Data.csv'):
    # Create sample data
    df = pd.DataFrame({
        'player_name': ['Virat Kohli', 'Rohit Sharma', 'Kane Williamson', 'Joe Root', 'Babar Azam'],
        'role': ['Batsman', 'Batsman', 'Batsman', 'Batsman', 'Batsman'],
        'total_runs': [12169, 9283, 6173, 6190, 5005],
        'strike_rate': [93.3, 89.5, 81.8, 86.9, 88.2],
        'total_balls_faced': [13055, 10372, 7547, 7124, 5677],
        'total_matches_played': [254, 227, 151, 152, 97],
        'matches_won': [155, 135, 95, 93, 58],
        'matches_lost': [85, 82, 50, 55, 35]
    })
    
    # Save to CSV
    df.to_csv('data/raw/ODI_Cricket_Data.csv', index=False)
    print('Created sample cricket data')
else:
    print('Sample cricket data already exists') 