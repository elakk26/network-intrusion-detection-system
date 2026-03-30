import { useEffect, useState } from "react";

function App() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchAlerts = () => {
    fetch("http://localhost:8080/api/alerts/all")
      .then((res) => res.json())
      .then((data) => {
        setAlerts(data.reverse());
        setLoading(false);
      })
      .catch((err) => console.error(err));
  };

  const getSeverityColor = (severity) => {
    if (severity === "CRITICAL") return "#ff4444";
    if (severity === "HIGH") return "#ff8800";
    return "#ffcc00";
  };

  return (
    <div style={{ backgroundColor: "#0a0a0a", minHeight: "100vh", padding: "20px", fontFamily: "monospace" }}>
      
      {/* Header */}
      <div style={{ textAlign: "center", marginBottom: "30px" }}>
        <h1 style={{ color: "#00ff88", fontSize: "28px" }}>
          🛡️ Network Intrusion Detection System
        </h1>
        <p style={{ color: "#888" }}>Live threat monitoring dashboard</p>
        <div style={{ color: "#00ff88", fontSize: "12px" }}>
          ● LIVE — Auto refreshing every 5 seconds
        </div>
      </div>

      {/* Stats */}
      <div style={{ display: "flex", gap: "20px", marginBottom: "30px", justifyContent: "center" }}>
        <div style={{ backgroundColor: "#1a1a1a", padding: "20px", borderRadius: "8px", textAlign: "center", border: "1px solid #333", minWidth: "150px" }}>
          <div style={{ color: "#00ff88", fontSize: "32px", fontWeight: "bold" }}>{alerts.length}</div>
          <div style={{ color: "#888", fontSize: "12px" }}>Total Alerts</div>
        </div>
        <div style={{ backgroundColor: "#1a1a1a", padding: "20px", borderRadius: "8px", textAlign: "center", border: "1px solid #333", minWidth: "150px" }}>
          <div style={{ color: "#ff4444", fontSize: "32px", fontWeight: "bold" }}>
            {alerts.filter(a => a.severity === "CRITICAL").length}
          </div>
          <div style={{ color: "#888", fontSize: "12px" }}>Critical</div>
        </div>
        <div style={{ backgroundColor: "#1a1a1a", padding: "20px", borderRadius: "8px", textAlign: "center", border: "1px solid #333", minWidth: "150px" }}>
          <div style={{ color: "#ff8800", fontSize: "32px", fontWeight: "bold" }}>
            {alerts.filter(a => a.severity === "HIGH").length}
          </div>
          <div style={{ color: "#888", fontSize: "12px" }}>High</div>
        </div>
      </div>

      {/* Alerts Table */}
      {loading ? (
        <div style={{ color: "#00ff88", textAlign: "center" }}>Loading alerts...</div>
      ) : alerts.length === 0 ? (
        <div style={{ color: "#888", textAlign: "center" }}>No alerts detected yet!</div>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ backgroundColor: "#1a1a1a" }}>
              <th style={{ color: "#00ff88", padding: "12px", textAlign: "left", borderBottom: "1px solid #333" }}>ID</th>
              <th style={{ color: "#00ff88", padding: "12px", textAlign: "left", borderBottom: "1px solid #333" }}>Source IP</th>
              <th style={{ color: "#00ff88", padding: "12px", textAlign: "left", borderBottom: "1px solid #333" }}>Threat Type</th>
              <th style={{ color: "#00ff88", padding: "12px", textAlign: "left", borderBottom: "1px solid #333" }}>Port</th>
              <th style={{ color: "#00ff88", padding: "12px", textAlign: "left", borderBottom: "1px solid #333" }}>Severity</th>
              <th style={{ color: "#00ff88", padding: "12px", textAlign: "left", borderBottom: "1px solid #333" }}>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {alerts.map((alert) => (
              <tr key={alert.id} style={{ borderBottom: "1px solid #222" }}>
                <td style={{ color: "#888", padding: "12px" }}>{alert.id}</td>
                <td style={{ color: "#fff", padding: "12px" }}>{alert.sourceIp}</td>
                <td style={{ color: "#fff", padding: "12px" }}>{alert.threatType}</td>
                <td style={{ color: "#fff", padding: "12px" }}>{alert.port}</td>
                <td style={{ padding: "12px" }}>
                  <span style={{
                    backgroundColor: getSeverityColor(alert.severity),
                    color: "#000",
                    padding: "4px 10px",
                    borderRadius: "4px",
                    fontSize: "12px",
                    fontWeight: "bold"
                  }}>
                    {alert.severity}
                  </span>
                </td>
                <td style={{ color: "#888", padding: "12px", fontSize: "12px" }}>
                  {new Date(alert.timestamp).toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;