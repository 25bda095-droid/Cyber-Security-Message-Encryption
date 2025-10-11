import reflex as rx
import pandas as pd
import numpy as np
import joblib
import PyPDF2
import re
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

# ---- MODEL LOADING ----
MODELPATH = 'fraud_detection_model_tuned.pkl'
SCALERPATH = 'scaler.pkl'
RANDOMFORESTPATH = 'random_Forest_model.pkl'
XGBOOSTPATH = 'XGBoost_model.joblib'

try:
    tunedmodel = joblib.load(MODELPATH)
    scaler = joblib.load(SCALERPATH)
    rfmodel = joblib.load(RANDOMFORESTPATH)
    xgbmodel = joblib.load(XGBOOSTPATH)
except Exception as e:
    print(f"Error loading models: {e}")

# ---- HELPER FUNCTIONS ----
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['csv', 'pdf']

def extract_csv_from_pdf(pdf_content):
    try:
        pdf_file = io.BytesIO(pdf_content)
        pdfreader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in pdfreader.pages:
            text += page.extract_text()
        lines = text.strip().split('\n')
        data = []
        for line in lines:
            row = re.split(r',\s*', line.strip())
            if len(row) > 1:
                data.append(row)
        if data:
            df = pd.DataFrame(data[1:], columns=data[0])
            return df
        return None
    except Exception as e:
        return None

def preprocess_data(df):
    try:
        required_cols = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            if 'Time' in missing_cols:
                required_cols = [f'V{i}' for i in range(1, 29)] + ['Amount']
                missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                return None, f"Missing columns: {', '.join(missing_cols)}"
        
        for col in required_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df = df.dropna(subset=required_cols)
        
        if len(df) == 0:
            return None, "No valid data after cleaning"
        
        X = df[required_cols].copy()
        X_scaled = scaler.transform(X)
        return X_scaled, None
    except Exception as e:
        return None, f"Preprocessing error: {str(e)}"

def predict_fraud(X_scaled, model_choice):
    try:
        if model_choice == "tuned":
            model = tunedmodel
        elif model_choice == "rf":
            model = rfmodel
        elif model_choice == "xgb":
            model = xgbmodel
        
        predictions = model.predict(X_scaled)
        probabilities = model.predict_proba(X_scaled)[:, 1]
        return predictions, probabilities
    except Exception as e:
        return None, None

def generate_pie_charts(pred_tuned, pred_rf, pred_xgb, total):
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    fig.patch.set_facecolor('#f8f9fa')
    
    models_data = [
        ('Tuned Model', int(np.sum(pred_tuned)), total - int(np.sum(pred_tuned))),
        ('Random Forest', int(np.sum(pred_rf)), total - int(np.sum(pred_rf))),
        ('XGBoost', int(np.sum(pred_xgb)), total - int(np.sum(pred_xgb)))
    ]
    
    for idx, (name, fraud, legit) in enumerate(models_data):
        axes[idx].pie([fraud, legit], labels=['Fraudulent', 'Legitimate'],
                     autopct='%1.1f%%', colors=['#fc5c7d', '#6a82fb'],
                     startangle=90, textprops={'fontweight':'bold'})
        axes[idx].set_title(name, fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode()
    plt.close()
    return f"data:image/png;base64,{img_str}"

def generate_histogram(prob_tuned, prob_rf, prob_xgb):
    fig, ax = plt.subplots(figsize=(12, 5))
    fig.patch.set_facecolor('#f8f9fa')
    
    ax.hist(prob_tuned, bins=25, alpha=0.6, label='Tuned Model', color='#fc5c7d', edgecolor='black')
    ax.hist(prob_rf, bins=25, alpha=0.6, label='Random Forest', color='#6a82fb', edgecolor='black')
    ax.hist(prob_xgb, bins=25, alpha=0.6, label='XGBoost', color='#ffb800', edgecolor='black')
    
    ax.set_xlabel('Fraud Probability', fontsize=11, fontweight='bold')
    ax.set_ylabel('Count', fontsize=11, fontweight='bold')
    ax.set_title('Probability Distribution Comparison', fontsize=12, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode()
    plt.close()
    return f"data:image/png;base64,{img_str}"

# ---- REFLEX STATE ----
class FraudDetectionState(rx.State):
    file_content: str = ""
    file_name: str = ""
    analysis_complete: bool = False
    
    total_transactions: int = 0
    tuned_fraud: int = 0
    rf_fraud: int = 0
    xgb_fraud: int = 0
    
    fraud_3_count: int = 0
    fraud_2_count: int = 0
    fraud_1_count: int = 0
    
    pie_chart_img: str = ""
    histogram_img: str = ""
    
    fraud_3_data: list = []
    fraud_2_data: list = []
    fraud_1_data: list = []
    
    error_message: str = ""
    success_message: str = ""
    
    async def handle_file_upload(self, files: list[rx.upload.FileInfo]):
        try:
            for file in files:
                self.file_name = file.filename
                if file.filename.endswith('.csv'):
                    df = pd.read_csv(file.filepath)
                elif file.filename.endswith('.pdf'):
                    with open(file.filepath, 'rb') as f:
                        df = extract_csv_from_pdf(f.read())
                else:
                    self.error_message = "Invalid file format. Use CSV or PDF."
                    return
                
                X_scaled, error = preprocess_data(df)
                if error:
                    self.error_message = error
                    return
                
                pred_tuned, prob_tuned = predict_fraud(X_scaled, "tuned")
                pred_rf, prob_rf = predict_fraud(X_scaled, "rf")
                pred_xgb, prob_xgb = predict_fraud(X_scaled, "xgb")
                
                if pred_tuned is None:
                    self.error_message = "Prediction failed"
                    return
                
                self.total_transactions = len(pred_tuned)
                self.tuned_fraud = int(np.sum(pred_tuned))
                self.rf_fraud = int(np.sum(pred_rf))
                self.xgb_fraud = int(np.sum(pred_xgb))
                
                # Generate charts
                self.pie_chart_img = generate_pie_charts(pred_tuned, pred_rf, pred_xgb, self.total_transactions)
                self.histogram_img = generate_histogram(prob_tuned, prob_rf, prob_xgb)
                
                # Calculate consensus
                models_count = (pred_tuned.astype(int) + pred_rf.astype(int) + pred_xgb.astype(int))
                
                self.fraud_3_count = len(np.where(models_count == 3)[0])
                self.fraud_2_count = len(np.where(models_count == 2)[0])
                self.fraud_1_count = len(np.where(models_count == 1)[0])
                
                self.analysis_complete = True
                self.success_message = f"Analysis complete! Processed {self.total_transactions} transactions."
                self.error_message = ""
                
        except Exception as e:
            self.error_message = f"Error: {str(e)}"

# ---- REFLEX COMPONENTS ----
def header():
    return rx.box(
        rx.vstack(
            rx.heading(
                "Fraud Detection System",
                size="xl",
                text_align="center",
                color="#232946",
                font_weight="800",
            ),
            rx.text(
                "CREDIT CARD TRANSACTION ANALYSIS",
                text_align="center",
                font_size="1.3rem",
                color="#ffb800",
                font_weight="600",
            ),
            spacing="2",
            align="center",
        ),
        py="2rem",
        px="1rem",
        background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        border_radius="lg",
        box_shadow="0 4px 24px rgba(0,0,0,0.1)",
        margin_bottom="2rem",
    )

def info_section():
    return rx.callout(
        rx.vstack(
            rx.heading("How to Use", size="md", color="#ffb800"),
            rx.unordered_list(
                rx.list_item("Upload credit card transaction data (CSV or PDF)"),
                rx.list_item("File must have columns: Time, V1-V28, Amount"),
                rx.list_item("Click 'Analyze Transactions' to process with all 3 models"),
                rx.list_item("Get instant fraud detection with model comparison"),
            ),
            rx.text(
                "Your data is processed securely and never stored.",
                color="#ff4b4b",
                font_weight="600",
            ),
            spacing="1",
        ),
        icon="info",
        color_scheme="blue",
        margin_bottom="2rem",
    )

def upload_section():
    return rx.box(
        rx.vstack(
            rx.upload(
                rx.button("Upload File (CSV/PDF)", width="100%"),
                id="file-upload",
                on_drop=FraudDetectionState.handle_file_upload,
                multiple=False,
                accept=".csv,.pdf",
            ),
            rx.cond(
                FraudDetectionState.file_name != "",
                rx.text(f"File: {FraudDetectionState.file_name}", color="#6a82fb"),
            ),
            spacing="1",
        ),
        width="100%",
    )

def metrics_section():
    return rx.cond(
        FraudDetectionState.analysis_complete,
        rx.vstack(
            rx.heading("Overall Summary", size="lg", color="#232946"),
            rx.grid(
                rx.stat(
                    label="Total Transactions",
                    value=rx.cond(
                        FraudDetectionState.total_transactions > 0,
                        FraudDetectionState.total_transactions,
                        "0"
                    ),
                ),
                rx.stat(
                    label="Tuned Model Fraud",
                    value=rx.cond(
                        FraudDetectionState.tuned_fraud > 0,
                        FraudDetectionState.tuned_fraud,
                        "0"
                    ),
                    help_text="Fraudulent transactions detected",
                ),
                rx.stat(
                    label="RF Model Fraud",
                    value=rx.cond(
                        FraudDetectionState.rf_fraud > 0,
                        FraudDetectionState.rf_fraud,
                        "0"
                    ),
                ),
                rx.stat(
                    label="XGB Model Fraud",
                    value=rx.cond(
                        FraudDetectionState.xgb_fraud > 0,
                        FraudDetectionState.xgb_fraud,
                        "0"
                    ),
                ),
                columns="4",
                spacing="2",
                width="100%",
            ),
            spacing="1.5",
            width="100%",
        ),
    )

def charts_section():
    return rx.cond(
        FraudDetectionState.analysis_complete,
        rx.vstack(
            rx.heading("Visualizations", size="lg", color="#232946"),
            rx.grid(
                rx.image(src=FraudDetectionState.pie_chart_img, width="100%"),
                rx.image(src=FraudDetectionState.histogram_img, width="100%"),
                columns="2",
                spacing="2",
                width="100%",
            ),
            spacing="1.5",
            width="100%",
        ),
    )

def risk_section():
    return rx.cond(
        FraudDetectionState.analysis_complete,
        rx.vstack(
            rx.heading("Risk Summary", size="lg", color="#232946"),
            rx.grid(
                rx.stat(
                    label="100% Fraud (3/3)",
                    value=FraudDetectionState.fraud_3_count,
                    help_text="All models agree",
                ),
                rx.stat(
                    label="Medium Risk (2/3)",
                    value=FraudDetectionState.fraud_2_count,
                    help_text="Two models agree",
                ),
                rx.stat(
                    label="Low Risk (1/3)",
                    value=FraudDetectionState.fraud_1_count,
                    help_text="One model detected",
                ),
                columns="3",
                spacing="2",
                width="100%",
            ),
            spacing="1.5",
            width="100%",
        ),
    )

def messages_section():
    return rx.vstack(
        rx.cond(
            FraudDetectionState.error_message != "",
            rx.callout(
                FraudDetectionState.error_message,
                icon="alert_circle",
                color_scheme="red",
            ),
        ),
        rx.cond(
            FraudDetectionState.success_message != "",
            rx.callout(
                FraudDetectionState.success_message,
                icon="check_circle",
                color_scheme="green",
            ),
        ),
        width="100%",
    )

# ---- MAIN PAGE ----
def index():
    return rx.box(
        rx.vstack(
            header(),
            info_section(),
            upload_section(),
            messages_section(),
            metrics_section(),
            charts_section(),
            risk_section(),
            spacing="2rem",
            max_width="1200px",
            mx="auto",
        ),
        width="100%",
        padding="2rem",
        background="linear-gradient(to bottom, #f5f7fa 0%, #c3cfe2 100%)",
        min_height="100vh",
    )

# ---- REFLEX APP ----
app = rx.App()
app.add_page(index)
