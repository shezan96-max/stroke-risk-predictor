/* ===============================
   Screen Navigation
================================ */
function goToScreen(screenID) {
    const screens = document.querySelectorAll('.screen');
    screens.forEach(screen => screen.classList.remove('active'));
    document.getElementById(screenID).classList.add('active');
}

/* ===============================
   Submit Data to Backend
================================ */
function submitData() {
    const payload = {};

    // 🔹 Basic info
    const inputs = document.querySelectorAll('#screen-user input');
    payload.age = Number(inputs[1].value);
    payload.weight = Number(inputs[2].value);
    payload.height = Number(inputs[3].value);

    // 🔹 Lifestyle habits
    const lifestyleChecks = document.querySelectorAll(
        '#screen-lifestyle input[type="checkbox"]'
    );
    lifestyleChecks.forEach(cb => {
        payload[cb.value] = cb.checked ? 1 : 0;
    });

    // 🔹 Clinical symptoms
    const symptomChecks = document.querySelectorAll(
        '#screen-symptoms input[type="checkbox"]'
    );
    symptomChecks.forEach(cb => {
        payload[cb.value] = cb.checked ? 1 : 0;
    });

    fetch("/predict?explain=true", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        console.log("🧪 API RESPONSE:", data);
        showResult(data);
    })
    .catch(err => {
        console.error("Frontend error:", err);
        alert("Prediction failed. Please try again.");
    });
}

/* ===============================
   Show Result Screen
================================ */
function showResult(data) {
    const card = document.getElementById("result-card");
    const badge = document.getElementById("risk-badge");
    const summary = document.getElementById("risk-summary");
    const title = document.getElementById("guidance-title");
    const message = document.getElementById("risk-message");
    const awareness = document.getElementById("awareness-box");
    const explainBox = document.getElementById("explain-box");
    const progressBox = document.getElementById("progress-box");

    /* ---------- RESET UI ---------- */
    card.className = "result-card";
    badge.className = "risk-badge";
    awareness.innerHTML = "";
    explainBox.classList.add("hidden");
    explainBox.innerHTML = "";
    progressBox.innerHTML = "";

    /* ---------- LOAD PREVIOUS RESULT ---------- */
    let progressHTML = "";
    const prev = localStorage.getItem("lastStrokeResult");

    if (prev) {
        try {
            const prevData = JSON.parse(prev);

            if (prevData.risk && prevData.risk !== data.risk) {
                if (data.risk === "Low Risk") {
                    progressHTML =
                        "📈 <strong>Good news:</strong> Your risk appears to have improved since last check.";
                } else {
                    progressHTML =
                        "⚠️ <strong>Notice:</strong> Your risk appears higher than last time.";
                }
            } else {
                progressHTML =
                    "⏸️ Your risk level appears unchanged since last check.";
            }

            if (
                prevData.lifestyle_score !== null &&
                data.lifestyle_score !== undefined
            ) {
                if (data.lifestyle_score < prevData.lifestyle_score) {
                    progressHTML +=
                        "<br>✅ Lifestyle habits have improved.";
                } else if (data.lifestyle_score > prevData.lifestyle_score) {
                    progressHTML +=
                        "<br>⚠️ Lifestyle habits need more attention.";
                } else {
                    progressHTML +=
                        "<br>➖ Lifestyle habits unchanged.";
                }
            }
        } catch (e) {
            // ignore corrupted storage
        }
    }

    /* ---------- RISK UI + SUMMARY ---------- */
    if (data.risk === "High Risk") {
        card.classList.add("high");
        badge.innerText = "🔴 HIGH RISK";
        title.innerText = "🚨 Immediate Actions";
        summary.innerText =
            "Based on your age, lifestyle, and symptoms, your current stroke risk appears high.";
    } else {
        card.classList.add("low");
        badge.innerText = "🟡 LOW / MODERATE RISK";
        title.innerText = "🧠 Preventive Guidance";
        summary.innerText =
            "Based on your age, lifestyle, and symptoms, your current stroke risk appears moderate.";
    }

    /* ---------- MESSAGE ---------- */
    message.innerText = data.message || "";

    /* ---------- GUIDANCE GROUPING ---------- */
    if (data.guidance && data.guidance.length > 0) {
        let habits = [];
        let medical = [];

        data.guidance.forEach(item => {
            if (
                item.toLowerCase().includes("doctor") ||
                item.toLowerCase().includes("medical") ||
                item.toLowerCase().includes("consult")
            ) {
                medical.push(item);
            } else {
                habits.push(item);
            }
        });

        let html = "";

        if (habits.length > 0) {
            html += "<h4>🧠 Preventive Habits</h4><ul>";
            habits.forEach(h => html += `<li>${h}</li>`);
            html += "</ul>";
        }

        if (medical.length > 0) {
            html += "<h4>❤️ Medical Attention</h4><ul>";
            medical.forEach(m => html += `<li>${m}</li>`);
            html += "</ul>";
        }

        html += `
            <h4>📅 What to do next</h4>
            <ul>
                <li>Monitor your symptoms regularly</li>
                <li>Re-check your risk after lifestyle improvements</li>
            </ul>
        `;

        awareness.innerHTML = html;
    } else {
        awareness.innerHTML =
            "<p>Maintain healthy habits and monitor your health regularly.</p>";
    }

    /* ---------- EXPLAINABILITY ---------- */
    if (data.top_features && data.top_features.length > 0) {
        let html =
            "<p><strong>This risk is influenced by:</strong></p><ul>";
        data.top_features.forEach(f => {
            html += `<li>${humanizeFeature(f)}</li>`;
        });
        html += "</ul>";
        explainBox.innerHTML = html;
    } else {
        explainBox.innerHTML = `
            <p><strong>Why this risk?</strong></p>
            <ul>
                <li>Your age and body indicators</li>
                <li>Your lifestyle habits</li>
                <li>The symptoms you selected</li>
            </ul>
            <p style="font-size:13px;color:#555;">
                This assessment is for awareness only, not a diagnosis.
            </p>
        `;
    }

    /* ---------- PROGRESS RENDER ---------- */
    if (progressHTML) {
        progressBox.innerHTML = progressHTML;
    }

    /* ---------- SAVE CURRENT RESULT ---------- */
    const snapshot = {
        risk: data.risk,
        lifestyle_score: data.lifestyle_score ?? null,
        timestamp: Date.now()
    };
    localStorage.setItem(
        "lastStrokeResult",
        JSON.stringify(snapshot)
    );

    goToScreen("screen-result");
}

/* ===============================
   Explain Button Toggle
================================ */
function toggleExplain() {
    const box = document.getElementById("explain-box");
    if (!box) return;
    box.classList.toggle("hidden");
}

/* ===============================
   Helper: Human readable feature
================================ */
function humanizeFeature(feature) {
    const map = {
        high_blood_pressure: "High blood pressure",
        smoking: "Smoking habit",
        alcohol: "Alcohol consumption",
        poor_sleep: "Poor sleep pattern",
        physical_inactivity: "Lack of physical activity",
        high_stress: "High stress level",
        bmi: "Body weight (BMI)",
        age: "Age factor"
    };
    return map[feature] || feature.replace(/_/g, " ");
}
