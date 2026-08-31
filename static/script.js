

async function generateTests() {

    const requirement =
        document.getElementById("requirement").value;

    const resultDiv =
        document.getElementById("testResults");

    if (!requirement.trim()) {

        resultDiv.innerHTML =
            "<p class='failure'>Please enter a requirement.</p>";

        return;
    }

    resultDiv.innerHTML =
        "<p>Generating test cases...</p>";

    try {

        const response = await fetch(
            "/api/generate-tests",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    requirement: requirement
                })
            }
        );

        const data = await response.json();

        if (!data.success) {

            resultDiv.innerHTML =
                `<p class="failure">${data.message}</p>`;

            return;
        }

        let html = `
            <div class="result-box">

            <h3>
                Generated ${data.count} Test Cases
            </h3>

            <table class="test-table">

            <tr>
                <th>ID</th>
                <th>Type</th>
                <th>Test Case</th>
                <th>Expected Result</th>
            </tr>
        `;

        data.test_cases.forEach(test => {

            html += `
                <tr>

                    <td>${test.id}</td>

                    <td>${test.type}</td>

                    <td>${test.test_case}</td>

                    <td>${test.expected}</td>

                </tr>
            `;

        });

        html += `
            </table>
            </div>
        `;

        resultDiv.innerHTML = html;

    } catch (error) {

        resultDiv.innerHTML =
            `<p class="failure">
                Error: ${error}
            </p>`;
    }
}


// --------------------------------------------------
// MODULE 2
// AUTOMATED TEST EXECUTION
// --------------------------------------------------

async function runTests() {

    const resultDiv =
        document.getElementById(
            "executionResults"
        );

    if (!resultDiv) return;

    resultDiv.innerHTML =
        "<p>Executing automated tests...</p>";

    try {

        const response = await fetch(
            "/api/run-tests",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                }
            }
        );

        const data = await response.json();

        const result = data.result;

        let statusClass =
            result.status === "PASSED"
                ? "success"
                : "failure";

        resultDiv.innerHTML = `

            <div class="result-box">

                <h3 class="${statusClass}">
                    ${result.status}
                </h3>

                <p>
                    <strong>Total Tests:</strong>
                    ${result.total}
                </p>

                <p>
                    <strong>Passed:</strong>
                    ${result.passed}
                </p>

                <p>
                    <strong>Failed:</strong>
                    ${result.failed}
                </p>

                <p>
                    <strong>Errors:</strong>
                    ${result.errors}
                </p>

                <p>
                    <strong>Execution Time:</strong>
                    ${result.execution_time} seconds
                </p>

                <h4>Execution Log</h4>

                <pre>${escapeHtml(result.output)}</pre>

            </div>
        `;

        loadDashboard();

    } catch (error) {

        resultDiv.innerHTML =
            `<p class="failure">
                Error: ${error}
            </p>`;
    }
}


// --------------------------------------------------
// MODULE 3
// DEFECT PREDICTION
// --------------------------------------------------

async function predictDefect() {

    const resultDiv =
        document.getElementById(
            "predictionResults"
        );

    const complexity =
        document.getElementById(
            "complexity"
        ).value;

    const changes =
        document.getElementById(
            "changes"
        ).value;

    const previous_bugs =
        document.getElementById(
            "previous_bugs"
        ).value;

    const lines_of_code =
        document.getElementById(
            "lines_of_code"
        ).value;

    const test_failures =
        document.getElementById(
            "test_failures"
        ).value;


    if (
        complexity === "" ||
        changes === "" ||
        previous_bugs === "" ||
        lines_of_code === "" ||
        test_failures === ""
    ) {

        resultDiv.innerHTML =
            `<p class="failure">
                Please enter all values.
            </p>`;

        return;
    }


    resultDiv.innerHTML =
        "<p>Analyzing defect risk...</p>";


    try {

        const response = await fetch(
            "/api/predict-defect",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    complexity:
                        complexity,

                    changes:
                        changes,

                    previous_bugs:
                        previous_bugs,

                    lines_of_code:
                        lines_of_code,

                    test_failures:
                        test_failures

                })
            }
        );


        const data = await response.json();


        if (!data.success) {

            resultDiv.innerHTML =
                `<p class="failure">
                    ${data.message}
                </p>`;

            return;
        }


        let riskClass = "";

        if (data.risk === "HIGH") {

            riskClass = "high";

        } else if (data.risk === "MEDIUM") {

            riskClass = "medium";

        } else {

            riskClass = "low";
        }


        resultDiv.innerHTML = `

            <div class="result-box">

                <div class="risk-result ${riskClass}">

                    Risk Level:
                    ${data.risk}

                </div>

                <p>

                    Defect Probability:
                    <strong>
                        ${data.probability}%
                    </strong>

                </p>

            </div>
        `;


        loadDashboard();

    } catch (error) {

        resultDiv.innerHTML =
            `<p class="failure">
                Error: ${error}
            </p>`;
    }
}


// --------------------------------------------------
// MODULE 4
// DASHBOARD
// --------------------------------------------------

async function loadDashboard() {

    try {

        const response =
            await fetch("/api/dashboard");

        const data =
            await response.json();


        const total =
            document.getElementById(
                "totalTests"
            );

        const passed =
            document.getElementById(
                "passedTests"
            );

        const failed =
            document.getElementById(
                "failedTests"
            );

        const errors =
            document.getElementById(
                "errorTests"
            );

        const high =
            document.getElementById(
                "highRisk"
            );

        const medium =
            document.getElementById(
                "mediumRisk"
            );

        const low =
            document.getElementById(
                "lowRisk"
            );


        if (total)
            total.textContent =
                data.tests.total;

        if (passed)
            passed.textContent =
                data.tests.passed;

        if (failed)
            failed.textContent =
                data.tests.failed;

        if (errors)
            errors.textContent =
                data.tests.errors;

        if (high)
            high.textContent =
                data.risks.HIGH;

        if (medium)
            medium.textContent =
                data.risks.MEDIUM;

        if (low)
            low.textContent =
                data.risks.LOW;


        loadReports(data);

    } catch (error) {

        console.error(
            "Dashboard error:",
            error
        );
    }
}


// --------------------------------------------------
// REPORTS
// --------------------------------------------------

function loadReports(data) {

    const reportSummary =
        document.getElementById(
            "reportSummary"
        );

    if (reportSummary) {

        reportSummary.innerHTML = `

            <div class="dashboard-grid">

                <div class="metric">

                    <h3>Total Tests</h3>

                    <span>
                        ${data.tests.total}
                    </span>

                </div>

                <div class="metric">

                    <h3>Passed</h3>

                    <span>
                        ${data.tests.passed}
                    </span>

                </div>

                <div class="metric">

                    <h3>Failed</h3>

                    <span>
                        ${data.tests.failed}
                    </span>

                </div>

                <div class="metric">

                    <h3>Errors</h3>

                    <span>
                        ${data.tests.errors}
                    </span>

                </div>

            </div>
        `;
    }


    const latestResults =
        document.getElementById(
            "latestResults"
        );


    if (latestResults) {

        if (
            data.latest_results.length === 0
        ) {

            latestResults.innerHTML =
                "<p>No test execution data available.</p>";

        } else {

            let html = `
                <table class="test-table">

                <tr>

                    <th>Date</th>
                    <th>Total</th>
                    <th>Passed</th>
                    <th>Failed</th>
                    <th>Errors</th>
                    <th>Time</th>

                </tr>
            `;


            data.latest_results.forEach(
                result => {

                    html += `

                        <tr>

                            <td>
                                ${result.created_at}
                            </td>

                            <td>
                                ${result.total_tests}
                            </td>

                            <td>
                                ${result.passed}
                            </td>

                            <td>
                                ${result.failed}
                            </td>

                            <td>
                                ${result.errors}
                            </td>

                            <td>
                                ${result.execution_time}s
                            </td>

                        </tr>
                    `;
                }
            );


            html += "</table>";

            latestResults.innerHTML =
                html;
        }
    }


    const latestPredictions =
        document.getElementById(
            "latestPredictions"
        );


    if (latestPredictions) {

        if (
            data.latest_predictions.length === 0
        ) {

            latestPredictions.innerHTML =
                "<p>No defect predictions available.</p>";

        } else {

            let html = `

                <table class="test-table">

                <tr>

                    <th>Date</th>
                    <th>Risk</th>
                    <th>Probability</th>

                </tr>
            `;


            data.latest_predictions.forEach(
                prediction => {

                    html += `

                        <tr>

                            <td>
                                ${prediction.created_at}
                            </td>

                            <td>
                                ${prediction.risk}
                            </td>

                            <td>
                                ${(
                                    prediction.probability * 100
                                ).toFixed(2)}%
                            </td>

                        </tr>
                    `;
                }
            );


            html += "</table>";

            latestPredictions.innerHTML =
                html;
        }
    }
}


function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}



document.addEventListener(
    "DOMContentLoaded",
    function () {

        loadDashboard();

    }
);
