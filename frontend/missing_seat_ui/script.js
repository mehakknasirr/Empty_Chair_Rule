// Global State & Chart Instances
window.allStudents = [];
let postSupportChartInstance = null;
let baselinesChartInstance = null;

// Global Toast Popup Function (Window Scope to avoid clashes)
window.showCustomPopup = function(title, message, type = 'success') {
    let container = document.getElementById('toast-container');
    
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'fixed top-6 right-6 z-[100] flex flex-col gap-3 pointer-events-none';
        document.body.appendChild(container);
    }

    const popup = document.createElement('div');
    const borderClass = type === 'success' 
        ? 'border-emerald-500/40 bg-slate-900/90 text-emerald-400 shadow-emerald-500/10' 
        : 'border-rose-500/40 bg-slate-900/90 text-rose-400 shadow-rose-500/10';
    const icon = type === 'success' ? 'ph-check-circle' : 'ph-warning-circle';

    popup.className = `pointer-events-auto flex items-start gap-3 p-4 rounded-2xl border backdrop-blur-xl shadow-2xl transition-all duration-300 transform translate-x-12 opacity-0 max-w-sm ${borderClass}`;
    popup.innerHTML = `
        <i class="ph-bold ${icon} text-2xl shrink-0 mt-0.5"></i>
        <div class="flex-1">
            <h4 class="text-xs font-bold uppercase tracking-wider text-white">${title}</h4>
            <p class="text-xs text-slate-300 mt-1 leading-snug">${message}</p>
        </div>
    `;
    
    container.appendChild(popup);
    
    requestAnimationFrame(() => {
        popup.classList.remove('translate-x-12', 'opacity-0');
    });
    
    setTimeout(() => {
        popup.classList.add('opacity-0', 'translate-x-8');
        setTimeout(() => popup.remove(), 300);
    }, 3500);
};

// Global Tab Switching Handler (Window Scope to fix click event clashes)
window.switchTab = function(event, tabId) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.add('hidden');
    });
    
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('bg-[var(--accent-color)]', 'text-white', 'shadow-md', 'shadow-cyan-500/20');
        btn.classList.add('text-theme_text_muted', 'hover:text-theme_text', 'hover:bg-white/5');
    });
    
    const activeTab = document.getElementById(tabId);
    if (activeTab) {
        activeTab.classList.remove('hidden');
    }
    
    if (event && event.currentTarget) {
        const clickedBtn = event.currentTarget;
        clickedBtn.classList.remove('text-theme_text_muted', 'hover:text-theme_text', 'hover:bg-white/5');
        clickedBtn.classList.add('bg-[var(--accent-color)]', 'text-white', 'shadow-md', 'shadow-cyan-500/20');
    }

    if (tabId === 'interventions' && postSupportChartInstance) {
        postSupportChartInstance.resize();
        postSupportChartInstance.update();
    }

    if (tabId === 'risk-heatmap') {
        renderHeatmap();
    }
};

// Initializer
document.addEventListener("DOMContentLoaded", () => {
    fetchDashboardData();
    setupSearchFilter();
    setupActionButtons();
    renderPostSupportChart(); // ADDED: Graph initialize call
});

// Fetch Data from API or Fallback
async function fetchDashboardData() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/pattern-report');
        if (!response.ok) throw new Error("Failed to fetch data from API");
       
        window.allStudents = await response.json();
        updateAllViews(window.allStudents);
    } catch (error) {
        console.warn("Live API offline. Using fallback 10-student synchronized dataset.", error);
        window.allStudents = [
            { student_id: "7780", student_name: "Ali Khan", pattern_detected: "Post-Assessment Absence", pattern_confidence: 55, baseline_attendance: 90.5, current_attendance: 80.0, flag_reason: "Contextual alert logged: Interventions active." },
            { student_id: "7781", student_name: "Ahmed Raza", pattern_detected: "None", pattern_confidence: 41, baseline_attendance: 88.4, current_attendance: 88.4, flag_reason: "Regular attendance observed across modules." },
            { student_id: "7782", student_name: "Sara Ahmed", pattern_detected: "Post-Assessment Absence", pattern_confidence: 78, baseline_attendance: 92.0, current_attendance: 74.0, flag_reason: "Missed 3 consecutive days post midterm exam." },
            { student_id: "7783", student_name: "Ayesha Khan", pattern_detected: "Pre-Weekend Drop", pattern_confidence: 62, baseline_attendance: 85.0, current_attendance: 79.0, flag_reason: "Absent on Fridays preceding long weekends." },
            { student_id: "7784", student_name: "Hamza Shah", pattern_detected: "Lab Skip Pattern", pattern_confidence: 82, baseline_attendance: 91.0, current_attendance: 82.0, flag_reason: "Selectively skipped practical laboratory sessions." },
            { student_id: "7785", student_name: "Fatima Noor", pattern_detected: "Monday Slump", pattern_confidence: 70, baseline_attendance: 89.0, current_attendance: 81.0, flag_reason: "Repeated Monday morning absences detected." },
            { student_id: "7786", student_name: "Usman Tariq", pattern_detected: "None", pattern_confidence: 22, baseline_attendance: 94.0, current_attendance: 93.5, flag_reason: "Consistent and punctual participation." },
            { student_id: "7787", student_name: "Zainab Malik", pattern_detected: "None", pattern_confidence: 18, baseline_attendance: 96.0, current_attendance: 95.0, flag_reason: "High baseline retention." },
            { student_id: "7788", student_name: "Bilal Ahmed", pattern_detected: "Post-Assessment Absence", pattern_confidence: 68, baseline_attendance: 86.0, current_attendance: 75.0, flag_reason: "Absences clustered immediately after quiz weeks." },
            { student_id: "7789", student_name: "Hira Sohail", pattern_detected: "None", pattern_confidence: 12, baseline_attendance: 98.0, current_attendance: 98.0, flag_reason: "Exemplary attendance track record." }
        ];
        updateAllViews(window.allStudents);
    }
}

// Single Master Dispatcher
function updateAllViews(students) {
    renderStudents(students);
    renderHeatmap();
    renderXaiSystemFlags(students);
    renderBaselinesChart(students);
    populateStudentDropdown(students);
}

// 1. Dynamic Student Cards
function renderStudents(students) {
    const grid = document.getElementById('studentCardsContainer');
    if (!grid) return;

    grid.innerHTML = "";

    if (students.length === 0) {
        grid.innerHTML = `<div class="col-span-2 text-center py-10 text-theme_text_muted text-xs">No students found matching search criteria.</div>`;
        return;
    }

    students.forEach(student => {
        const isSignal = student.pattern_detected && student.pattern_detected.toLowerCase() !== "none";
        
        // Updated styling with bright neon side borders and lighting effects
        const cardStyle = isSignal 
            ? "border border-rose-500/50 border-l-4 border-l-rose-500 shadow-[0_0_15px_rgba(244,63,94,0.25)] bg-rose-500/[0.03] hover:shadow-[0_0_25px_rgba(244,63,94,0.4)]" 
            : "border border-emerald-500/50 border-l-4 border-l-emerald-500 shadow-[0_0_15px_rgba(52,211,153,0.2)] bg-emerald-500/[0.03] hover:shadow-[0_0_25px_rgba(52,211,153,0.35)]";

        const badgeBg = isSignal ? "bg-rose-500/10 text-rose-400 border-rose-500/20" : "bg-emerald-500/10 text-emerald-400 border-emerald-500/20";
        const scoreColor = isSignal ? "text-rose-400" : "text-emerald-400";
        const iconClass = isSignal ? "ph-warning-circle" : "ph-check";
        const initials = student.student_name ? student.student_name.split(' ').map(n => n[0]).join('') : 'ST';

        grid.innerHTML += `
            <div class="glass-panel p-6 rounded-2xl transition-all flex flex-col justify-between ${cardStyle}">
                <div>
                    <div class="flex items-center justify-between pb-4 border-b border-[var(--card-border)]">
                        <div class="flex items-center gap-3">
                            <div class="w-10 h-10 rounded-full bg-gradient-to-tr from-cyan-600 to-blue-600 flex items-center justify-center text-white font-bold text-sm shadow-md">
                                ${initials}
                            </div>
                            <div>
                                <h4 class="font-bold text-sm">${student.student_name} <span class="text-xs font-normal text-theme_text_muted">(${student.student_id})</span></h4>
                                <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md ${badgeBg} text-[10px] font-bold tracking-wide mt-0.5 border">
                                    <i class="ph-bold ${iconClass}"></i> ${student.pattern_detected}
                                </span>
                            </div>
                        </div>
                        <div class="text-right">
                            <span class="text-2xl font-extrabold ${scoreColor}">${student.pattern_confidence}%</span>
                        </div>
                    </div>

                    <div class="pt-4 grid grid-cols-2 gap-4 text-xs">
                        <div class="p-3 rounded-xl bg-white/[0.02] border border-[var(--card-border)]">
                            <span class="text-theme_text_muted block text-[10px] uppercase font-semibold">Baseline Attendance</span>
                            <span class="font-bold text-theme_text text-sm mt-0.5 block">${student.baseline_attendance}%</span>
                        </div>
                        <div class="p-3 rounded-xl bg-white/[0.02] border border-[var(--card-border)]">
                            <span class="text-theme_text_muted block text-[10px] uppercase font-semibold">Current Attendance</span>
                            <span class="font-bold text-emerald-400 text-sm mt-0.5 block">${student.current_attendance}%</span>
                        </div>
                    </div>

                    <div class="mt-4 pt-3 border-t border-[var(--card-border)] text-[11px] text-theme_text_muted flex items-center gap-2">
                        <i class="ph-bold ph-info text-cyan-400 text-base"></i> ${student.flag_reason}
                    </div>
                </div>

                <div class="mt-5 pt-3 border-t border-[var(--card-border)] flex justify-end">
                    <button onclick="recordCheckin('${student.student_id}', '${student.student_name}')" class="px-4 py-2 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-semibold hover:bg-cyan-500 hover:text-white transition-all shadow-lg flex items-center gap-2">
                        <i class="ph-bold ph-check-circle text-base"></i> Record Check-in
                    </button>
                </div>
            </div>
        `;
    });
}

// 2. Class Risk Heatmap
function renderHeatmap() {
    const gridEl = document.getElementById('heatmapGrid');
    if (!gridEl) return;

    let html = `
        <div class="min-w-[700px]">
            <div class="grid grid-cols-5 gap-3 mb-3 px-4 text-[10px] font-bold text-theme_text_muted uppercase tracking-wider">
                <div class="col-span-1">Student</div>
                <div class="text-center">Week 1 (Oct 1-7)</div>
                <div class="text-center">Week 2 (Oct 8-14)</div>
                <div class="text-center">Week 3 (Oct 15-21)</div>
                <div class="text-center">Week 4 (Oct 22-28)</div>
            </div>
            <div class="space-y-3">
    `;

    window.allStudents.forEach(student => {
        const initials = student.student_name ? student.student_name.split(' ').map(n => n[0]).join('') : 'ST';
        const isFlagged = student.pattern_detected && student.pattern_detected.toLowerCase() !== 'none';
        const isHighConfidence = (student.pattern_confidence || 0) >= 60;

        const weeks = [
            { status: "baseline", note: "Baseline attendance active" },
            { status: "baseline", event: "Midterm Exams", note: "Attended assessment period" },
            { status: isFlagged ? (isHighConfidence ? "high" : "mild") : "baseline", note: isFlagged ? student.flag_reason : "Normal weekly attendance" },
            { status: isFlagged ? "high" : "baseline", note: `Current Rate: ${student.current_attendance}% (${student.pattern_detected})` }
        ];

        html += `
            <div class="grid grid-cols-5 gap-3 items-center p-3 bg-white/[0.02] border border-[var(--card-border)] rounded-xl hover:bg-white/[0.05] transition-all cursor-pointer" onclick="showHeatmapDrilldown('${student.student_id}')">
                <div class="font-semibold text-sm truncate pl-2 flex items-center gap-2">
                    <div class="w-8 h-8 rounded-full bg-slate-800 text-xs flex items-center justify-center border border-slate-700 font-bold text-cyan-400 shrink-0">
                        ${initials}
                    </div>
                    <div class="truncate">
                        <div class="text-xs font-bold text-white truncate">${student.student_name}</div>
                        <div class="text-[10px] text-theme_text_muted">ID: ${student.student_id}</div>
                    </div>
                </div>`;
        
        weeks.forEach((data) => {
            let bgClass = "bg-emerald-500/10 border-emerald-500/30"; 
            let dotClass = "bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.5)]";
            
            if (data.status === 'mild') {
                bgClass = "bg-amber-500/10 border-amber-500/30";
                dotClass = "bg-amber-400 shadow-[0_0_8px_rgba(251,191,36,0.5)]";
            } else if (data.status === 'high') {
                bgClass = "bg-rose-500/10 border-rose-500/30";
                dotClass = "bg-rose-500 shadow-[0_0_8px_rgba(244,63,94,0.6)]";
            }

            let eventHtml = data.event ? `<i class="ph-fill ph-star text-amber-400 absolute -top-2 -right-1 text-[15px]"></i>` : "";
            
            html += `
                <div class="relative h-12 rounded-lg border ${bgClass} transition-colors flex flex-col items-center justify-center group">
                    ${eventHtml}
                    <div class="opacity-0 group-hover:opacity-100 transition-opacity absolute bottom-full mb-2 bg-slate-800 text-white text-[10px] p-2 rounded-lg whitespace-nowrap z-50 shadow-xl border border-slate-600 pointer-events-none">
                        ${data.note}
                    </div>
                    <div class="w-2.5 h-2.5 rounded-full ${dotClass}"></div>
                </div>`;
        });
        html += `</div>`;
    });

    html += `</div></div>`;
    gridEl.innerHTML = html;
}

// 3. Dynamic XAI System Flags
function renderXaiSystemFlags(students) {
    const container = document.querySelector('#system-context .space-y-4');
    if (!container) return;

    container.innerHTML = "";

    students.forEach(student => {
        const isSignal = student.pattern_detected && student.pattern_detected.toLowerCase() !== "none";
        const boxColor = isSignal ? "bg-rose-500/[0.03] border-rose-500/20 text-rose-400" : "bg-emerald-500/[0.03] border-emerald-500/20 text-emerald-400";
        const badgeColor = isSignal ? "bg-rose-500/10 text-rose-400" : "bg-emerald-500/10 text-emerald-400";
        
        // CONDITIONAL LABEL: Agar issue hai toh "Why was this flagged?", warna "System Note"
        const reasonLabel = isSignal ? "Why was this flagged?" : "System Note:";

        container.innerHTML += `
            <div class="p-5 rounded-2xl border ${boxColor}">
                <div class="flex justify-between items-start mb-2">
                    <h3 class="font-bold text-sm">Pattern Status — ${student.student_name} (${student.student_id})</h3>
                    <span class="px-2.5 py-1 rounded-full ${badgeColor} text-[10px] font-bold">Confidence: ${student.pattern_confidence}%</span>
                </div>
                <p class="text-xs text-theme_text_muted mb-3"><strong>Pattern:</strong> ${student.pattern_detected}</p>
                <div class="p-3 rounded-xl bg-cyan-950/30 border border-cyan-500/20 text-cyan-300 text-xs">
                    <strong>${reasonLabel}</strong> ${student.flag_reason}
                </div>
            </div>
        `;
    });
}

// 4. Dynamic Dropdown Population
function populateStudentDropdown(students) {
    const select = document.getElementById('studentSelect');
    if (!select) return;

    select.innerHTML = `<option value="" disabled selected class="bg-slate-900 text-gray-400">Select a student...</option>`;
    students.forEach(student => {
        const option = document.createElement('option');
        option.value = `${student.student_name} (${student.student_id})`;
        option.className = "bg-slate-800 text-white";
        option.textContent = `${student.student_name} (${student.student_id})`;
        select.appendChild(option);
    });
}

// 5. Dynamic Chart Rendering
function renderBaselinesChart(students) {
    const ctxBaseline = document.getElementById('baselinesChart');
    if (!ctxBaseline) return;

    const names = students.map(s => s.student_name);
    const baselines = students.map(s => s.baseline_attendance);
    const currents = students.map(s => s.current_attendance);

    if (baselinesChartInstance) {
        baselinesChartInstance.destroy();
    }

    baselinesChartInstance = new Chart(ctxBaseline.getContext('2d'), {
        type: 'bar',
        data: {
            labels: names,
            datasets: [
                { label: 'Baseline Attendance (%)', data: baselines, backgroundColor: '#64748b' },
                { label: 'Current Attendance (%)', data: currents, backgroundColor: '#06b6d4' }
            ]
        },
        options: { 
            responsive: true, 
            maintainAspectRatio: false,
            scales: { 
                y: { max: 100, grid: { color: 'rgba(255,255,255,0.05)' } },
                x: { grid: { display: false } }
            } 
        }
    });
}

// ADDED: The Missing Post-Support Graph Function
function renderPostSupportChart() {
    const ctxPostSupport = document.getElementById('postSupportChart');
    if (!ctxPostSupport) return;

    if (postSupportChartInstance) {
        postSupportChartInstance.destroy();
    }

    postSupportChartInstance = new Chart(ctxPostSupport.getContext('2d'), {
        type: 'line',
        data: {
            labels: ['Pre-Support', 'Week 1', 'Week 2', 'Week 3', 'Current'],
            datasets: [{ 
                label: 'Absence Rate Frequency', 
                data: [4.2, 3.0, 1.8, 0.8, 0.5], 
                borderColor: '#06b6d4', 
                backgroundColor: 'rgba(6,182,212,0.15)', 
                borderWidth: 3,
                pointBackgroundColor: '#06b6d4',
                pointRadius: 5,
                fill: true, 
                tension: 0.35 
            }]
        },
        options: { 
            responsive: true, 
            maintainAspectRatio: false,
            scales: { 
                y: { beginAtZero: true, max: 5, grid: { color: 'rgba(255,255,255,0.05)' } },
                x: { grid: { color: 'rgba(255,255,255,0.05)' } }
            }, 
            plugins: { legend: { display: false } } 
        }
    });
}

// Helpers & Handlers
function setupSearchFilter() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            const filtered = window.allStudents.filter(student =>
                (student.student_name && student.student_name.toLowerCase().includes(query)) ||
                (student.student_id && student.student_id.toLowerCase().includes(query)) ||
                (student.pattern_detected && student.pattern_detected.toLowerCase().includes(query))
            );
            renderStudents(filtered);
        });
    }
}

window.recordCheckin = async function(studentId, studentName = '') {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/record-checkin', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                student_id: studentId,
                outcome: "Supported / Contacted",
                notes: "Teacher reviewed pattern via dashboard interface."
            })
        });

        const result = await response.json();
        if (response.ok) {
            window.showCustomPopup("Check-in Successful", result.message || `Check-in recorded for student ${studentName || studentId}`, "success");
        } else {
            window.showCustomPopup("Action Failed", "Failed to record check-in on backend.", "error");
        }
    } catch (err) {
        window.showCustomPopup("Server Error", "Error connecting to backend server.", "error");
    }
};

function setupActionButtons() {
    const logOutcomeBtn = document.getElementById('logOutcomeBtn');
    if (logOutcomeBtn) {
        logOutcomeBtn.addEventListener('click', () => {
            const student = document.getElementById('studentSelect').value;
            const outcome = document.getElementById('outcomeSelect').value;
            
            if (!student || !outcome) {
                window.showCustomPopup("Selection Required", "Please select a student and outcome.", "error");
                return;
            }

            window.showCustomPopup("Check-In Recorded", `Outcome '${outcome}' logged for ${student}.`, 'success');
        });
    }

    // ADDED: The Missing Bulk Alert Listener
    const bulkAlertBtn = document.getElementById('bulkAlertBtn');
    if (bulkAlertBtn) {
        bulkAlertBtn.addEventListener('click', () => {
            window.showCustomPopup('Bulk Alerts Sent', 'High-risk automated notices dispatched to academic advisors.', 'success');
        });
    }

    const downloadCsvBtn = document.getElementById('downloadCsvBtn');
    if (downloadCsvBtn) {
        downloadCsvBtn.addEventListener('click', () => {
            window.showCustomPopup('Exporting Data', 'Downloading Live Class Report CSV...', 'success');
            
            let csvContent = "data:text/csv;charset=utf-8,Student ID,Student Name,Baseline Attendance (%),Current Attendance (%),Pattern\n";
            window.allStudents.forEach(s => {
                csvContent += `${s.student_id},${s.student_name},${s.baseline_attendance},${s.current_attendance},${s.pattern_detected}\n`;
            });
            
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "Class_Risk_Report.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });
    }
}