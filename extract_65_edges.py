import json
from src.engine.report_generator import ReportGenerator

rg = ReportGenerator('c:/Proyectos/kha0sys3/data', 'c:/Proyectos/kha0sys3/src/infrastructure/config/asset_config.json', 'reports')

hyper_edges = {}

for sym, cfg in rg.config.items():
    durations = [15, 30, 45, 60]
    sessions = cfg.get("sessions", [])
    
    asset_edges = []
    
    for sess in sessions:
        for d_min in durations:
            try:
                metrics = rg._evaluate_combo(
                    rg.loader.load_data(sym, "M15"), 
                    sess["time_start"], 
                    d_min
                )
                if "error" in metrics: continue
                
                def check_metrics(m_dict, condition_name):
                    try:
                        if m_dict['extensions']['UP']['up_gt_1.5_or'] >= 0.65:
                            asset_edges.append({"type": "momentum_up", "session": sess_name, "condition": condition_name, "prob": m_dict['extensions']['UP']['up_gt_1.5_or']})
                        if m_dict['extensions']['DOWN']['down_gt_1.5_or'] >= 0.65:
                            asset_edges.append({"type": "momentum_down", "session": sess_name, "condition": condition_name, "prob": m_dict['extensions']['DOWN']['down_gt_1.5_or']})
                        if m_dict['false_breaks']['p_false_breakup'] >= 0.65:
                            asset_edges.append({"type": "fade_breakup", "session": sess_name, "condition": condition_name, "prob": m_dict['false_breaks']['p_false_breakup']})
                        if m_dict['false_breaks']['p_false_breakdown'] >= 0.65:
                            asset_edges.append({"type": "fade_breakdown", "session": sess_name, "condition": condition_name, "prob": m_dict['false_breaks']['p_false_breakdown']})
                        if m_dict['pd_interactions']['p_touch_pd_close'] >= 0.65:
                            asset_edges.append({"type": "magnet_pd_close", "session": sess_name, "condition": condition_name, "prob": m_dict['pd_interactions']['p_touch_pd_close']})
                        if m_dict['pd_interactions']['p_touch_pd_mid'] >= 0.65:
                            asset_edges.append({"type": "magnet_pd_mid", "session": sess_name, "condition": condition_name, "prob": m_dict['pd_interactions']['p_touch_pd_mid']})
                    except KeyError:
                        pass
                        
                check_metrics(metrics, "Global")
                
                # Check Advanced
                adv = metrics.get('advanced_crossing', {})
                for k, v in adv.items():
                    # The subsets have different dictionary structures returned by _get_core_edges!
                    try:
                        if v.get('up_ext_1.5', 0) >= 0.65: asset_edges.append({"type": "momentum_up", "session": sess_name, "condition": k, "prob": v['up_ext_1.5']})
                        if v.get('dw_ext_1.5', 0) >= 0.65: asset_edges.append({"type": "momentum_down", "session": sess_name, "condition": k, "prob": v['dw_ext_1.5']})
                        if v.get('f_breakup', 0) >= 0.65: asset_edges.append({"type": "fade_breakup", "session": sess_name, "condition": k, "prob": v['f_breakup']})
                        if v.get('f_breakdw', 0) >= 0.65: asset_edges.append({"type": "fade_breakdown", "session": sess_name, "condition": k, "prob": v['f_breakdw']})
                        if v.get('touch_pd_close', 0) >= 0.65: asset_edges.append({"type": "magnet_pd_close", "session": sess_name, "condition": k, "prob": v['touch_pd_close']})
                        if v.get('touch_pd_mid', 0) >= 0.65: asset_edges.append({"type": "magnet_pd_mid", "session": sess_name, "condition": k, "prob": v['touch_pd_mid']})
                    except KeyError:
                        pass

                    
            except Exception:
                pass
                
    if asset_edges:
        hyper_edges[sym] = asset_edges
        
with open("c:/Proyectos/kha0sys3/high_prob_edges.json", "w") as f:
    json.dump(hyper_edges, f, indent=4)
    
print(f"Extraction complete. {len(hyper_edges)} assets passed the 65% threshold.")
