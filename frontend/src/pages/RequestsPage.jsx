import PageHeader from "../components/PageHeader";

const requestRows = [
  {
    id: 1,
    title: "Simulation workstation upgrade",
    department: "Engineering",
    status: "submitted",
    priority: "high",
  },
  {
    id: 2,
    title: "Cooling system maintenance",
    department: "Operations",
    status: "in_review",
    priority: "medium",
  },
];

function RequestsPage() {
  return (
    <section>
      <PageHeader
        title="Requests"
        description="Browse current process requests across departments."
      />

      <div className="panel">
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Department</th>
              <th>Status</th>
              <th>Priority</th>
            </tr>
          </thead>
          <tbody>
            {requestRows.map((row) => (
              <tr key={row.id}>
                <td>{row.id}</td>
                <td>{row.title}</td>
                <td>{row.department}</td>
                <td>{row.status}</td>
                <td>{row.priority}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default RequestsPage;