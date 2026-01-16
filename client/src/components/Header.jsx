import logo from "../assets/logo.png";

function Header() {
    return (
        <header className="site-header">
            <img src={logo} alt="Site logo" className="logo" />
        </header>
    );
}

export default Header;
