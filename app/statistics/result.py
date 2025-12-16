#!/usr/bin/env python3
"""
German Business Document Classification
Chapter 4: Results (Ergebnisse) - Unified Analysis Script

Features:
1. Parses individual experiment_report.json AND aggregate evaluation_results_*.json.
2. Generates Dashboards, Scatter Plots, Bar Charts, and Confusion Matrices.
3  These images are named and saved consistently in the results and 
   copied to the appropriate directories in latex for visualization.
4. Produces a summary text report highlighting the best model and dataset stats."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import warnings
import matplotlib.ticker as ticker
from pathlib import Path
from io import StringIO
import sys
from app.core.paths import PROJECT_ROOT, PROCESSED_DIR


# --- Configuration ---
warnings.filterwarnings('ignore')
# Use modern Seaborn theme
sns.set_theme(style="whitegrid", context="paper", font_scale=1.8)

# Use a serif font that is more common in academic papers
plt.rcParams['font.family'] = 'serif'
# --- Constants ---
MODELS_DIR = PROJECT_ROOT / "models"
RESULTS_DIR = PROJECT_ROOT / "results"
DATA_PATH = PROCESSED_DIR / "all_data.csv"



# --- Utilities ---
def log(msg: str):
    print(f"[INFO] {msg}")

def save_fig(fig, filename: str):
    """Saves a figure to the output directory with high DPI."""
    path = RESULTS_DIR / filename
    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    log(f"✓ Saved Figure: {filename}")

def get_available_models() -> list[Path]:
    if not MODELS_DIR.exists():
        return []
    return [d for d in MODELS_DIR.iterdir() if d.is_dir()]

def find_latest_aggregate_file():
    """Finds the most recent evaluation_results_*.json file."""
    candidates = []
    if MODELS_DIR.exists():
        candidates.extend(list(MODELS_DIR.glob("evaluation_results_*.json")))
        # Legacy check
        if (MODELS_DIR / "evaluation_results.json").exists():
            candidates.append(MODELS_DIR / "evaluation_results.json")
    if RESULTS_DIR.exists():
        candidates.extend(list(RESULTS_DIR.glob("evaluation_results_*.json")))
    
    if not candidates: return None
    # Sort by filename (assumes timestamp in name)
    return sorted(candidates, key=lambda x: x.name)[-1]

def load_aggregate_results():
    path = find_latest_aggregate_file()
    if path and path.exists():
        try:
            with open(path, 'r') as f: return json.load(f)
        except Exception as e:
            log(f"Error reading aggregate JSON: {e}")
    return {}

# --- Data Loading Logic ---

def load_experiment_data(model_dirs):
    """
    Parses both individual 'experiment_report.json' files and the aggregate JSON.
    """
    records = []
    aggregate_data = load_aggregate_results()

    for model_dir in model_dirs:
        # Skip files in the models root
        if model_dir.is_file(): continue
        
        report_path = model_dir / "experiment_report.json"
        model_name = model_dir.name.replace("_", "-")
        
        # Initialize Records
        record_val = {"Model": model_name, "Dataset": "Validation", "Accuracy": 0, "F1_Score": 0, "Loss": 0, "Samples_Per_Sec": 0}
        record_test = {"Model": model_name, "Dataset": "Test", "Accuracy": 0, "F1_Score": 0, "Loss": 0, "Samples_Per_Sec": 0}

        # 1. Try Loading from individual report
        if report_path.exists():
            try:
                with open(report_path, 'r') as f: data = json.load(f)
                
                # Validation
                val = data.get("phases", {}).get("2_validation", {}).get("metrics", {})
                record_val.update({
                    "Accuracy": val.get("validation_accuracy", 0),
                    "F1_Score": val.get("validation_f1", 0),
                    "Loss": val.get("validation_loss", 0)
                })
                # Test
                test = data.get("phases", {}).get("3_testing", {}).get("metrics", {})
                record_test.update({
                    "Accuracy": test.get("test_accuracy", 0),
                    "F1_Score": test.get("test_f1", 0),
                    "Loss": test.get("test_loss", 0)
                })
            except Exception: pass

        # 2. Try Loading/Filling from Aggregate JSON
        if aggregate_data:
            # Normalize names for fuzzy matching (e.g. "gbert-base" matches "gbertbase")
            norm_folder = model_dir.name.replace("_", "").replace("-", "").lower()
            
            found_key = None
            for key in aggregate_data.keys():
                if norm_folder in key.replace("_", "").replace("-", "").replace("/", "").lower():
                    found_key = key
                    break
            
            if found_key:
                # Validation
                v_metrics = aggregate_data[found_key].get("validation", {})
                if record_val["Accuracy"] == 0: record_val["Accuracy"] = v_metrics.get("eval_accuracy", 0)
                if record_val["F1_Score"] == 0: record_val["F1_Score"] = v_metrics.get("eval_f1", 0)
                record_val["Samples_Per_Sec"] = v_metrics.get("eval_samples_per_second", 0)

                # Test
                t_metrics = aggregate_data[found_key].get("test", {})
                if record_test["Accuracy"] == 0: record_test["Accuracy"] = t_metrics.get("eval_accuracy", 0)
                if record_test["F1_Score"] == 0: record_test["F1_Score"] = t_metrics.get("eval_f1", 0)
                record_test["Samples_Per_Sec"] = t_metrics.get("eval_samples_per_second", 0)

        # Append if data exists
        if record_val["Accuracy"] > 0 or record_val["F1_Score"] > 0: records.append(record_val)
        if record_test["Accuracy"] > 0 or record_test["F1_Score"] > 0: records.append(record_test)

    return pd.DataFrame(records)

# --- Visualization Functions ---

def plot_f1_score_bar(df):
    """Generates a bar chart for F1 Score."""
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(data=df, x='Model', y='F1_Score', hue='Dataset', ax=ax, palette="viridis")
    min_f1 = df['F1_Score'].min()
    ax.set_ylim(max(0, min_f1 - 0.05), 1.01) # Zoom in slightly
    ax.set_title('Model Performance (F1 Score)', fontweight='bold', pad=15)
    
    # --- FIX BELOW: Removed ha='right' ---
    ax.tick_params(axis='x', rotation=45) 
    
    # This line handles the alignment correctly, so keep it:
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    save_fig(fig, "fig_bar_f1_score.png")

def plot_loss_bar(df):
    """Generates a bar chart for Model Loss."""
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(data=df, x='Model', y='Loss', hue='Dataset', ax=ax, palette="magma")
    ax.set_title('Model Loss (Lower is Better)', fontweight='bold', pad=15)
    
    # --- FIX BELOW: Removed ha='right' ---
    ax.tick_params(axis='x', rotation=45)
    
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    ax.legend(title='Dataset')
    save_fig(fig, "fig_bar_loss.png")

def plot_speed_bar(df):
    """Generates a bar chart for Inference Speed."""
    speed_df = df[df['Dataset'] == 'Test']
    if not speed_df.empty and speed_df['Samples_Per_Sec'].sum() > 0:
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(data=speed_df, x='Model', y='Samples_Per_Sec', ax=ax, color="skyblue", edgecolor='black')
        ax.set_title('Inference Speed (Samples/Sec)', fontweight='bold', pad=15)
        
        # --- FIX BELOW: Removed ha='right' ---
        ax.tick_params(axis='x', rotation=45)
        
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        for container in ax.containers:
            ax.bar_label(container, fmt='%.0f', padding=3, fontsize=14)
        save_fig(fig, "fig_bar_inference_speed.png")

def plot_metrics_dashboard(df):
    """Generates separate plots for F1, Loss, and Speed."""
    log("Generating Dashboard plots...")
    plot_f1_score_bar(df)
    plot_loss_bar(df)
    plot_speed_bar(df)

def plot_tradeoff_scatter(df):
    """Scatter plot: Speed vs Accuracy."""
    test_df = df[df['Dataset'] == 'Test']
    if test_df.empty or test_df['Samples_Per_Sec'].sum() == 0: return

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.scatterplot(
        data=test_df, x='Samples_Per_Sec', y='F1_Score', 
        hue='Model', style='Model', s=300, palette='deep', ax=ax
    )

    ax.set_title('Trade-off: Inference Speed vs Test F1 Score', fontweight='bold', pad=20)
    ax.set_xlabel('Speed (Samples/Sec) - Higher is Better', fontweight='bold')
    ax.set_ylabel('F1 Score - Higher is Better', fontweight='bold')
    
    # Legend placement
    # Adjust legend to be cleanly placed at the bottom.
    # 'loc='upper center'' anchors the top of the legend box.
    # 'bbox_to_anchor' places it relative to the plot axes. The y-value is lowered for more space.    
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=3, fancybox=True, shadow=False, frameon=False)
    
    save_fig(fig, "fig_scatter_speed_vs_f1.png")

def plot_single_comparison(df, metric, title, filename):
    """Generic bar plot for a single metric."""
    plot_df = df[df[metric] > 0]
    if plot_df.empty: return

    fig, ax = plt.subplots(figsize=(14, 8))
    sns.barplot(data=plot_df, x=metric, y='Model', hue='Dataset', 
                ax=ax, palette='Paired', edgecolor='black', alpha=0.9)
    
    ax.set_title(title, fontweight='bold', pad=15)
    ax.set_xlabel(metric.replace('_', ' '), fontweight='bold')
    
    # Label bars
    fmt = '%.1f' if plot_df[metric].max() > 10 else '%.4f'
    for container in ax.containers:
        ax.bar_label(container, fmt=fmt, padding=3, fontsize=14)

    # Zoom if F1/Acc
    if plot_df[metric].max() <= 1.0:
        ax.set_xlim(0, 1.1)
    
    save_fig(fig, filename)

def plot_class_distribution(df_data):
    """Plots class counts and text length distributions."""
    # 1. Bar Chart
    class_counts = df_data['label'].value_counts().reset_index()
    class_counts.columns = ['label', 'count']
    
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.barplot(data=class_counts, x='label', y='count', palette='husl', ax=ax, edgecolor='black')
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom', xytext=(0, 5), textcoords='offset points', fontsize=14)
    ax.set_title('Document Class Distribution', fontweight='bold')
    save_fig(fig, 'fig_dataset_class_distribution.png')

    # 2. Box Plot (Text Length)
    if 'text' in df_data.columns:
        df_data['text_length'] = df_data['text'].str.len()
        fig2, ax2 = plt.subplots(figsize=(14, 8))
        sns.boxplot(data=df_data, x='label', y='text_length', palette="Set2", ax=ax2)
        ax2.set_yscale('log')
        ax2.set_title('Text Length Distribution by Class (Log Scale)', fontweight='bold')
        ax2.set_ylabel('Text Length (Characters)')
        save_fig(fig2, 'fig_dataset_text_length_by_class.png')

def plot_confusion_matrix(report_path, model_name):
    """Loads a specific confusion matrix from experiment_report.json."""
    try:
        with open(report_path, 'r') as f: data = json.load(f)
        
        cm_data = data.get('confusion_matrix')
        # Check nested location if not at root
        if not cm_data:
            cm_data = data.get("phases", {}).get("3_testing", {}).get("metrics", {}).get("confusion_matrix")
            
        labels = data.get('dataset_config', {}).get('label_classes')
        if not labels: labels = data.get('labels')

        if cm_data and labels:
            cm = np.array(cm_data)
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                        xticklabels=labels, yticklabels=labels, 
                        ax=ax, annot_kws={"weight": "bold"})
            ax.set_title(f'Confusion Matrix: {model_name}', fontweight='bold', pad=20)
            ax.set_xlabel('Predicted')
            ax.set_ylabel('Actual')
            plt.xticks(rotation=45, ha='right')
            plt.yticks(rotation=0)
            save_fig(fig, f'fig_cm_{model_name}.png')
    except Exception as e:
        pass

# --- Main Execution ---

def generate_results():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    log(f"Starting Result Analysis. Output: {RESULTS_DIR.resolve()}")

    # 1. Dataset Analysis (Only if CSV exists)
    if DATA_PATH.exists():
        log("Analyzing Dataset...")
        try:
            raw_data = pd.read_csv(DATA_PATH)
            plot_class_distribution(raw_data)
        except Exception as e:
            log(f"⚠️ Dataset plot error: {e}")
    else:
        log("ℹ️ Dataset CSV not found. Skipping dataset plots.")

    # 2. Model Data Loading
    log("Scanning models...")
    model_dirs = get_available_models()
    
    # Try loading from disk
    results_df = load_experiment_data(model_dirs)
    
    # Fallback Mechanism
    if results_df.empty:
        log("⚠️ No valid JSON data found in 'models/' directory.")
        log("🔄 Using FALLBACK CSV data for demonstration.")
        results_df = pd.read_csv(StringIO((RESULTS_DIR / 'table_model_performance.csv').read_text()))
    else:
        log(f"✓ Loaded data for {results_df['Model'].nunique()} models from disk.")

    if results_df.empty:
        log("❌ No data available (Local or Fallback). Exiting.")
        return

    # 3. Clean and Save Data
    results_df = results_df.round(4)
    results_df.to_csv(RESULTS_DIR / 'table_model_performance.csv', index=False)

    # 4. Generate Visualizations
    log("Generating Visualizations...")
    
    # A. Dashboard (Overview)
    plot_metrics_dashboard(results_df)
    
    # B. Trade-off (Speed vs F1)
    plot_tradeoff_scatter(results_df)
    
    # C. Detailed Bar Charts
    plot_single_comparison(results_df, 'F1_Score', 'Model Comparison: F1-Score', 'fig_comparison_f1_score.png')
    plot_single_comparison(results_df, 'Accuracy', 'Model Comparison: Accuracy', 'fig_comparison_accuracy.png')

    # D. Confusion Matrices (Requires local JSON files)
    for model_dir in model_dirs:
        if model_dir.is_file(): continue
        plot_confusion_matrix(model_dir / "experiment_report.json", model_dir.name.replace("_", "-"))

    # 5. Summary Text Report
    try:
        test_df = results_df[results_df['Dataset'] == 'Test']
        if not test_df.empty:
            best = test_df.sort_values('F1_Score', ascending=False).iloc[0]
            summary = f"""
# Thesis Results Summary
Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

## Best Performing Model
**Model:** {best['Model']}
**F1-Score:** {best['F1_Score']:.4f}
**Accuracy:** {best['Accuracy']:.4f}
**Inference Speed:** {best['Samples_Per_Sec']:.1f} samples/sec

## Dataset Overview
Total Models Evaluated: {results_df['Model'].nunique()}
            """
            with open(RESULTS_DIR / 'summary_report.txt', 'w') as f:
                f.write(summary)
            log("✓ Saved: summary_report.txt")
    except Exception as e:
        log(f"⚠️ Summary generation error: {e}")

    log("✓ Process Complete.")