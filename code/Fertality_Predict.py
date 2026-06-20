import numpy as np
import pandas as pd 
import joblib 

import warnings 
warnings.filterwarnings('ignore')

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold, train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer 
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, accuracy_score, f1_score, roc_auc_score, roc_curve

from xgboost import XGBClassifier  # type: ignore

# Load datasheet 
df = pd.read_csv('datasheet/Fertility_Health_Dataset_2026.csv', keep_default_na=False, na_values=['',])

# hapus kolom Couple_ID karena tidak relevan untuk analisis
df = df.drop(columns=['Couple_ID'], axis=1)

# pisahkan fitur dan target
X = df.iloc[:, :-1] # Fitur 
y = df.iloc[:, -1]  # Target (Pregnancy Outcome)

# pisahkan fitur numerikal dan kategorikal
NUM_FEATURES = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
CAT_FEATURES = X.select_dtypes(include=['object']).columns.tolist()

# preprocessing target variabel dengan label encoder 
le = LabelEncoder()
y = le.fit_transform(y)

# bagi datasheet menjadi data latih dan data uji 
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=4, stratify=y)

# buat pipeline untuk preprocessing data 
pre = ColumnTransformer(
    [
        ('num', StandardScaler(), NUM_FEATURES),
        ('cat', OneHotEncoder(handle_unknown='ignore'), CAT_FEATURES)
    ]
)

# setting hyperparameter untuk mode 
cv = StratifiedKFold(
    n_splits=5, shuffle=True, random_state=42
)

# kandidat model yang akan digunakan 
candidates = {
    "LogisticRegression": {
        "estimator": LogisticRegression(max_iter=2000, class_weight="balanced", random_state=42),
        "param_grid": {
            "model__C":       [0.01, 0.1, 1, 10, 100],
            "model__penalty": ["l2"],
            "model__solver":  ["lbfgs"],
        },
    },
    "RandomForest": {
        "estimator": RandomForestClassifier(class_weight="balanced", random_state=42),
        "param_grid": {
            "model__n_estimators":   [100, 200],
            "model__max_depth":      [4, 6, 8, None],
            "model__min_samples_leaf": [1, 2, 4],
        },
    },
    "GradientBoosting": {
        "estimator": GradientBoostingClassifier(random_state=42),
        "param_grid": {
            "model__n_estimators":  [100, 200],
            "model__learning_rate": [0.01, 0.05, 0.1],
            "model__max_depth":     [2, 3, 4],
        },
    },
    "XGBoost": {
        "estimator": XGBClassifier(eval_metric="logloss", random_state=42),
        "param_grid": {
            "model__n_estimators":  [100, 200],
            "model__learning_rate": [0.05, 0.1],
            "model__max_depth":     [3, 5],
            "model__subsample":     [0.8, 1.0],
        },
    },
}

# jalankan hyperparameter tuning untuk setiap kandidat model
results = {}

for name, cfg in candidates.items():
    print(f"\n{'='*50}\nTuning: {name}\n{'='*50}")
    pipe = Pipeline([("pre",pre), ("model", cfg["estimator"])])
    
    grid_search = GridSearchCV(
        pipe, cfg["param_grid"],
        cv=cv, scoring="f1",
        n_jobs=-1, verbose=0,
    )
    grid_search.fit(X_train, y_train)

    y_pred = grid_search.best_estimator_.predict(X_test)
    y_proba = grid_search.best_estimator_.predict_proba(X_test)[:, 1]

    results[name] = {
        "best_estimator": grid_search.best_estimator_,
        "best_params":    grid_search.best_params_,
        "cv_f1":          grid_search.best_score_,
        "test_f1":        f1_score(y_test, y_pred),
        "test_f1_macro":  f1_score(y_test, y_pred, average="macro"),
        "roc_auc":        roc_auc_score(y_test, y_proba),          # ← tambahan
    }

    print(f"  CV F1        : {grid_search.best_score_:.4f}")
    print(f"  Test F1      : {f1_score(y_test, y_pred):.4f}")
    print(f"  Test F1 Macro: {f1_score(y_test, y_pred, average='macro'):.4f}")
    print(f"  ROC-AUC      : {roc_auc_score(y_test, y_proba):.4f}")   # ← tambahan
    print(classification_report(y_test, y_pred, target_names=["Failure", "Success"]))

print("\n\nHasil Hyperparameter Tuning:\n")

for name, res in results.items():
    print(f"{name}:")
    print(f"  Best Parameters: {res['best_params']}")
    print(f"  CV F1 Score: {res['cv_f1']:.4f}")
    print(f"  Test F1 Score: {res['test_f1']:.4f}")
    print(f"  Test F1 Macro Score: {res['test_f1_macro']:.4f}")
    print(f"  ROC AUC Score: {res['roc_auc']:.4f}\n")

# simpan preprocessing dan model terbaik ke dalam file untuk digunakan pada tahap selanjutnya 
best_model_name = max(results, key=lambda x: results[x]['test_f1'])
best_model = results[best_model_name]['best_estimator']

# simpan standard scaler dan one hot encoder ke dalam file 'preprocessor.pkl'
joblib.dump(pre, 'preprocessor.pkl')
print(f"Preprocessor telah disimpan sebagai 'preprocessor.pkl'")

# simpan label encoder
joblib.dump(le, 'label_encoder.pkl')
print(f"Label encoder telah disimpan sebagai 'label_encoder.pkl'")

# simpan model terbaik ke dalam file 'best_model.pkl'
joblib.dump(best_model, 'best_model.pkl')
print(f"Best_model '{best_model_name}' telah disimpan sebagai 'best_model.pkl'")
