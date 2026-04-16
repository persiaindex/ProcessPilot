import { useParams } from "react-router-dom";

import PageHeader from "../components/PageHeader";

function RequestDetailPage() {
  const { requestId } = useParams();

  return (
    <section>
      <PageHeader
        title={`Request #${requestId}`}
        description="Inspect request metadata, comments, and workflow history."
      />

      <div className="panel">
        <p>This is a placeholder detail page for request {requestId}.</p>
        <p>Later days will load full backend data here.</p>
      </div>
    </section>
  );
}

export default RequestDetailPage;