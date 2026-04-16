function PageHeader({ title, description }) {
  return (
    <header className="page-header">
      <h2>{title}</h2>
      <p>{description}</p>
    </header>
  );
}

export default PageHeader;