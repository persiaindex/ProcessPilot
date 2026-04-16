import PageHeader from "../components/PageHeader";

const summaryCards = [
  { label: "Open Requests", value: "12" },
  { label: "In Review", value: "4" },
  { label: "Approved This Week", value: "9" },
];

const recentActivity = [
  "Cooling system review moved to in_review",
  "Laptop replacement request submitted",
  "Simulation workstation upgrade approved",
];

function DashboardPage() {
  return (
    <section>
      <PageHeader
        title="Dashboard"
        description="Track requests, review workload, and recent process activity."
      />

      <div className="card-grid">
        {summaryCards.map((card) => (
          <article key={card.label} className="card">
            <p className="card-label">{card.label}</p>
            <strong className="card-value">{card.value}</strong>
          </article>
        ))}
      </div>

      <div className="panel">
        <h3>Recent activity</h3>
        <ul>
          {recentActivity.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </div>
    </section>
  );
}

export default DashboardPage;