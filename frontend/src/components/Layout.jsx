import Header from "./Header";
import Footer from "./Footer";

const Layout = ({ sidebar, children }) => {
  return (
    <div>
      <Header />
      <div className="flex pt-12">
        {sidebar}
        <div className="ml-64 flex-1 p-4">{children}</div>
      </div>
      <Footer />
    </div>
  );
};

export default Layout;
