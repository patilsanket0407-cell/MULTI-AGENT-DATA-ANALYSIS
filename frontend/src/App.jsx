import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    if (!selectedFile) {
      return;
    }

    if (!selectedFile.name.toLowerCase().endsWith(".csv")) {
      setError("Please select a CSV file.");
      setFile(null);
      return;
    }

    setFile(selectedFile);
    setError("");
    setResult(null);
  };

  const analyzeDataset = async () => {
    if (!file) {
      setError("Please select a CSV file first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Dataset analysis failed."
        );
      }

      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  const results = result?.results || {};

  const datasetResult = results.dataset_result || {};
  const preprocessingResult = results.preprocessing_result || {};
  const analysisResult = results.analysis_result || {};
  const patternResult = results.pattern_result || {};
  const visualizationResult =
    results.visualization_result || {};
  const insightResult = results.insight_result || {};

  const datasetInfo =
    datasetResult.dataset_info || {};

  const preprocessingInfo =
    preprocessingResult.preprocessing_info || {};

  const numericalAnalysis =
    analysisResult.numerical_analysis || {};

  const categoricalAnalysis =
    analysisResult.categorical_analysis || {};

  const correlations =
    analysisResult.correlation || {};

  const patterns =
    patternResult.patterns || {};

  const visualizationSummary =
    visualizationResult.visualization_summary || {};

  const charts =
    visualizationSummary.charts || [];

  const aiInsights =
    insightResult.ai_insights || {};
    
    console.log("INSIGHT RESULT:", insightResult);
    console.log("AI INSIGHTS:", aiInsights);

  const insights =
    aiInsights.key_insights || [];

  const getChartUrl = (chart) => {
    if (chart.startsWith("http")) {
      return chart;
    }

    return `${API_URL}${chart}`;
  };

  return (
    <div className="app">

      {/* ================================================= */}
      {/* HEADER */}
      {/* ================================================= */}

      <header className="header">
        <div>
          <h1>Multi-Agent Data Analysis</h1>

          <p>
            AI-powered automated dataset analysis using
            LangGraph
          </p>
        </div>

        {result && (
          <div className="status-badge">
            Analysis Complete
          </div>
        )}
      </header>


      {/* ================================================= */}
      {/* UPLOAD SECTION */}
      {/* ================================================= */}

      <section className="upload-section">

        <div className="upload-content">

          <div className="upload-icon">
            📊
          </div>

          <h2>Upload Dataset</h2>

          <p>
            Upload a CSV file and let the six AI agents
            analyze it automatically.
          </p>

          <label className="file-button">
            Choose CSV File

            <input
              type="file"
              accept=".csv"
              onChange={handleFileChange}
            />
          </label>

          {file && (
            <div className="selected-file">
              <strong>Selected:</strong>{" "}
              {file.name}
            </div>
          )}

          <button
            className="analyze-button"
            onClick={analyzeDataset}
            disabled={!file || loading}
          >
            {loading
              ? "Agents Analyzing..."
              : "Analyze Dataset"}
          </button>

          {loading && (
            <div className="loading-box">
              <div className="spinner"></div>

              <p>
                Dataset → Preprocessing → Analysis →
                Pattern Detection → Visualization →
                Insights
              </p>
            </div>
          )}

          {error && (
            <div className="error-box">
              {error}
            </div>
          )}

        </div>

      </section>


      {/* ================================================= */}
      {/* RESULTS */}
      {/* ================================================= */}

      {result && (
        <main className="results">

          <div className="results-title">
            <div>
              <h2>Analysis Results</h2>

              <p>
                Complete multi-agent analysis for{" "}
                <strong>{result.filename}</strong>
              </p>
            </div>
          </div>


          {/* ================================================= */}
          {/* OVERVIEW */}
          {/* ================================================= */}

          <section className="section">

            <div className="section-header">
              <span className="agent-number">
                1
              </span>

              <div>
                <h2>Dataset Agent</h2>

                <p>
                  Dataset structure and basic information
                </p>
              </div>
            </div>

            <div className="stats-grid">

              <StatCard
                title="Rows"
                value={datasetInfo.rows ?? "-"}
                icon="👥"
              />

              <StatCard
                title="Columns"
                value={datasetInfo.columns ?? "-"}
                icon="📋"
              />

              <StatCard
                title="Features"
                value={
                  datasetInfo.column_names?.length ?? "-"
                }
                icon="🔢"
              />

              <StatCard
                title="Missing Values"
                value={
                  preprocessingInfo.missing_values_before ??
                  "-"
                }
                icon="✓"
              />

            </div>


            {/* Dataset columns */}

            {datasetInfo.column_names && (
              <div className="card">

                <h3>Dataset Columns</h3>

                <div className="tag-container">

                  {datasetInfo.column_names.map(
                    (column) => (
                      <span
                        className="tag"
                        key={column}
                      >
                        {column}
                      </span>
                    )
                  )}

                </div>

              </div>
            )}


            {/* Dataset preview */}

            {datasetResult.preview && (
              <div className="card">

                <h3>Dataset Preview</h3>

                <div className="table-wrapper">

                  <table>

                    <thead>

                      <tr>
                        {Object.keys(
                          datasetResult.preview[0] || {}
                        ).map((column) => (
                          <th key={column}>
                            {column}
                          </th>
                        ))}
                      </tr>

                    </thead>

                    <tbody>

                      {datasetResult.preview.map(
                        (row, index) => (
                          <tr key={index}>

                            {Object.keys(row).map(
                              (column) => (
                                <td key={column}>
                                  {String(
                                    row[column] ?? ""
                                  )}
                                </td>
                              )
                            )}

                          </tr>
                        )
                      )}

                    </tbody>

                  </table>

                </div>

              </div>
            )}

          </section>


          {/* ================================================= */}
          {/* PREPROCESSING AGENT */}
          {/* ================================================= */}

          <section className="section">

            <div className="section-header">
              <span className="agent-number">
                2
              </span>

              <div>
                <h2>Preprocessing Agent</h2>

                <p>
                  Dataset cleaning and preprocessing
                </p>
              </div>
            </div>

            <div className="stats-grid">

              <StatCard
                title="Original Rows"
                value={
                  preprocessingInfo.original_rows ??
                  "-"
                }
              />

              <StatCard
                title="Original Columns"
                value={
                  preprocessingInfo.original_columns ??
                  "-"
                }
              />

              <StatCard
                title="Duplicates Removed"
                value={
                  preprocessingInfo.duplicates_removed ??
                  "-"
                }
              />

              <StatCard
                title="Missing Before"
                value={
                  preprocessingInfo.missing_values_before ??
                  "-"
                }
              />

              <StatCard
                title="Missing After"
                value={
                  preprocessingInfo.missing_values_after ??
                  "-"
                }
              />

              <StatCard
                title="Final Rows"
                value={
                  preprocessingInfo.final_rows ??
                  "-"
                }
              />

              <StatCard
                title="Final Columns"
                value={
                  preprocessingInfo.final_columns ??
                  "-"
                }
              />

            </div>

          </section>


          {/* ================================================= */}
          {/* ANALYSIS AGENT */}
          {/* ================================================= */}

          <section className="section">

            <div className="section-header">
              <span className="agent-number">
                3
              </span>

              <div>
                <h2>Analysis Agent</h2>

                <p>
                  Numerical, categorical and correlation
                  analysis
                </p>
              </div>
            </div>


            {/* Numerical */}

            <div className="card">

              <div className="card-title-row">
                <h3>Numerical Analysis</h3>

                <span className="count-badge">
                  {Object.keys(
                    numericalAnalysis
                  ).length}{" "}
                  Features
                </span>
              </div>

              <div className="table-wrapper">

                <table>

                  <thead>

                    <tr>
                      <th>Feature</th>
                      <th>Mean</th>
                      <th>Median</th>
                      <th>Minimum</th>
                      <th>Maximum</th>
                      <th>Std. Dev.</th>
                    </tr>

                  </thead>

                  <tbody>

                    {Object.entries(
                      numericalAnalysis
                    ).map(
                      ([feature, stats]) => (
                        <tr key={feature}>

                          <td>
                            <strong>
                              {feature}
                            </strong>
                          </td>

                          <td>
                            {formatNumber(
                              stats.mean
                            )}
                          </td>

                          <td>
                            {formatNumber(
                              stats.median
                            )}
                          </td>

                          <td>
                            {formatNumber(
                              stats.minimum
                            )}
                          </td>

                          <td>
                            {formatNumber(
                              stats.maximum
                            )}
                          </td>

                          <td>
                            {formatNumber(
                              stats.standard_deviation
                            )}
                          </td>

                        </tr>
                      )
                    )}

                  </tbody>

                </table>

              </div>

            </div>


            {/* Categorical */}

            <div className="card">

              <div className="card-title-row">

                <h3>
                  Categorical Analysis
                </h3>

                <span className="count-badge">
                  {Object.keys(
                    categoricalAnalysis
                  ).length}{" "}
                  Features
                </span>

              </div>

              <div className="category-grid">

                {Object.entries(
                  categoricalAnalysis
                ).map(
                  ([feature, values]) => (
                    <div
                      className="category-card"
                      key={feature}
                    >

                      <h4>{feature}</h4>

                      {Object.entries(
                        values
                      ).map(
                        ([value, count]) => (
                          <div
                            className="category-row"
                            key={value}
                          >

                            <span>
                              {value}
                            </span>

                            <strong>
                              {count}
                            </strong>

                          </div>
                        )
                      )}

                    </div>
                  )
                )}

              </div>

            </div>


            {/* Correlations */}

            <div className="card">

              <h3>
                Correlation Analysis
              </h3>

              <div className="correlation-grid">

                {getStrongCorrelations(
                  correlations
                ).map(
                  (item, index) => (
                    <div
                      className="correlation-card"
                      key={index}
                    >

                      <div>
                        <strong>
                          {item.feature1}
                        </strong>

                        <span> ↔ </span>

                        <strong>
                          {item.feature2}
                        </strong>
                      </div>

                      <div className="correlation-value">
                        {item.value.toFixed(2)}
                      </div>

                    </div>
                  )
                )}

              </div>

            </div>

          </section>


          {/* ================================================= */}
          {/* PATTERN AGENT */}
          {/* ================================================= */}

          <section className="section">

            <div className="section-header">

              <span className="agent-number">
                4
              </span>

              <div>
                <h2>Pattern Agent</h2>

                <p>
                  Important patterns, correlations and
                  outliers
                </p>
              </div>

            </div>


            {/* Correlations */}

            <div className="card">

              <h3>
                Strong Correlations
              </h3>

              <div className="pattern-list">

                {(patterns.correlations || []).map(
                  (item, index) => (
                    <div
                      className="pattern-item"
                      key={index}
                    >

                      <div>

                        <strong>
                          {item.feature_1}
                        </strong>

                        <span>
                          {" "}↔{" "}
                        </span>

                        <strong>
                          {item.feature_2}
                        </strong>

                      </div>

                      <span className="value-pill">
                        {Number(
                          item.correlation
                        ).toFixed(2)}
                      </span>

                    </div>
                  )
                )}

              </div>

            </div>


            {/* Outliers */}

            <div className="card">

              <h3>
                Outlier Detection
              </h3>

              <div className="outlier-grid">

                {(patterns.outliers || []).map(
                  (item) => (
                    <div
                      className="outlier-card"
                      key={item.column}
                    >

                      <h4>
                        {item.column}
                      </h4>

                      <div className="outlier-number">
                        {item.outlier_count}
                      </div>

                      <p>
                        {item.percentage}%
                        {" "}of values
                      </p>

                    </div>
                  )
                )}

              </div>

            </div>


            {/* Categorical patterns */}

            <div className="card">

              <h3>
                Categorical Patterns
              </h3>

              <div className="pattern-list">

                {(
                  patterns.categorical_patterns ||
                  []
                ).map(
                  (item) => (
                    <div
                      className="pattern-item"
                      key={item.column}
                    >

                      <div>

                        <strong>
                          {item.column}
                        </strong>

                        <span>
                          {" "}
                          →
                          {" "}
                          {item.most_common_value}
                        </span>

                      </div>

                      <span className="value-pill">
                        {item.percentage}%
                      </span>

                    </div>
                  )
                )}

              </div>

            </div>

          </section>


          {/* ================================================= */}
          {/* VISUALIZATION AGENT */}
          {/* ================================================= */}

          <section className="section">

            <div className="section-header">

              <span className="agent-number">
                5
              </span>

              <div>

                <h2>
                  Visualization Agent
                </h2>

                <p>
                  Automatically generated dataset
                  visualizations
                </p>

              </div>

              <span className="count-badge">
                {charts.length} Charts
              </span>

            </div>


            <div className="charts-grid">

              {charts.map(
                (chart, index) => (
                  <div
                    className="chart-card"
                    key={chart}
                  >

                    <div className="chart-header">
                      <span>
                        Chart {index + 1}
                      </span>
                    </div>

                    <img
                      src={getChartUrl(chart)}
                      alt={`Chart ${index + 1}`}
                    />

                    <p>
                      {chart.split("/").pop()}
                    </p>

                  </div>
                )
              )}

            </div>

          </section>


          {/* ================================================= */}
          {/* INSIGHT AGENT */}
          {/* ================================================= */}

          <section className="section">

            <div className="section-header">

              <span className="agent-number">
                6
              </span>

              <div>

                <h2>
                  Insight Agent
                </h2>

                <p>
                  Automatically generated insights
                  from the complete analysis
                </p>

              </div>

              <span className="count-badge">
                {insights.length} Insights
              </span>

            </div>


            {/* AI Summary */}

            {aiInsights.summary && (

              <div className="card">

                <h3>
                  AI Summary
                </h3>

                <p>
                  {aiInsights.summary}
                </p>

              </div>

            )}


            {/* Key Insights */}

            <div className="insights-grid">

              {insights.map(
                (insight, index) => (

                  <div
                    className="insight-card"
                    key={index}
                  >

                    <div className="insight-number">
                      {index + 1}
                    </div>

                    <h3>
                      {insight.title}
                    </h3>

                    <p>
                      {insight.insight}
                    </p>

                    {insight.evidence && (

                      <div>

                        <strong>
                          Evidence:
                        </strong>

                        <p>
                          {insight.evidence}
                        </p>

                      </div>

                    )}

                    {insight.interpretation && (

                      <div>

                        <strong>
                          Business Interpretation:
                        </strong>

                        <p>
                          {insight.interpretation}
                        </p>

                      </div>

                    )}

                  </div>

                )
              )}

            </div>


            {/* Recommendations */}

            {aiInsights.recommendations?.length > 0 && (

              <div className="card">

                <h3>
                  Recommendations
                </h3>

                <ul>

                  {aiInsights.recommendations.map(
                    (recommendation, index) => (

                      <li key={index}>
                        {recommendation}
                      </li>

                    )
                  )}

                </ul>

              </div>

            )}


            {/* Risk Factors */}

            {aiInsights.risk_factors?.length > 0 && (

              <div className="card">

                <h3>
                  Risk Factors & Limitations
                </h3>

                <ul>

                  {aiInsights.risk_factors.map(
                    (risk, index) => (

                      <li key={index}>
                        {risk}
                      </li>

                    )
                  )}

                </ul>

              </div>

            )}

          </section>

        </main>
      )}

    </div>
  );
}


/* ============================================================ */
/* STAT CARD */
/* ============================================================ */

function StatCard({
  title,
  value,
  icon
}) {
  return (
    <div className="stat-card">

      {icon && (
        <div className="stat-icon">
          {icon}
        </div>
      )}

      <div>

        <p>
          {title}
        </p>

        <h3>
          {value}
        </h3>

      </div>

    </div>
  );
}


/* ============================================================ */
/* FORMAT NUMBER */
/* ============================================================ */

function formatNumber(value) {

  if (
    value === null ||
    value === undefined ||
    Number.isNaN(Number(value))
  ) {
    return "-";
  }

  const number = Number(value);

  if (Number.isInteger(number)) {
    return number;
  }

  return number.toFixed(2);
}


/* ============================================================ */
/* GET STRONG CORRELATIONS */
/* ============================================================ */

function getStrongCorrelations(correlationData) {

  const result = [];
  const seen = new Set();

  Object.entries(correlationData).forEach(
    ([feature1, values]) => {

      Object.entries(values).forEach(
        ([feature2, value]) => {

          const numericValue = Number(value);

          if (
            feature1 === feature2 ||
            !Number.isFinite(numericValue)
          ) {
            return;
          }

          if (Math.abs(numericValue) < 0.7) {
            return;
          }

          const key = [
            feature1,
            feature2
          ].sort().join("|");

          if (seen.has(key)) {
            return;
          }

          seen.add(key);

          result.push({
            feature1,
            feature2,
            value: numericValue
          });
        }
      );
    }
  );

  return result.sort(
    (a, b) =>
      Math.abs(b.value) -
      Math.abs(a.value)
  );
}


export default App;

