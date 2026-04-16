import { NavLink } from "react-router-dom";

const navigationItems = [
  { to: "/dashboard", label: "Dashboard" },
  { to: "/requests", label: "Requests" },
  { to: "/requests/new", label: "New Request" },
];

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <h1>ProcessPilot</h1>
        <p>Internal workflow portal</p>
      </div>

      <nav className="sidebar-nav">
        {navigationItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              isActive ? "sidebar-link sidebar-link-active" : "sidebar-link"
            }
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}

export default Sidebar;