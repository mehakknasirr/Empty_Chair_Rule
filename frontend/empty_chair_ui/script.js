let allStudents = [];

// Custom Glassmorphism Toast Popup Function
function showCustomPopup(title, message, type = 'success') {
    let container = document.getElementById('toast-container');
    
    // Agar index.html mein toast container missing ho toh dynamically create karein
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
}

// Theme Toggle Functionality
function toggleTheme() {
    const htmlEl = document.documentElement;
    const themeIcon = document.getElementById('themeIcon');
    const themeText = document.getElementById('themeText');

    htmlEl.classList.toggle('light');

    if (htmlEl.classList.contains('light')) {
        if (themeIcon) themeIcon.className = "ph-bold ph-sun text-base text-amber-500";
        if (themeText) themeText.innerText = "Dark Mode";
    } else {
        if (themeIcon) themeIcon.className = "ph-bold ph-moon text-base text-theme_accent";
        if (themeText) themeText.innerText = "Light Mode";
    }
}

// Single Consolidated DOMContentLoaded Event Listener
document.addEventListener("DOMContentLoaded", () => {
    fetchDashboardData();
    setupSearchFilter();
});

// Sidebar View Switching Handler
function switchTab(event, tabId) {
    // Hide all tab content sections
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.add('hidden');
    });

    // Show targeted tab
    const activeContent = document.getElementById(tabId);
    if (activeContent) {
        activeContent.classList.remove('hidden');
    }

    // Update Sidebar Navigation button styles
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('bg-[var(--accent-color)]', 'text-white', 'shadow-md', 'shadow-cyan-500/20');
        btn.classList.add('text-theme_text_muted');
    });

    if (event && event.currentTarget) {
        event.currentTarget.classList.add('bg-[var(--accent-color)]', 'text-white', 'shadow-md', 'shadow-cyan-500/20');
        event.currentTarget.classList.remove('text-theme_text_muted');
    }
}

// Fetch Live Data on Page Load
async function fetchDashboardData() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/pattern-report');
        if (!response.ok) throw new Error("Failed to fetch data from API");
       
        allStudents = await response.json();
        processDashboardMetrics(allStudents);
        renderStudents(allStudents);
    } catch (error) {
        console.warn("Live API connection offline. Using fallback data.", error);
        allStudents = [
            { student_id: "7780", student_name: "Ali Khan", pattern_detected: "Post-Assessment Absence", pattern_confidence: 55, baseline_attendance: 90.5, current_attendance: 80.0, flag_reason: "Contextual alert logged: Interventions & Controls active." },
            { student_id: "7781", student_name: "Ahmed Raza", pattern_detected: "None", pattern_confidence: 41, baseline_attendance: 88.4, current_attendance: 88.4, flag_reason: "Regular attendance observed across all modules." }
        ];
        processDashboardMetrics(allStudents);
        renderStudents(allStudents);
    }
}

// Metrics Display Update
function processDashboardMetrics(students) {
    const totalMonitored = students.length;
    const patternsDetected = students.filter(s => s.pattern_detected && s.pattern_detected.toLowerCase() !== "none").length;
   
    const totalConfidence = students.reduce((sum, s) => sum + (s.pattern_confidence || 0), 0);
    const avgConfidence = totalMonitored > 0 ? Math.round(totalConfidence / totalMonitored) : 0;
   
    const flaggedCount = students.filter(s => (s.pattern_confidence || 0) > 50).length;
    const flagPercentage = totalMonitored > 0 ? Math.round((flaggedCount / totalMonitored) * 100) : 0;

    const metricCards = document.querySelectorAll('.grid-cols-1.sm\\:grid-cols-2.lg\\:grid-cols-4 > div');
   
    if (metricCards.length >= 4) {
        if (metricCards[0].querySelector('h3')) metricCards[0].querySelector('h3').innerText = totalMonitored;
        if (metricCards[1].querySelector('h3')) metricCards[1].querySelector('h3').innerText = patternsDetected;
        if (metricCards[2].querySelector('h3')) metricCards[2].querySelector('h3').innerText = avgConfidence + "%";
        if (metricCards[3].querySelector('h3')) metricCards[3].querySelector('h3').innerText = flagPercentage + "%";
    }
}

// Search Filter Input
function setupSearchFilter() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            const filtered = allStudents.filter(student =>
                (student.student_name && student.student_name.toLowerCase().includes(query)) ||
                (student.student_id && student.student_id.toLowerCase().includes(query)) ||
                (student.pattern_detected && student.pattern_detected.toLowerCase().includes(query))
            );
            renderStudents(filtered);
        });
    }
}

// Render Student Cards Grid
function renderStudents(students) {
    const grid = document.querySelector('#analytics-home .grid.grid-cols-1.lg\\:grid-cols-2.gap-6') || document.getElementById('studentCardsContainer');
    if (!grid) return;

    grid.innerHTML = "";

    if (students.length === 0) {
        grid.innerHTML = `<div class="col-span-2 text-center py-10 text-theme_text_muted text-xs">No students found matching your search.</div>`;
        return;
    }

    students.forEach(student => {
        const isSignal = student.pattern_detected && student.pattern_detected.toLowerCase() !== "none";
        const borderColor = isSignal ? "hover:border-rose-500/40" : "hover:border-emerald-500/40";
        const badgeBg = isSignal ? "bg-rose-500/10 text-rose-400 border-rose-500/20" : "bg-emerald-500/10 text-emerald-400 border-emerald-500/20";
        const scoreColor = isSignal ? "text-rose-400" : "text-emerald-400";
        const iconClass = isSignal ? "ph-warning-circle" : "ph-check";
        const initials = student.student_name ? student.student_name.split(' ').map(n => n[0]).join('') : 'ST';

        const card = `
            <div class="glass-panel p-6 rounded-2xl border border-[var(--card-border)] ${borderColor} transition-all flex flex-col justify-between">
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
                    <button onclick="recordCheckin('${student.student_id}')" class="px-4 py-2 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-semibold hover:bg-cyan-500 hover:text-white transition-all shadow-lg flex items-center gap-2">
                        <i class="ph-bold ph-check-circle text-base"></i> Record Check-in
                    </button>
                </div>
            </div>
        `;
        grid.innerHTML += card;
    });
}

// Backend Check-in Action (Fixed with Toast Popup)
async function recordCheckin(studentId) {
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
            showCustomPopup("Check-in Successful", result.message || `Check-in recorded for student ${studentId}`, "success");
        } else {
            showCustomPopup("Action Failed", "Failed to record check-in on backend.", "error");
        }
    } catch (err) {
        console.error("Error:", err);
        showCustomPopup("Server Error", "Error connecting to backend server.", "error");
    }
}
// Quick Filter by Risk Level
function filterByRisk(type) {
    // Update button styles
    document.querySelectorAll('.risk-filter-btn').forEach(btn => {
        btn.classList.remove('bg-cyan-500/20', 'text-cyan-400', 'border-cyan-500/40');
        btn.classList.add('bg-white/[0.04]', 'text-theme_text_muted', 'border-[var(--card-border)]');
    });

    if (event && event.currentTarget) {
        event.currentTarget.classList.add('bg-cyan-500/20', 'text-cyan-400', 'border-cyan-500/40');
        event.currentTarget.classList.remove('bg-white/[0.04]', 'text-theme_text_muted');
    }

    // Filter students data
    if (type === 'flagged') {
        const flagged = allStudents.filter(s => s.pattern_detected && s.pattern_detected.toLowerCase() !== 'none');
        renderStudents(flagged);
    } else if (type === 'normal') {
        const normal = allStudents.filter(s => !s.pattern_detected || s.pattern_detected.toLowerCase() === 'none');
        renderStudents(normal);
    } else {
        renderStudents(allStudents);
    }
}
