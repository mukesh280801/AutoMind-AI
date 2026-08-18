import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="flex items-center justify-between px-10 py-5 border-b border-slate-800 bg-slate-950">

      {/* Logo */}
      <Link
        to="/"
        className="text-2xl font-bold text-cyan-400 hover:text-cyan-300 transition"
      >
        AutoMind AI
      </Link>

      {/* Navigation */}
      <div className="flex items-center gap-8">

        <Link
          to="/"
          className="text-slate-300 hover:text-cyan-400 transition"
        >
          Home
        </Link>

        <Link
          to="/dashboard"
          className="text-slate-300 hover:text-cyan-400 transition"
        >
          Dashboard
        </Link>

        <Link
          to="/chat"
          className="text-slate-300 hover:text-cyan-400 transition"
        >
          AI Chat
        </Link>

        <Link
          to="/upload"
          className="text-slate-300 hover:text-cyan-400 transition"
        >
          Upload
        </Link>

      </div>

      {/* Button */}
      <Link
        to="/dashboard"
        className="bg-cyan-500 hover:bg-cyan-600 px-5 py-2 rounded-lg font-semibold transition"
      >
        Get Started
      </Link>

    </nav>
  );
}

export default Navbar;