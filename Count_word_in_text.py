import urllib.request
from collections import Counter
import time
import matplotlib.pyplot as plt
import numpy as np

# Step 1: get the Shakespearean text
shakespeare_text = "Shakespear_artwork.txt"

# Step 2: Create functions to count word occurrences

# Using a dictionary
def count_words_with_dict(text):
    word_count = {}
    words = text.split()
    for word in words:
        word = word.lower()
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count

# Using Counter
def count_words_with_counter(text):
    words = text.split()
    word_count = Counter(words)
    return word_count

# Step 3: Measure execution times
n_trials = 100
dict_execution_times = []
counter_execution_times = []

for _ in range(n_trials):
    # Using dictionary
    start_time = time.time()
    count_words_with_dict(shakespeare_text)
    dict_execution_times.append(time.time() - start_time)

    # Using Counter
    start_time = time.time()
    count_words_with_counter(shakespeare_text)
    counter_execution_times.append(time.time() - start_time)

# Step 4: Plot the distributions
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.hist(dict_execution_times, bins=20, color='blue', alpha=0.7)
plt.title('Execution Times (Dictionary)')
plt.xlabel('Time (seconds)')
plt.ylabel('Frequency')

plt.subplot(1, 2, 2)
plt.hist(counter_execution_times, bins=20, color='green', alpha=0.7)
plt.title('Execution Times (Counter)')
plt.xlabel('Time (seconds)')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()

# Step 5: Analyze the performance
dict_mean_time = np.mean(dict_execution_times)
counter_mean_time = np.mean(counter_execution_times)
print(f"Mean execution time (Dictionary): {dict_mean_time:.6f} seconds")
print(f"Mean execution time (Counter): {counter_mean_time:.6f} seconds")
