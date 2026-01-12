import Navbar from "./NavBar";

export default function Layout({ children }) {
  return (
    <div className="bg-gray-50 min-h-screen">
      <Navbar />
      <main className="pt-20 px-6">{children}</main>
    </div>
  );
}
