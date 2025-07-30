<<<<<<< HEAD
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from scipy.sparse import hstack

# Load dataset
df = pd.read_csv("career_data.csv")

# Vectorize interest text
vectorizer = TfidfVectorizer()
X_text = vectorizer.fit_transform(df['interest_text'])

# Combine with numeric features
X_other = df[['math', 'science', 'art']]
X = hstack((X_text, X_other.values))

# Target
y = df['career']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Predict sample input
sample_text = "I love solving problems and building software"
sample_vector = vectorizer.transform([sample_text])
sample_combined = hstack((sample_vector, [[1, 1, 0]]))  # Math=1, Science=1, Art=0

prediction = model.predict(sample_combined)
print("Suggested Career:", prediction[0])
print(data.columns)


=======
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from scipy.sparse import hstack

# Load dataset
df = pd.read_csv("career_data.csv")

# Vectorize interest text
vectorizer = TfidfVectorizer()
X_text = vectorizer.fit_transform(df['interest_text'])

# Combine with numeric features
X_other = df[['math', 'science', 'art']]
X = hstack((X_text, X_other.values))

# Target
y = df['career']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Predict sample input
sample_text = "I love solving problems and building software"
sample_vector = vectorizer.transform([sample_text])
sample_combined = hstack((sample_vector, [[1, 1, 0]]))  # Math=1, Science=1, Art=0

prediction = model.predict(sample_combined)
print("Suggested Career:", prediction[0])
print(data.columns)


>>>>>>> 160a65b (new update)
 