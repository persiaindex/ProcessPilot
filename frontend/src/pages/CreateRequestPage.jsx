import { useState } from "react";

import PageHeader from "../components/PageHeader";

const initialForm = {
  title: "",
  description: "",
  priority: "medium",
  department: "",
};

function CreateRequestPage() {
  const [formData, setFormData] = useState(initialForm);

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData((current) => ({
      ...current,
      [name]: value,
    }));
  }

  function handleSubmit(event) {
    event.preventDefault();
    console.log("Day 8 placeholder submit:", formData);
  }

  return (
    <section>
      <PageHeader
        title="New Request"
        description="Create a new internal process request."
      />

      <form className="panel form-layout" onSubmit={handleSubmit}>
        <label>
          Title
          <input
            name="title"
            type="text"
            value={formData.title}
            onChange={handleChange}
            placeholder="Enter request title"
          />
        </label>

        <label>
          Description
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="Describe the problem or request"
            rows="5"
          />
        </label>

        <label>
          Priority
          <select
            name="priority"
            value={formData.priority}
            onChange={handleChange}
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </label>

        <label>
          Department
          <input
            name="department"
            type="text"
            value={formData.department}
            onChange={handleChange}
            placeholder="Engineering"
          />
        </label>

        <button type="submit">Save Draft</button>
      </form>
    </section>
  );
}

export default CreateRequestPage;