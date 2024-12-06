import pandas as pd

def split_genres_into_columns(input_file, output_file):
    """
    Read the input CSV file, split the genres into individual columns, and save the result to a new CSV file.
    
    Args:
        input_file (str): Path to the input CSV file with artist and genres.
        output_file (str): Path to the output CSV file.
    """
    # Read the input CSV file
    df = pd.read_csv(input_file)
    
    # Split the genres string into a list for each row
    df['genres'] = df['genres'].str.split(', ')
    
    # Explode the genres list into separate rows
    df = df.explode('genres')
    
    # Pivot the data to create columns for each genre
    df = df.pivot(index='artist', columns='genres', values='genres').fillna('')
    
    # Save the output to a new CSV file
    df.to_csv(output_file, index=True)

# Example usage
split_genres_into_columns('artists_genres.csv', 'artists_with_genres.csv')
print("Genre data split and saved to artists_with_genres.csv")