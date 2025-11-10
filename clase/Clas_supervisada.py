from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
# 1. Cargar dataset real (flores Iris)
iris = load_iris()
X, y = iris.data, iris.target
# 2. Separar en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
# 3. Entrenar modelo supervisado (KNN)
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, y_train)
# 4. Evaluar
y_pred = model.predict(X_test)
print("Exactitud del modelo:", accuracy_score(y_test, y_pred))
# 5. Predicción con nuevos datos
nueva_flor = [[5.1, 3.5, 1.4, 0.2]]
print("Predicción para la flor nueva:", iris.target_names[model.predict(nueva_flor)][0])