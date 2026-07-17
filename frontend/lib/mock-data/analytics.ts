// ─── Analytics Mock Data ─────────────────────────────────────────────────────

// Monthly crime counts broken down by category (Jan–Jun 2024)
export const MONTHLY_TREND = [
  { month: "Jan", violent: 312, property: 421, cyber: 198, narcotics: 134, financial: 98 },
  { month: "Feb", violent: 289, property: 398, cyber: 223, narcotics: 119, financial: 112 },
  { month: "Mar", violent: 334, property: 445, cyber: 267, narcotics: 143, financial: 124 },
  { month: "Apr", violent: 298, property: 412, cyber: 241, narcotics: 128, financial: 108 },
  { month: "May", violent: 321, property: 387, cyber: 289, narcotics: 156, financial: 143 },
  { month: "Jun", violent: 293, property: 278, cyber: 185, narcotics:  63, financial:  36 },
];

// Crime type distribution (current period)
export const CRIME_TYPE_BREAKDOWN = [
  { name: "Property",  value: 2341, prev: 2198, color: "#0070f3" },
  { name: "Violent",   value: 1847, prev: 1654, color: "#ff2d55" },
  { name: "Cyber",     value: 1403, prev:  987, color: "#bf5af2" },
  { name: "Narcotics", value:  743, prev:  821, color: "#ff8c00" },
  { name: "Financial", value:  621, prev:  543, color: "#30d158" },
  { name: "Other",     value:  412, prev:  398, color: "#526080" },
];

// Case status distribution
export const STATUS_DISTRIBUTION = [
  { name: "Open",          value: 1203, color: "#0070f3" },
  { name: "Investigating", value:  847, color: "#ffd60a" },
  { name: "Closed",        value: 2841, color: "#30d158" },
  { name: "Escalated",     value:  128, color: "#ff2d55" },
  { name: "Pending",       value:  195, color: "#526080" },
];

// Top districts by crime count
export const TOP_DISTRICTS = [
  { name: "Central Delhi",    crimes: 421, resolved: 312, rate: 74, color: "#ff2d55" },
  { name: "Mumbai City",      crimes: 389, resolved: 267, rate: 69, color: "#ff8c00" },
  { name: "Bengaluru Urban",  crimes: 312, resolved: 241, rate: 77, color: "#0070f3" },
  { name: "Hyderabad",        crimes: 287, resolved: 198, rate: 69, color: "#bf5af2" },
  { name: "Gurugram",         crimes: 234, resolved: 187, rate: 80, color: "#30d158" },
  { name: "Pune",             crimes: 198, resolved: 145, rate: 73, color: "#0070f3" },
  { name: "Noida",            crimes: 176, resolved: 121, rate: 69, color: "#ffd60a" },
  { name: "Chennai Central",  crimes: 154, resolved: 118, rate: 77, color: "#526080" },
];

// Year-over-year comparison
export const YOY_STATS = [
  { label: "Total Crimes",      current: 7167, previous: 6854, unit: "" },
  { label: "Detection Rate",    current: 73.2, previous: 68.4, unit: "%" },
  { label: "Avg Response Time", current: 8.4,  previous: 11.2, unit: "min", lowerIsBetter: true },
  { label: "Open Cases",        current: 1203, previous: 1487, unit: "", lowerIsBetter: true },
];

// Day × Hour heatmap data (7 days × 24 hours) — crime count per cell
// Rows = Mon(0)…Sun(6), Cols = Hour 0…23
function buildHeatmap(): number[][] {
  const days: number[][] = [];
  for (let d = 0; d < 7; d++) {
    const hours: number[] = [];
    for (let h = 0; h < 24; h++) {
      let base = Math.random() * 3;
      // Weekends spike
      if (d >= 5) base *= 1.6;
      // Late night spike (22–3)
      if (h >= 22 || h <= 3) base *= 2.2;
      // Evening rush (18–21)
      if (h >= 18 && h < 22) base *= 1.5;
      // Morning lull (5–8)
      if (h >= 5 && h < 8) base *= 0.4;
      hours.push(Math.min(10, Math.round(base)));
    }
    days.push(hours);
  }
  return days;
}

// Stable seed — generated once so SSR/CSR match
export const HEATMAP_DATA: number[][] = [
  [4,5,5,4,3,1,0,1,2,2,3,3,3,3,3,3,4,4,5,5,6,7,7,6],
  [3,4,4,3,2,1,0,1,2,3,3,3,3,3,4,4,4,5,5,6,6,7,6,5],
  [3,3,4,3,2,1,0,1,2,3,4,4,3,3,3,4,4,5,6,6,7,7,6,5],
  [4,4,5,4,2,1,0,1,2,3,3,3,3,3,3,3,5,5,6,7,7,8,7,6],
  [4,4,5,4,2,1,0,1,2,3,3,4,3,4,4,4,5,6,7,7,8,9,8,6],
  [5,6,7,6,4,2,1,1,2,4,4,5,5,5,5,6,7,8,9,9,9,10,9,7],
  [5,6,6,5,3,1,0,1,2,3,4,5,5,4,4,5,6,7,8,9,9,10,8,6],
];

export const DAYS_OF_WEEK = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
export const HOURS = Array.from({ length: 24 }, (_, i) =>
  i === 0 ? "12am" : i < 12 ? `${i}am` : i === 12 ? "12pm" : `${i - 12}pm`
);
