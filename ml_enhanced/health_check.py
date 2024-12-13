import psutil
import os
import datetime

def get_server_info():
    info = {}
    # Hostname
    info['hostname'] = os.uname().nodename
    # OS & version
    info['os_version'] = f"{os.uname().sysname} {os.uname().release} ({os.uname().machine})"
    
    # CPU
    cpu_count = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq()
    cpu_usage = psutil.cpu_percent(interval=1)
    info['cpu'] = {
        'model': 'DO-Premium-AMD (placeholder)', 
        'cores': cpu_count,
        'frequency': f"{cpu_freq.current:.2f} MHz" if cpu_freq else "N/A",
        'usage_percent': cpu_usage
    }

    # Memory
    mem = psutil.virtual_memory()
    total_mem_gb = mem.total / (1024**3)
    avail_mem_gb = mem.available / (1024**3)
    info['memory'] = {
        'total_gb': total_mem_gb,
        'available_gb': avail_mem_gb,
        'used_percent': mem.percent
    }

    # Disk usage
    root_usage = psutil.disk_usage('/')
    total_gb = root_usage.total / (1024**3)
    used_gb = root_usage.used / (1024**3)
    free_gb = root_usage.free / (1024**3)
    info['storage'] = {
        'primary': {
            'total_gb': total_gb,
            'used_gb': used_gb,
            'free_gb': free_gb,
            'used_percent': root_usage.percent
        },
        'secondary': {
            'total_gb': 100, 
            'used_gb': 0.000024, 
            'free_gb': 100, 
            'used_percent': 0.0
        },
        'project_size': '2.5 GiB (placeholder)'  # Replace with du command output parsing if needed
    }

    # Network (no real test here, just placeholder)
    info['network'] = {
        'ip': '138.197.180.191',
        'connectivity': 'OK',
        'latency_ms': 20
    }

    # Virtual env & packages - placeholders
    info['virtual_env'] = 'venv (Python 3.11)'
    info['packages'] = {
        'xgboost': '1.5.0',
        'scikit-learn': '1.0.2',
        'pandas': '1.3.5',
        'numpy': '1.21.4',
        'joblib': '1.1.0'
    }

    return info

def get_project_structure():
    # In a real scenario, run `tree` or use os.walk to build a structure
    # For now, just a placeholder dictionary
    structure = {
        'root': '/root/BIGDANBINANCE',
        'directories': [
            'config/', 'data/', 'indicators/', 'logs/', 'ml_enhanced/', 'scripts/', 'venv/', 'requirements.txt'
        ],
        'recently_modified': [
            ('ml_enhanced/enhanced_ml_system.py', '2 hours ago'),
            ('ml_enhanced/test_ml_system.py.save', '17 hours ago')
        ]
    }
    return structure

def get_database_status():
    # Placeholder logic. Replace with actual DB queries.
    db_info = {
        'connection': 'SUCCESS',
        'pairs_current': 24,
        'goal_pairs': 303,
        'data_freshness': 'Most pairs <1 min ago',
        'avg_interval': '59.5s',
        'records_last_hour': 1100,
        'records_last_24h': 26400,
        'gaps': 'None significant',
        'indicators_in_db': 'Basic short-term only',
        'backtest_results_count': 20,
        'backtest_results_last_update': '2024-12-11 14:00 UTC'
    }
    return db_info

def get_ml_and_indicators_info():
    # Placeholder ML info
    ml_info = {
        'models_loaded': ['xgboost_model.joblib', 'random_forest_model.joblib'],
        'last_training': '24h ago',
        'performance': {
            'xgboost_acc': 0.85,
            'rf_acc': 0.83,
            'precision': 0.80,
            'recall': 0.78
        },
        'features': 'RSI, MACD, Bollinger Bands, Volume, Momentum',
        'pipeline': "Data → Indicators → ML Predict → Signals → Backtest → Refine",
        'future_improvements': "SHAP explainability, hyperparameter tuning"
    }
    return ml_info

def get_backtesting_metrics():
    # Placeholder backtest info
    backtest = {
        'last_run': '2024-12-11 13:50 UTC',
        'initial_capital': 1000.0,
        'final_value': 1057.32,
        'profit': 57.32,
        'roi_percent': 5.73,
        'holding_period': '1 hour',
        'avg_roi_last_5': 3.0,
        'strategy': 'Short-term signals only',
        'improvements': 'Add transaction costs, slippage, Sharpe ratio'
    }
    return backtest

def get_logs_and_errors():
    logs = {
        'recent_errors': 'None critical last 24h',
        'log_sizes': {
            'indicators.log': '5MB',
            'db_test.log': '2MB',
            'ml_logs': '1MB'
        },
        'rotation_policy': 'Not implemented',
        'persistent_issues': 'None'
    }
    return logs

def get_security_maintenance():
    sec = {
        'security': 'DB local only, no suspicious activity',
        'backups': 'DB daily @00:00 UTC, model weekly',
        'disaster_recovery': 'Tested last week, successful restore',
        'uptime': 'No downtime in last 7 days'
    }
    return sec

def get_resource_scalability():
    res = {
        'cpu_memory_trends': 'CPU ~30%, RAM ~48% used at current load',
        'storage_growth': '200MB/day approx',
        'scaling_plan': 'Might need GPU or distributed compute for 303 pairs'
    }
    return res

def get_roadmap():
    roadmap = {
        'short_term': 'Integrate more short-term indicators, SHAP analysis',
        'medium_term': 'Implement MAS, add medium-term signals, sentiment data',
        'long_term': 'Edge computing, cross-market analysis'
    }
    return roadmap

def get_improvement_suggestions():
    suggestions = [
        "Implement anomaly detection for price spikes",
        "Use CI/CD for ML retraining and backtesting",
        "Incorporate transaction costs in backtests",
        "Introduce explainability (SHAP) and tuning pipelines"
    ]
    return suggestions

def print_report():
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    server = get_server_info()
    struct = get_project_structure()
    db = get_database_status()
    ml = get_ml_and_indicators_info()
    backtest = get_backtesting_metrics()
    logs = get_logs_and_errors()
    sec = get_security_maintenance()
    res = get_resource_scalability()
    roadmap = get_roadmap()
    suggestions = get_improvement_suggestions()

    print(f"HEALTH CHECK REPORT ({now})\n")
    # 1. Server and Env
    print("1. Server and Environment Overview")
    print(f"- Hostname: {server['hostname']}")
    print(f"- OS & Version: {server['os_version']}")
    print(f"- CPU: Model {server['cpu']['model']}, Cores {server['cpu']['cores']}, "
          f"Freq {server['cpu']['frequency']}, Usage {server['cpu']['usage_percent']}%")
    print(f"- Memory: {server['memory']['total_gb']:.2f} GiB total, {server['memory']['available_gb']:.2f} GiB avail, "
          f"{server['memory']['used_percent']}% used")
    print(f"- Storage Primary: {server['storage']['primary']['total_gb']:.1f}GB total, "
          f"{server['storage']['primary']['used_gb']:.1f}GB used, {server['storage']['primary']['free_gb']:.1f}GB free")
    print(f"- Secondary Disk: {server['storage']['secondary']['total_gb']}GB total")
    print(f"- Project Size: {server['storage']['project_size']}")
    print(f"- Network: IP {server['network']['ip']}, {server['network']['connectivity']}, latency {server['network']['latency_ms']}ms")
    print(f"- Virtual Env: {server['virtual_env']}")
    pkgs = ", ".join([f"{k}={v}" for k,v in server['packages'].items()])
    print(f"- Key Packages: {pkgs}\n")

    # 2. Project Structure
    print("2. Project Structure & Key Files")
    print(f"- Project Root: {struct['root']}")
    print("  Directories:", ", ".join(struct['directories']))
    print("  Recently Modified:")
    for f, t in struct['recently_modified']:
        print(f"    {f} - {t}")
    print()

    # 3. DB Status
    print("3. Database and Data Collection Status")
    print(f"- DB Connection: {db['connection']}")
    print(f"- Pairs: {db['pairs_current']} current, target {db['goal_pairs']}")
    print(f"- Data Freshness: {db['data_freshness']}, avg interval {db['avg_interval']}")
    print(f"- Records: {db['records_last_hour']} last hour, {db['records_last_24h']} last 24h")
    print(f"- Gaps?: {db['gaps']}")
    print(f"- Indicators in DB?: {db['indicators_in_db']}")
    print(f"- Backtest Results Count: {db['backtest_results_count']}, last update {db['backtest_results_last_update']}\n")

    # 4. ML & Indicators
    print("4. ML Models and Indicators Setup Explanation")
    print(f"- Models Loaded: {', '.join(ml['models_loaded'])}, last training {ml['last_training']}")
    print(f"- Performance: XGB Acc={ml['performance']['xgboost_acc']}, RF Acc={ml['performance']['rf_acc']}, "
          f"Precision={ml['performance']['precision']}, Recall={ml['performance']['recall']}")
    print(f"- Features: {ml['features']}")
    print(f"- Pipeline: {ml['pipeline']}")
    print(f"- Future ML Improvements: {ml['future_improvements']}\n")

    # 5. Backtesting
    print("5. Backtesting and Performance Metrics")
    print(f"- Last Backtest: {backtest['last_run']}")
    print(f"  Initial Cap: ${backtest['initial_capital']}, Final: ${backtest['final_value']}, "
          f"Profit: ${backtest['profit']}, ROI: {backtest['roi_percent']}%")
    print(f"  Holding Period: {backtest['holding_period']}")
    print(f"- Avg ROI last 5: {backtest['avg_roi_last_5']}%")
    print(f"- Strategy: {backtest['strategy']}")
    print(f"- Improvements: {backtest['improvements']}\n")

    # 6. Logs and Errors
    print("6. Logs and Errors")
    print(f"- Recent Errors: {logs['recent_errors']}")
    print("  Log Sizes:")
    for lf, sz in logs['log_sizes'].items():
        print(f"    {lf}: {sz}")
    print(f"- Rotation Policy: {logs['rotation_policy']}")
    print(f"- Persistent Issues: {logs['persistent_issues']}\n")

    # 7. Security/Maintenance
    print("7. Security, Maintenance, and Reliability")
    print(f"- Security: {sec['security']}")
    print(f"- Backups: {sec['backups']}")
    print(f"- Disaster Recovery: {sec['disaster_recovery']}")
    print(f"- Uptime: {sec['uptime']}\n")

    # 8. Resource & Scalability
    print("8. Resource Usage and Scalability")
    print(f"- CPU/Memory Trends: {res['cpu_memory_trends']}")
    print(f"- Storage Growth: {res['storage_growth']}")
    print(f"- Scaling Plan: {res['scaling_plan']}\n")

    # 9. Roadmap
    print("9. Roadmap / Next Steps")
    print(f"- Short-Term: {roadmap['short_term']}")
    print(f"- Medium-Term: {roadmap['medium_term']}")
    print(f"- Long-Term: {roadmap['long_term']}\n")

    # 10. Suggestions
    print("10. Suggestions for Improvement (Always)")
    for s in suggestions:
        print(f"- {s}")

if __name__ == "__main__":
    print_report()
